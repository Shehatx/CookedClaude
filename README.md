# CookedClaude

A small AI coding agent built from scratch in Python. You give it a request in plain English. It then decides which tools to call, reads and edits files, runs Python code, and loops until it has an answer.

The agent works inside a sandboxed working directory. Right now that's the bundled [`calculator/`](calculator/) project. It has already added a feature to the calculator and updated the calculator's README by itself.

## How it works

1. Your prompt is sent to the model along with a system prompt and a list of tools it can call.
2. If the model asks for tool calls, the agent runs each one and sends the results back to the model.
3. This repeats until the model replies with plain text and no tool calls, or until it hits the 20-iteration limit.

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
| `write_file` | Creates or overwrites a file |
| `run_python_file` | Runs a `.py` file with optional arguments (30-second timeout) and returns its stdout and stderr |

Every tool checks that the target path stays inside the working directory, so the agent can't read, write, or run anything outside it. The model never picks the working directory itself. [`call_function.py`](call_function.py) adds it to every tool call.

## Project structure

```
.
├── main.py              # CLI entry point and the agent loop
├── call_function.py     # Sends tool calls to the matching Python function
├── prompts.py           # System prompt
├── config.py            # Settings (e.g. MAX_CHARS)
├── functions/           # Tool code and JSON schemas
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── calculator/          # Sandbox project the agent works on
└── test_*.py            # Manual tests for each tool
```

## Setup

You need Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/Shehatx/CookedClaude.git
cd CookedClaude
uv sync
```

Create a `.env` file in the project root with your API key:

```sh
OPENROUTER_API_KEY=your-api-key-here
```

> The client points at `https://api.openai.com/v1` and uses the `gpt-6-luna` model. To use a different provider or model, change `base_url` and `model` in [`main.py`](main.py).

## Usage

```sh
uv run main.py "your prompt here"
```

Examples:

```sh
uv run main.py "what files are in the root?"
uv run main.py "run the calculator tests and tell me if they pass"
uv run main.py "add a modulo operator to the calculator and update its README"
```

Add `--verbose` to also print the tool results and token usage:

```sh
uv run main.py "how does the calculator render results?" --verbose
```

## Running the tool tests

```sh
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_write_file.py
uv run test_run_python_file.py
```

## ⚠️ Safety note

The agent can write files and run Python code inside its working directory. The path checks keep it inside `calculator/`, but any code it runs has the same permissions as your user account. Run it only on projects you're fine with it changing, and don't point it at anything sensitive.
