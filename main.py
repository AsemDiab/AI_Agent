import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ],
)

prompt_tokens = response.usage.prompt_tokens
completion_tokens = response.usage.completion_tokens
if prompt_tokens is not None and completion_tokens is not None:
    print(f'Prompt tokens: {prompt_tokens}')
    print(f'Response tokens: {completion_tokens}')
else:
    raise ValueError("Token usage information is not available in the response.")

print(response.choices[0].message.content)