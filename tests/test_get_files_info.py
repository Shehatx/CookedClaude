from functions.get_files_info import get_files_info


def test_lists_working_directory(workdir):
    result = get_files_info(str(workdir), ".")
    assert "- hello.py:" in result
    assert "- pkg: " in result and "is_dir=True" in result


def test_lists_subdirectory(workdir):
    result = get_files_info(str(workdir), "pkg")
    assert "- module.py:" in result


def test_rejects_absolute_path_outside(workdir):
    assert get_files_info(str(workdir), "/bin").startswith("Error: Cannot list")


def test_rejects_parent_directory(workdir):
    assert get_files_info(str(workdir), "../").startswith("Error: Cannot list")


def test_rejects_file(workdir):
    assert "is not a directory" in get_files_info(str(workdir), "notes.txt")
