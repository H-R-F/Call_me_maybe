"""Command-line interface."""
import sys
from .pipeline import run_pipeline


def get_argument() -> dict:
    """Create the CLI argument parser"""
    arguments: dict[str, str] = {
        "--functions_definition": "data/input/functions_definition.json",
        "--input": "data/input/function_calling_tests.json",
        "--output": "data/output/function_calling_results.json"
    }

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        flag: str = args[i]

        if flag not in arguments:
            sys.exit(f"Unknown Flag: {flag}")

        if i + 1 >= len(args):
            sys.exit(f"Missing value for argument: '{flag}'")

        value: str = args[i+1]
        if value.startswith("--"):
            sys.exit(
                f"Missing value for argument: '{flag}'"
                f" (got '{value}' instead)"
            )

        arguments[flag] = value

        i += 2

    return arguments


def main() -> int:
    """Run the CLI entry point"""
    args = get_argument()
    try:
        run_pipeline(
            functions_definition_path=args["--functions_definition"],
            input_path=args["--input"],
            output_path=args["--output"],
        )
        pass
    except Exception as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 1
    return 0
