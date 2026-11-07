import json
from collections.abc import Callable

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

# Tool name -> Python function that implements it.
function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

# JSON schemas sent to the model so it knows which tools exist.
available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]


def call_function(tool_call, working_directory: str, verbose: bool = False) -> dict:
    """Run one tool call from the model and return the message to send back."""
    function_name = tool_call.function.name

    def tool_result(content: str) -> dict:
        return {"role": "tool", "tool_call_id": tool_call.id, "content": content}

    try:
        function_args = json.loads(tool_call.function.arguments or "{}")
    except json.JSONDecodeError as e:
        return tool_result(f"Error: Invalid JSON arguments for {function_name}: {e}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function = function_map.get(function_name)
    if function is None:
        return tool_result(f"Error: Unknown function: {function_name}")

    # The working directory is always set by us, never by the model.
    function_args.pop("working_directory", None)
    try:
        result = function(working_directory=working_directory, **function_args)
    except TypeError as e:
        # The model passed arguments that don't match the function signature.
        result = f"Error: Bad arguments for {function_name}: {e}"

    return tool_result(result)
