import json
from pathlib import Path
from typing import Any, Iterable

from .schema import FunctionDefinition, OutputItem, PromptItem


def load_json_file(path: str) -> Any:
    """Load JSON content from a file and return raw data"""
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError as exc:
        raise FileNotFoundError(f'Input file not found: "{path}"') from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f'Invalid JSON in file: "{path}"') from exc


def load_function_definitions(path: str) -> list[FunctionDefinition]:
    """Load and validate function definitions from JSON"""
    data = load_json_file(path)
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError(
            f'"{path}" must contain a JSON array'
        )
    functions: list[FunctionDefinition] = []
    for item in data:
        try:
            functions.append(FunctionDefinition.model_validate(item))
        except ValueError as exc:
            raise ValueError(
                f'Invalid data in input file: "{path}": {exc}'
            ) from exc
    return functions


def load_prompts(path: str) -> list[PromptItem]:
    """Load and validate prompt items from JSON"""
    data = load_json_file(path)
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError(
            f'"{path}" must contain a JSON array'
        )
    prompts: list[PromptItem] = []
    for item in data:
        try:
            prompts.append(PromptItem.model_validate(item))
        except ValueError as exc:
            raise ValueError(
                f'Invalid data in input file: "{path}": {exc}'
            ) from exc
    return prompts


def write_output(path: str, items: Iterable[OutputItem]) -> None:
    """Write validated output items to a JSON file"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [item.model_dump() for item in items]
    content = json.dumps(payload, indent=2)
    file_path.write_text(content)
