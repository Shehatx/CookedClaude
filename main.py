import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("Unable to fetch API Key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt_text", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
prompt_text = args.prompt_text

messages = [
    {"role": "user", "content": args.prompt_text},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
)

if args.verbose:
    print(f"User prompt: {prompt_text}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print(f"Response: {response.choices[0].message.content}")
else:
    print(f"Response: {response.choices[0].message.content}")
