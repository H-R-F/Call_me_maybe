from typing import Any

from llm_sdk import Small_LLM_Model

from .decoder import ConstrainedDecoder, decode
from .io_utils import load_function_definitions, load_prompts, write_output
from .schema import UNKNOWN_FUNCTION, OutputItem


def run_pipeline(
    *,
    functions_definition_path: str,
    input_path: str,
    output_path: str,
) -> None:
    """Run the end-to-end generation pipeline"""
    functions = load_function_definitions(functions_definition_path)
    functions.append(UNKNOWN_FUNCTION)
    prompts = load_prompts(input_path)
    model = Small_LLM_Model()
    decoder = ConstrainedDecoder(model, functions)
    outputs: list[OutputItem] = []

    for item in prompts:
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