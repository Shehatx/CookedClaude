import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    file_path = os.path.join(working_directory, file_path)
    valid_target_dir = os.path.commonpath([working_dir_abs, os.path.abspath(file_path)]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        file = open(file_path, 'r')
        file_string = file.read(MAX_CHARS)
        if file.read(1):
            file_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_string
    except Exception as e:
        return f'Error: {e}'


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the content in a file after as a string reading only up to 10000 chars",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the file we want to read it's content",
                },
            },
            "required": ["file_path"],
        },
    },
}