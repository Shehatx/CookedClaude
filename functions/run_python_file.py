import os, subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        valid_target_dir = os.path.commonpath([working_dir_abs, os.path.abspath(os.path.join(working_directory, file_path))]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(os.path.join(working_directory, file_path)):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", os.path.abspath(os.path.join(working_directory, file_path))]
        if args:
            command.extend(args)
        output = subprocess.run(command, timeout=30, text=True, capture_output=True, cwd= working_dir_abs)
        output_string = ""
        if output.returncode != 0:
            output_string += f"Process exited with code {output.returncode}\n"
        if not output.stderr and not output.stdout:
            output_string += f"No output produced\n"
        if output.stderr:
            output_string += f"STDERR: {output.stderr}"
        if output.stdout:
            output_string += f"STDOUT: {output.stdout}"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"