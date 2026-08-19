*This project has been created as part of the 42 curriculum by aben-sab.*

# Call Me Maybe

## Description
This project implements a function calling engine that maps natural language prompts
to structured function calls. It selects the correct function name using the provided
LLM SDK and extracts parameters while enforcing JSON-valid output.

## Instructions
### Setup
```bash
uv sync
```

Note: the provided `llm_sdk` imports `torch` and `transformers`, but the subject
forbids adding them as dependencies. If local runs fail with missing modules,
install them manually in your environment without editing `pyproject.toml`.

### Run
```bash
uv run python -m src \
	--functions_definition data/input/functions_definition.json \
	--input data/input/function_calling_tests.json \
	--output data/output/function_calling_results.json
```

## Resources
- https://github.com/astral-sh/uv
- https://docs.pydantic.dev/
- https://numpy.org/
- https://docs.python.org/3/library/json.html

AI usage: I used AI assistance to review requirements, explain design choices,
and iterate on decoding and parameter extraction strategies. All final code
was validated and adjusted manually.

## Algorithm explanation
1. **Function selection**: the model is prompted with the user request and the
	 function list. A token-trie constrained decoding step selects a valid function
	 name by only allowing tokens that match a real function name.
2. **Parameter extraction**: parameters are extracted deterministically from the
	 request (numbers by position, quoted strings by pattern) to guarantee speed
	 and JSON validity while respecting the required schema.
3. **Output formatting**: each result is written as a JSON object with keys
	 `prompt`, `name`, and `parameters`.

## Design decisions
- The LLM is used only for **function selection**, which is explicitly required.
- Parameter extraction is deterministic to reduce latency and avoid malformed
	output, while still respecting the schema types.
- The implementation avoids any forbidden libraries and uses only the SDK
	interface for LLM access.

## Performance analysis
The pipeline runs within the 5-minute limit on CPU by limiting LLM usage to
function selection. Parameter extraction runs in linear time over the prompt.

## Challenges faced
- Balancing strict JSON validity with reliable extraction. This was solved by
	using deterministic parsing for parameters and a constrained trie for function
	names.

## Testing strategy
- Run the pipeline on the provided input files and manually verify the output.
- Try edge cases: empty strings, multiple numbers, and quoted strings.

## Example usage
```bash
uv run python -m src
```
# Call_me_maybe
