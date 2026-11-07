import json
from types import SimpleNamespace

from call_function import call_function


def make_tool_call(name, arguments):
    if not isinstance(arguments, str):
        arguments = json.dumps(arguments)
    return SimpleNamespace(
        id="call_1",
        function=SimpleNamespace(name=name, arguments=arguments),
    )


def test_dispatches_to_tool(workdir):
    result = call_function(make_tool_call("get_file_content", {"file_path": "notes.txt"}), str(workdir))
    assert result == {"role": "tool", "tool_call_id": "call_1", "content": "some notes"}


def test_model_cannot_override_working_directory(workdir):
    call = make_tool_call("get_files_info", {"directory": ".", "working_directory": "/"})
    result = call_function(call, str(workdir))
    assert "- notes.txt:" in result["content"]


def test_unknown_function(workdir):
    result = call_function(make_tool_call("delete_everything", {}), str(workdir))
    assert result["content"] == "Error: Unknown function: delete_everything"


def test_invalid_json_arguments(workdir):
    result = call_function(make_tool_call("get_files_info", "{not json"), str(workdir))
    assert result["content"].startswith("Error: Invalid JSON arguments")


def test_bad_arguments(workdir):
    result = call_function(make_tool_call("get_file_content", {"wrong": "x"}), str(workdir))
    assert result["content"].startswith("Error: Bad arguments")
