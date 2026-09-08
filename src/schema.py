"""Pydantic schemas for inputs and outputs."""

from typing import Any, Literal

from pydantic import BaseModel, Field


ParameterType = Literal[
    "string",
    "number",
    "integer",
    "boolean",
    "object",
    "array",
]


class ParameterSpec(BaseModel):
    """Describes a single parameter or return type"""

    type: ParameterType


class FunctionDefinition(BaseModel):
    """Represents a function definition from the input schema"""

    name: str
    description: str
    parameters: dict[str, ParameterSpec]
    returns: ParameterSpec


class PromptItem(BaseModel):
    """Represents one prompt entry from the input file"""

    prompt: str = Field(min_length=1)


class OutputItem(BaseModel):
    """Represents one output entry in the results file"""

    prompt: str
    name: str
    parameters: dict[str, Any]


UNKNOWN_FUNCTION = FunctionDefinition(
    name="unknown_function",
    description=(
        "Default function when no available function matches "
        "the user request"
    ),
    parameters={},
    returns=ParameterSpec(type="string"),
)
