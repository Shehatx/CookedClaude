import pytest


@pytest.fixture
def workdir(tmp_path):
    """A small throwaway project for the tools to work on."""
    (tmp_path / "hello.py").write_text('import sys\nprint("hello", *sys.argv[1:])\n')
    (tmp_path / "fail.py").write_text('import sys\nprint("oops", file=sys.stderr)\nsys.exit(3)\n')
    (tmp_path / "notes.txt").write_text("some notes")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "module.py").write_text("x = 1\n")
    return tmp_path
