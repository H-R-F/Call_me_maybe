import re
import json
from llm_sdk import Small_LLM_Model
from .schema import FunctionDefinition


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[int, TrieNode] = {}
        self.terminal: bool = False

    def insert(self, token_ids: list[int]) -> None:
        node = self
        for token_id in token_ids:
            if token_id not in node.children:
                node.children[token_id] = TrieNode()
            node = node.children[token_id]
        node.terminal = True


class ConstrainedDecoder():
    def __init__(
        self, model: Small_LLM_Model, function: list[FunctionDefinition]
    ):
        self.model = model
        self.functions_by_name: dict[str, FunctionDefinition] = {
            fn.name: fn for fn in function
        }

        # Load vocabulary
        vocab_path = self.model.get_path_to_vocab_file()
        with open(vocab_path, 'r') as f:
            vocab_str_to_id = json.load(f)
        self.vocab: dict[int, str] = {v: k for k, v in vocab_str_to_id.items()}

        #  Pre-compute vocab list for faster iteration
        self.vocab_items = list(self.vocab.items())
        self.vocab_size = len(self.vocab)

        # Build function name trie
        self.func_trie = TrieNode()
        for name in self.functions_by_name:
            token_ids = self.model.encode(name).tolist()[0]
            self.func_trie.insert(token_ids)

        # Build boolean trie
        self.bool_trie = TrieNode()
        for bool_str in ["true", "false"]:
            token_ids = self.model.encode(bool_str).tolist()[0]
            self.bool_trie.insert(token_ids)

        #  Pre-encode fixed tokens (already doing this!)
        # Changed to list for multi-token
        self.fixed_tokens: dict[str, list[int]] = {}
        for text in ["{", '"name"', '"parameters"', ":", ",", "}", '"']:
            self.fixed_tokens[text] = self.model.encode(text).tolist()[0]

    def generate_function_name(self, input_ids: list[int]) -> list[int]:
        current_node = self.func_trie
        generated_tokens: list[int] = []
        max_step = 10

        for _ in range(max_step):
            allowed_token_ids = list(current_node.children.keys())

            if not allowed_token_ids:
                raise ValueError("No Valid token available in trie")

            full_input = input_ids + generated_tokens
            logit = self.model.get_logits_from_input_ids(full_input)

            masked_logit = logit.copy()
            # only check allowed tokens
            for token_id in range(len(masked_logit)):
                if token_id not in allowed_token_ids:
                    masked_logit[token_id] = float('-inf')

            chosen_max = max(
                range(len(masked_logit)),
                key=lambda k: masked_logit[k],
            )

            if masked_logit[chosen_max] == float('-inf'):
                chosen_token = allowed_token_ids[0]
            else:
                chosen_token = chosen_max

            generated_tokens.append(chosen_token)
            current_node = current_node.children[chosen_token]

            if current_node.terminal:
                break

        return generated_tokens

    def generate_boolean(self, input_ids: list[int]) -> list[int]:
        current_node = self.bool_trie
        generate_tokens: list[int] = []
        max_step = 5

        for _ in range(max_step):
            allowed_token_ids = list(current_node.children.keys())

            if not allowed_token_ids:
                raise ValueError("No Valide token available in trie")

            full_input = input_ids + generate_tokens
            logit = self.model.get_logits_from_input_ids(full_input)

            masked_logit = logit.copy()
            # only check allowed tokens
            for token_id in range(len(masked_logit)):
                if token_id not in allowed_token_ids:
                    masked_logit[token_id] = float('-inf')

            chosen_max = max(
                range(len(masked_logit)),
                key=lambda k: masked_logit[k],
            )

            if masked_logit[chosen_max] == float('-inf'):
                chosen_token = allowed_token_ids[0]
            else:
                chosen_token = chosen_max

            generate_tokens.append(chosen_token)
            current_node = current_node.children[chosen_token]

            if current_node.terminal:
                break
        return generate_tokens

    def generate_number(
        self,
        input_ids: list[int],
        source_text: str = "",
    ) -> list[int]:
        generated_tokens: list[int] = []
        prefix = ""
        max_step = 20

        def clean_token(s: str | None) -> str:
            if s is None:
                return ""
            return s.lstrip('Ġ')

        def is_valid_number_prefix(s: str) -> bool:
            if not s:
                return True
            if s == '-':
                return True
            if not re.match(r'^-?[0-9]*\.?[0-9]*([eE][+-]?[0-9]*)?$', s):
                return False
            if len(s) > 1 and s[0] == '0' and s[1] not in ['.', 'e', 'E']:
                return False
            if s.count('.') > 1:
                return False
            if s.lower().count('e') > 1:
                return False
            if '.' in s and s[-1] != '.':
                parts = s.split('.')
                if len(parts) > 2:
                    return False
                if len(parts) == 2 and not parts[1].isdigit():
                    return False
            return True

        def is_complete_number(s: str) -> bool:
            if not s:
                return False
            if not s[-1].isdigit():
                return False
            return bool(re.fullmatch(
                r'^-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?', s
            ))

        for _ in range(max_step):
            full_input = input_ids + generated_tokens
            logit = self.model.get_logits_from_input_ids(full_input)

            unconstrainde_choice = max(
                range(len(logit)), key=lambda k: logit[k]
            )
            unconstrainde_choice_str = self.vocab.get(
                unconstrainde_choice
            )

            if is_complete_number(prefix):
                would_extend = (
                    unconstrainde_choice_str is not None
                    and is_valid_number_prefix(
                        prefix + clean_token(unconstrainde_choice_str)
                    )
                )
                if not would_extend:
                    break

            masked_logit = logit.copy()
            for token_id, token_str in self.vocab_items:
                if token_str is None:
                    masked_logit[token_id] = float('-inf')
                    continue

                if prefix and token_str.startswith('Ġ'):
                    masked_logit[token_id] = float('-inf')
                    continue

                c = clean_token(token_str)
                new_prefix = prefix + c
                if not is_valid_number_prefix(new_prefix):
                    masked_logit[token_id] = float('-inf')

            chosen_max = max(
                range(len(masked_logit)),
                key=lambda k: masked_logit[k],
            )

            generated_tokens.append(chosen_max)
            prefix += clean_token(self.vocab.get(chosen_max, ""))

        if source_text:
            generated_value = prefix
            corrected = self._correct_number_from_source(
                generated_value, source_text
            )
            if corrected != generated_value:
                # re-encode l-corrected value w regenerate tokens
                new_tokens = self.model.encode(corrected).tolist()[0]
                return new_tokens

        return generated_tokens

    def _correct_number_from_source(
        self, generated: str, source_text: str
    ) -> str:
        """
        Ila l-value li generated model qariba (nafs digits)
        m3a number f source, walakin naqsa negative sign,
        sе7е7ha.
        """
        if not generated:
            return generated

        # jib gemi3 numbers li kaynin f source (b sign dyalhom)
        source_numbers = re.findall(r'-?\d+\.?\d*', source_text)

        for num in source_numbers:
            # ila l-magnitude (bla sign) kif kif,
            # w source 3ando "-" wla model nassah
            if (num.lstrip('-') == generated.lstrip('-')
                    and num != generated):
                return num

        return generated

    def generate_string(self, input_ids: list[int]) -> list[int]:
        generated_tokens: list[int] = []
        prefix = ""
        max_step = 50

        def is_valid_string_prefix(s: str, token_str: str) -> bool:
            if not s:
                return True
            if len(s) == 1:
                return s == '"'
            i = 0
            while i < len(s):
                char = s[i]
                if ord(char) == 92:
                    if i + 1 == len(s):
                        return True
                    next_char = s[i+1]
                    valid_escapes = [92, 47, 34, 98, 102, 110, 114, 116, 117]
                    if ord(next_char) not in valid_escapes:
                        return False
                    i += 2
                    continue
                if char == '"':
                    if i > 0:
                        if i == len(s) - 1:
                            return True
                        if i == len(s) - len(token_str):
                            return True
                        return False
                if ord(char) < 32:
                    return False
                i += 1
            return True

        # Use pre-encoded quote token
        quote_token = self.fixed_tokens['"']
        generated_tokens.extend(quote_token)
        prefix += '"'

        for _ in range(max_step):
            full_input = input_ids + generated_tokens
            logit = self.model.get_logits_from_input_ids(full_input)

            masked_logit = logit.copy()

            # iterate over pre-computed vocab items
            for token_id, token_str in self.vocab_items:
                if token_str is None:
                    masked_logit[token_id] = float('-inf')
                    continue
                new_prefix = prefix + token_str
                if not is_valid_string_prefix(new_prefix, token_str):
                    masked_logit[token_id] = float('-inf')

            chosen_max = max(
                range(len(masked_logit)),
                key=lambda k: masked_logit[k],
            )
            chosen_str = self.vocab.get(chosen_max, "")

            new_prefix = prefix + chosen_str
            i = 1
            is_complete = False
            while i < len(new_prefix):
                if new_prefix[i] == '\\':
                    i += 2
                    continue
                if new_prefix[i] == '"':
                    is_complete = True
                    break
                i += 1

            if is_complete:
                if i < len(new_prefix) - 1:
                    generated_tokens.extend(quote_token)
                    prefix += '"'
                else:
                    generated_tokens.append(chosen_max)
                    prefix += chosen_str
                break
            else:
                generated_tokens.append(chosen_max)
                prefix += chosen_str

        return generated_tokens

    def generate_parameter_value(
        self,
        input_ids: list[int],
        ParameterType: str,
        source_text: str = "",
    ) -> list[int]:
        if ParameterType == "string":
            return self.generate_string(input_ids)
        elif ParameterType == "number":
            return self.generate_number(input_ids, source_text=source_text)
        elif ParameterType == "integer":
            return self.generate_number(input_ids, source_text=source_text)
        elif ParameterType == "boolean":
            return self.generate_boolean(input_ids)
        else:
            raise ValueError(f"Invalid parameter type: {ParameterType}")


