from functions.run_python_file import run_python_file


def test_runs_file(workdir):
    result = run_python_file(str(workdir), "hello.py")
    assert "STDOUT:\nhello" in result


def test_passes_arguments(workdir):
    assert "hello 3 + 5" in run_python_file(str(workdir), "hello.py", ["3", "+", "5"])


def test_reports_exit_code_and_stderr(workdir):
    result = run_python_file(str(workdir), "fail.py")
    assert "Process exited with code 3" in result
    assert "STDERR:\noops" in result


def test_rejects_path_outside(workdir):
    assert run_python_file(str(workdir), "../main.py").startswith("Error: Cannot execute")


def test_missing_file(workdir):
    assert "does not exist" in run_python_file(str(workdir), "nonexistent.py")


def test_rejects_non_python_file(workdir):
    assert "is not a Python file" in run_python_file(str(workdir), "notes.txt")


def test_times_out(workdir, monkeypatch):
    import functions.run_python_file as module

    monkeypatch.setattr(module, "RUN_TIMEOUT_SECONDS", 1)
    (workdir / "slow.py").write_text("import time\ntime.sleep(5)\n")
    assert "timed out" in run_python_file(str(workdir), "slow.py")
