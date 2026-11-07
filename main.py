import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if api_key == None:
    raise RuntimeError("Unable to fetch API Key")

client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key=api_key,
)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt_text", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
prompt_text = args.prompt_text

messages = [

    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.prompt_text},
]

for _ in range(20):
    response = client.chat.completions.create(
        model="gpt-6-luna",
        messages=messages,
        tools=available_functions,
        reasoning_effort="none",
    )

    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call=tool_call, verbose=args.verbose)
            function_args = json.loads(tool_call.function.arguments or "{}")
            if result_message["content"] == None:
                raise Exception()
            if args.verbose:
                print(f"-> {result_message['content']}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
            messages.append(result_message)
    else:
        if args.verbose:
            print(f"User prompt: {prompt_text}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            if response.choices[0].message.content:
                print(f"Response: {response.choices[0].message.content}")
        else:
            if response.choices[0].message.content:
                print(f"Response: {response.choices[0].message.content}")
        break
else:
    print("Limit reached with no final response")
    exit(1)
