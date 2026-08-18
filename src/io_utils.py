"""I/O helpers for JSON files."""

import json
from pathlib import Path
from typing import Any, Iterable, TypeVar, cast

from pydantic import BaseModel

from .schema import FunctionDefinition, OutputItem, PromptItem

ModelT = TypeVar("ModelT", bound=BaseModel)


def _validate_model(model_type: type[ModelT], data: Any) -> ModelT:
    """Validate arbitrary data into a Pydantic model"""
    return cast(ModelT,model_type.model_validate(data))


def load_json_file(path: str) -> Any:
    """Load JSON content from a file and return raw data"""
    try:
        with open(path, "r") as f:
            raw_text = f.read()
            print(raw_text)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f'Input file not found: "{path}"') from exc
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f'Invalid JSON in file: "{path}"') from exc


def load_function_definitions(path: str) -> list[FunctionDefinition]:
    """Load and validate function definitions from JSON"""
    data = load_json_file(path)
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError(
            f'"{path}" must contain a JSON array'
        )
    return [_validate_model(FunctionDefinition, item) for item in data]


def load_prompts(path: str) -> list[PromptItem]:
    """Load and validate prompt items from JSON"""
    data = load_json_file(path)
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError(
            f'"{path}" must contain a JSON array'
        )
    return [_validate_model(PromptItem, item) for item in data]


def write_output(path: str, items: Iterable[OutputItem]) -> None:
    """Write validated output items to a JSON file"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [item.model_dump() for item in items]
    content = json.dumps(payload, indent=2)
    file_path.write_text(content)
