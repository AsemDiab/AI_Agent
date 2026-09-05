import os
from dotenv import load_dotenv
import argparse
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

# Set up argument parser
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()
print(f"User prompt: {args.user_prompt}")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": args.user_prompt
        }
    ],
)

prompt_tokens = response.usage.prompt_tokens
completion_tokens = response.usage.completion_tokens
if prompt_tokens is not None and completion_tokens is not None:
    print(f'Prompt tokens: {prompt_tokens}')
    print(f'Response tokens: {completion_tokens}')
else:
    raise RuntimeError ("Token usage information is not available in the response.")

print(response.choices[0].message.content)