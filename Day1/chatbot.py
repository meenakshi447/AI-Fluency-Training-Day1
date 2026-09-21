import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

model = os.getenv("MODEL")

question = input("Ask a question: ")

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful college assistant."
        },
        {
            "role": "user",
            "content": question
        }
    ]
)

print("\nAssistant:", response.choices[0].message.content)