def _build_instruction_prompt(
    prompt: str, functions: list[FunctionDefinition]
) -> str:
    """Build an instruction prompt with context about available functions."""
    func_lines = []
    for fn in functions:
        params = ", ".join(
            f"{k}: {v.type}" for k, v in fn.parameters.items()
        )
        func_lines.append(f"- {fn.name}({params}): {fn.description}")

    return (
        "You are a function-calling assistant.\n"
        "Your task is to analyze the user request and call exactly "
        "one function with the correct parameters.\n"
        "Output ONLY valid JSON. Do not explain, do not add fields, "
        "do not invent values.\n\n"

        "OUTPUT FORMAT (strict):\n"
        "{\n"
        '  "name": "<function_name>",\n'
        '  "parameters": { <key>: <value>, ... }\n'
        "}\n\n"

        "PARAMETER EXTRACTION RULES:\n"
        "- String parameters: extract text as-is, "
        "do NOT include surrounding quotes in the value\n"
        "- Number parameters: copy exactly as written, "
        "preserve all digits and decimal points\n"
        "- Negative numbers MUST include the leading '-' character, "
        "do not drop it\n"
        "- Empty values: output empty string \"\" or 0 "
        "depending on parameter type\n"
        "- Only use information explicitly stated in the user request\n"
        "- Never invent, guess, or assume parameter values\n"
        "- Match parameter names exactly as defined in the function "
        "signature\n\n"

        "User: Call function with parameter x = -5\n"
        "Output:\n"
        "{\n"
        '  "name": "some_function",\n'
        '  "parameters": {"x": -5}\n'
        "}\n\n"

        "EXTRACTION EXAMPLES:\n"
        "User: Call function with parameter text = 'hello world'\n"
        "Output:\n"
        "{\n"
        '  "name": "some_function",\n'
        '  "parameters": {"text": "hello world"}\n'
        "}\n\n"

        "User: Call function with parameters a = 42 and b = 3.14\n"
        "Output:\n"
        "{\n"
        '  "name": "some_function",\n'
        '  "parameters": {"a": 42, "b": 3.14}\n'
        "}\n\n"

        "User: Call function with parameter name = ''\n"
        "Output:\n"
        "{\n"
        '  "name": "some_function",\n'
        '  "parameters": {"name": ""}\n'
        "}\n\n"

        "CRITICAL RULES:\n"
        "1. Output ONLY the JSON object, nothing else\n"
        "2. Do not output explanations, reasoning, or commentary\n"
        "3. String parameter values do NOT include their surrounding quotes\n"
        "4. Number parameters are NOT quoted\n"
        "5. Always match the exact function name and parameter names "
        "from available functions\n"
        "6. If no available function matches the user request, choose "
        '"unknown_function" and use an empty parameters object\n'
        "7. If required information is missing, do not invent it\n\n"

        "Available functions:\n"
        + "\n".join(func_lines)
        + "\n\n"
        + f"User request: {prompt}\n"
        + "Output JSON:\n"
    )


