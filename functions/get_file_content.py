import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    valid_target_dir = os.path.commonpath([working_dir_abs, file_path]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        file = open(file_path, 'r')
        file_string = file.read(MAX_CHARS)
        if file.read(MAX_CHARS + 1):
            file_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        print(f'Error: {e}')