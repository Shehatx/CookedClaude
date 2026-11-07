import os

from functions.path_utils import resolve_in_working_directory


def get_files_info(working_directory: str, directory: str = ".") -> str:
    target_dir = resolve_in_working_directory(working_directory, directory)
    if target_dir is None:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        lines = []
        for item in sorted(os.listdir(target_dir)):
            item_path = os.path.join(target_dir, item)
            lines.append(
                f"- {item}: file_size={os.path.getsize(item_path)} bytes, "
                f"is_dir={os.path.isdir(item_path)}"
            )
        return "\n".join(lines)
    except OSError as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a directory relative to the working directory, with each file's size and whether it is a directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": 'Directory to list, relative to the working directory. Use "." for the working directory itself.',
                },
            },
            "required": ["directory"],
        },
    },
}
