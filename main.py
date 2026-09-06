from email.mime import message
import json
import os
from dotenv import load_dotenv
import argparse
from openai import OpenAI
from prompts import system_prompt 
from call_function import available_functions, call_function
print("Starting the chatbot...",system_prompt)
# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

# Set up argument parser
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
if args.verbose:
    print(f"User prompt: {args.user_prompt}")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
def generate_content(client, messages, verbose=False):
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        if verbose:
            if prompt_tokens is not None and completion_tokens is not None:
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {completion_tokens}")
            else:
                raise RuntimeError(
                    "Token usage information is not available in the response."
                )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(f"Final response:\n{message.content}")
            return

        for tool_call in message.tool_calls:
            result_message = call_function(
                tool_call,
                verbose=verbose,
            )
            if not result_message.get("content"):
                raise Exception("Tool call returned empty content")

            messages.append(result_message)

            if verbose:
                print(f"-> {result_message['content']}")

    print("Agent stopped after reaching the maximum number of iterations.")
    raise SystemExit(1)

generate_content(client, messages, verbose=args.verbose)