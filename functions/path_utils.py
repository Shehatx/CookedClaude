import os


def resolve_in_working_directory(working_directory: str, path: str) -> str | None:
    """Return the absolute path of `path` inside `working_directory`.

    Returns None if the path would escape the working directory
    (e.g. "../secrets.txt" or "/etc/passwd").
    """
    working_dir_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_dir_abs, path))
    if os.path.commonpath([working_dir_abs, target]) != working_dir_abs:
        return None
    return target
