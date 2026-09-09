"""Pydantic schemas for inputs and outputs."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, create_model


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


def validate_function_parameters(
    function: FunctionDefinition,
    parameters: dict[str, Any],
) -> dict[str, Any]:
    """Validate generated arguments against a function definition."""
    python_types: dict[ParameterType, type[Any]] = {
        "string": str,
        "number": float,
        "integer": int,
        "boolean": bool,
        "object": dict,
        "array": list,
    }
    fields = {
        name: (python_types[spec.type], ...)
        for name, spec in function.parameters.items()
    }
    parameter_model = create_model(
        f"{function.name}Parameters",
        __config__=ConfigDict(extra="forbid"),
        **fields,
    )
    return parameter_model.model_validate(parameters).model_dump()


UNKNOWN_FUNCTION = FunctionDefinition(
    name="unknown_function",
    description=(
        "Default function when no available function matches "
        "the user request"
    ),
    parameters={},
    returns=ParameterSpec(type="string"),
)
