import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from config import DEFAULT_MAX_ITERATIONS, DEFAULT_MODEL, DEFAULT_WORKING_DIRECTORY
from prompts import system_prompt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CookedClaude: an AI coding agent that works inside a sandboxed directory."
    )
    parser.add_argument("prompt", help="What you want the agent to do")
    parser.add_argument(
        "--workdir",
        default=DEFAULT_WORKING_DIRECTORY,
        help=f"Directory the agent is allowed to work in (default: {DEFAULT_WORKING_DIRECTORY})",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=DEFAULT_MAX_ITERATIONS,
        help=f"Maximum number of model calls before giving up (default: {DEFAULT_MAX_ITERATIONS})",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print tool arguments, tool results, and token usage",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not os.path.isdir(args.workdir):
        print(f'Error: working directory "{args.workdir}" does not exist', file=sys.stderr)
        return 1

    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY is not set. Add it to a .env file.", file=sys.stderr)
        return 1

    client = OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Working directory: {os.path.abspath(args.workdir)}\n")

    for _ in range(args.max_iterations):
        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            tools=available_functions,
            reasoning_effort="none",
        )
        message = response.choices[0].message
        messages.append(message)

        if args.verbose and response.usage:
            print(
                f"[tokens] prompt={response.usage.prompt_tokens} "
                f"response={response.usage.completion_tokens}"
            )

        # No tool calls means the model is done and has given its final answer.
        if not message.tool_calls:
            print(f"\nFinal response:\n{message.content or '(no text returned)'}")
            return 0

        for tool_call in message.tool_calls:
            result = call_function(tool_call, args.workdir, verbose=args.verbose)
            if args.verbose:
                print(f"   -> {result['content']}")
            messages.append(result)

    print(
        f"Error: stopped after {args.max_iterations} iterations without a final response",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
