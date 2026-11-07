# CookedClaude

A small AI coding agent built from scratch in Python, with no agent framework. You give it a request in plain English. It then decides which tools to call, reads and edits files, runs Python code, and loops until it has an answer.

The agent can only work inside one working directory, which you choose. By default that's the bundled [`calculator/`](calculator/) project. The agent has already added a feature to the calculator (the `^` exponent operator) and updated the calculator's README by itself.

## Demo

```
$ uv run main.py "List the files in the root, then run main.py with the argument '2 ^ 3' and tell me the result. Don't modify any files." --verbose

 - Calling function: get_files_info({'directory': '.'})
   -> - README.md: file_size=1583 bytes, is_dir=False
      - main.py: file_size=748 bytes, is_dir=False
      ...
 - Calling function: run_python_file({'file_path': 'main.py', 'args': ['2 ^ 3']})
   -> STDOUT:
      { "expression": "2 ^ 3", "result": 8 }

Final response:
Root files: `README.md`, `lorem.txt`, `main.py`, and `tests.py`. There are also directories `__pycache__` and `pkg`.

Running `main.py` with `2 ^ 3` returned **8**. No files were modified.
```

## How it works

1. Your prompt is sent to the model along with a system prompt and a list of tools it can call.
2. If the model asks for tool calls, the agent runs each one and sends the results back to the model.
3. This repeats until the model replies with plain text and no tool calls, or until it hits the iteration limit.

```
user prompt ──► LLM ──► tool calls? ──yes──► run tools ──► results back to LLM ──┐
                 ▲                                                               │
                 └───────────────────────────────────────────────────────────────┘
                              no ──► print final response
```

## Tools

| Tool | What it does |
| --- | --- |
| `get_files_info` | Lists the files in a directory, with each file's size and whether it's a directory |
| `get_file_content` | Reads a file's contents (truncated after 10,000 characters) |
| `write_file` | Creates or overwrites a file, creating parent folders if needed |
| `run_python_file` | Runs a `.py` file with optional arguments (30-second timeout) and returns its stdout, stderr and exit code |

## Safety

- **Locked to the working directory.** Every tool checks that the target path stays inside the working directory, so `../` and absolute paths like `/etc/passwd` are rejected. The model never picks the working directory itself. [`call_function.py`](call_function.py) adds it to every tool call and ignores any value the model tries to send.
- **Limits.** Scripts the agent runs are stopped after 30 seconds, file reads are cut off at 10,000 characters, and the agent stops after 20 iterations by default.
- **Errors go back to the model.** Unknown tools, invalid JSON arguments and wrong parameters come back to the model as error messages instead of crashing the agent, so it can correct itself.

> ⚠️ These checks limit where the agent can read and write files, but any Python it runs has the same permissions as your user account. Only point it at projects you're fine with it changing.

## Project structure

```
.
├── main.py              # CLI entry point and the agent loop
├── call_function.py     # Sends tool calls to the matching Python function
├── prompts.py           # System prompt
├── config.py            # Limits and defaults (MAX_CHARS, timeout, model, ...)
├── functions/           # Tool code and the JSON schemas sent to the model
│   ├── path_utils.py    # Shared check that keeps paths inside the working directory
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── tests/               # pytest tests for every tool and the dispatcher
└── calculator/          # Sample project the agent works on by default
```

## Setup

You need Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/Shehatx/CookedClaude.git
cd CookedClaude
uv sync
cp .env.example .env   # then add your OpenAI API key
```

## Usage

```sh
uv run main.py "your prompt here"
```

| Option | Default | Description |
| --- | --- | --- |
| `--workdir PATH` | `./calculator` | Directory the agent is allowed to work in |
| `--model NAME` | `gpt-6-luna` | Model to use |
| `--max-iterations N` | `20` | Maximum number of model calls before giving up |
| `--verbose` | off | Print tool arguments, tool results and token usage |

Examples:

```sh
uv run main.py "run the calculator tests and tell me if they pass"
uv run main.py "add a modulo operator to the calculator and update its README"
uv run main.py "explain what this project does" --workdir ../some-other-project
```

## Tests

```sh
uv run pytest
```

The tests run each tool against a temporary directory, so they never touch `calculator/`. They cover normal use, attempts to escape the working directory, timeouts, and bad input from the model.
