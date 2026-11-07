import os
import subprocess
import sys

from config import RUN_TIMEOUT_SECONDS
from functions.path_utils import resolve_in_working_directory


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    target = resolve_in_working_directory(working_directory, file_path)
    if target is None:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    # sys.executable is the interpreter running the agent, so this works
    # even on systems where there is no plain `python` command.
    command = [sys.executable, target, *(args or [])]
    try:
        result = subprocess.run(
            command,
            cwd=os.path.abspath(working_directory),
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return f'Error: "{file_path}" timed out after {RUN_TIMEOUT_SECONDS} seconds'
    except OSError as e:
        return f"Error: executing Python file: {e}"

    output = []
    if result.returncode != 0:
        output.append(f"Process exited with code {result.returncode}")
    if result.stdout:
        output.append(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        output.append(f"STDERR:\n{result.stderr}")
    if not result.stdout and not result.stderr:
        output.append("No output produced")
    return "\n".join(output)


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": f"Runs a Python file with optional command-line arguments and returns its output. Stops after {RUN_TIMEOUT_SECONDS} seconds.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the .py file, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the script.",
                },
            },
            "required": ["file_path"],
        },
    },
}
