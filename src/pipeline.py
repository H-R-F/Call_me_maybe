"""Generation pipeline"""

from typing import Any

from llm_sdk import Small_LLM_Model

from .decoder import ConstrainedDecoder, decode
from .io_utils import load_function_definitions, load_prompts, write_output
from .schema import UNKNOWN_FUNCTION, OutputItem


def _function_matches_prompt(
    prompt: str, functions: list
) -> str | None:
    """Check if prompt keywords match any function description.

    Returns the function name if a match is found, None otherwise.
    """
    prompt_lower = prompt.lower()
    best_match = None
    best_score = 0

    for fn in functions:
        if fn.name == UNKNOWN_FUNCTION.name:
            continue
        desc_words = set(fn.description.lower().split())
        prompt_words = set(prompt_lower.split())
        overlap = len(desc_words & prompt_words)
        if overlap > best_score:
            best_score = overlap
            best_match = fn.name

    return best_match if best_score > 0 else None


def run_pipeline(
    *,
    functions_definition_path: str,
    input_path: str,
    output_path: str,
) -> list[dict[str, Any]]:
    """Run the end-to-end generation pipeline"""
    functions = load_function_definitions(functions_definition_path)
    functions.append(UNKNOWN_FUNCTION)
    prompts = load_prompts(input_path)
    model = Small_LLM_Model()
    decoder = ConstrainedDecoder(model, functions)
    outputs: list[OutputItem] = []

    for item in prompts:
        matched = _function_matches_prompt(item.prompt, functions)
        if matched is None:
            outputs.append(
                OutputItem(
                    prompt=item.prompt,
                    name=UNKNOWN_FUNCTION.name,
                    parameters={},
                )
            )
            continue

        decoded = decode(
            model=model,
            prompt=item.prompt,
            functions=functions,
            decoder=decoder,
        )
        outputs.append(
            OutputItem(
                prompt=item.prompt,
                name=decoded["name"],
                parameters=decoded["parameters"],
            )
        )

    write_output(output_path, outputs)
    return [item.model_dump() for item in outputs]