def decode(
    *,
    model: Small_LLM_Model,
    prompt: str,
    functions: list[FunctionDefinition],
    decoder: ConstrainedDecoder | None = None,
) -> dict:
    if decoder is None:
        decoder = ConstrainedDecoder(model, functions)

    instruction = _build_instruction_prompt(prompt, functions)
    input_ids = model.encode(instruction).tolist()[0]
    output_tokens: list[int] = []

    def force(text: str) -> None:
        # use pre-encoded tokens instead of encoding again
        token = decoder.fixed_tokens.get(text)
        if token is None:
            token = model.encode(text).tolist()[0]
        output_tokens.extend(token)
        input_ids.extend(token)

    force("{")
    force('"name"')
    force(": ")
    force('"')

    name_tokens = decoder.generate_function_name(input_ids)
    function_name = model.decode(name_tokens)
    output_tokens.extend(name_tokens)
    input_ids.extend(name_tokens)
    force('"')
    force(", ")
    force('"parameters"')
    force(": ")
    force("{")
    function = decoder.functions_by_name[function_name]
    params: list[str] = list(function.parameters.keys())
    for idx, (param_name, param_spec) in enumerate(
        function.parameters.items()
    ):
        force(f'"{param_name}": ')
        value_tokens = decoder.generate_parameter_value(
            input_ids, param_spec.type, source_text=prompt
        )
        output_tokens.extend(value_tokens)
        input_ids.extend(value_tokens)
        if idx < len(params) - 1:
            force(", ")
    force("}")
    force("}")
    output_str = model.decode(output_tokens)
    print("Output:", output_str)
    return json.loads(output_str)
