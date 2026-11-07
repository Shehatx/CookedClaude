from functions.write_file import write_file


def test_overwrites_file(workdir):
    result = write_file(str(workdir), "notes.txt", "new notes")
    assert result.startswith("Successfully wrote")
    assert (workdir / "notes.txt").read_text() == "new notes"


def test_creates_nested_directories(workdir):
    write_file(str(workdir), "new/dir/file.txt", "hi")
    assert (workdir / "new" / "dir" / "file.txt").read_text() == "hi"


def test_rejects_path_outside(workdir, tmp_path_factory):
    outside = tmp_path_factory.mktemp("outside") / "escape.txt"
    result = write_file(str(workdir), str(outside), "should not be written")
    assert result.startswith("Error: Cannot write")
    assert not outside.exists()


def test_rejects_parent_directory(workdir):
    assert write_file(str(workdir), "../escape.txt", "x").startswith("Error: Cannot write")


def test_rejects_directory(workdir):
    assert "is a directory" in write_file(str(workdir), "pkg", "x")
