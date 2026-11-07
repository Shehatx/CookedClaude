from config import MAX_CHARS
from functions.get_file_content import get_file_content


def test_reads_file(workdir):
    assert get_file_content(str(workdir), "notes.txt") == "some notes"


def test_reads_nested_file(workdir):
    assert get_file_content(str(workdir), "pkg/module.py") == "x = 1\n"


def test_truncates_long_file(workdir):
    (workdir / "big.txt").write_text("a" * (MAX_CHARS + 100))
    result = get_file_content(str(workdir), "big.txt")
    assert result.startswith("a" * MAX_CHARS)
    assert f"truncated at {MAX_CHARS} characters" in result


def test_rejects_path_outside(workdir):
    assert get_file_content(str(workdir), "/bin/cat").startswith("Error: Cannot read")
    assert get_file_content(str(workdir), "../secret.txt").startswith("Error: Cannot read")


def test_missing_file(workdir):
    assert "File not found" in get_file_content(str(workdir), "pkg/does_not_exist.py")
