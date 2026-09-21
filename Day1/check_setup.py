import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

model = os.getenv("MODEL")

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": "Reply with exactly: SETUP OK"}
    ]
)

print(response.choices[0].message.content)