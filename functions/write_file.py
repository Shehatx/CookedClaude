import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    file_path = os.path.join(working_directory, file_path)
    valid_target_dir = os.path.commonpath([working_dir_abs, os.path.abspath(file_path)]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        opened_file = open(file_path, 'w')
        opened_file = content
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file given the file_path and the content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the file we want to write content to",
                },
                "content": {
                    "type": "string",
                    "description": "The content we would like to write to the file",
                },             
            },
            "required": ["file_path", "content"],
        },
    },
}