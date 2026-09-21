import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import get_course_fee, calculator

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

model = os.getenv("MODEL")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the fee for a course.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

question = "I can pay Rs. 30,000. Which two courses can I take together within this budget?"

messages = [
    {
        "role": "system",
        "content": (
            "You are a college fee assistant. "
            "Available courses are CS101, AI202, and DS303. "
            "Use get_course_fee to find fees. "
            "Use calculator for arithmetic. "
            "Find pairs of two courses whose combined fee is within "
            "the student's budget. Never guess fees."
        )
    },
    {
        "role": "user",
        "content": question
    }
]

for step in range(8):

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        print("\nAgent:", message.content)
        break

    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print(f"\nTool called: {tool_name}")
        print(f"Arguments: {arguments}")

        if tool_name == "get_course_fee":
            result = get_course_fee(arguments["course_code"])

        elif tool_name == "calculator":
            result = calculator(arguments["expression"])

        else:
            result = "Unknown tool"

        print(f"Tool result: {result}")

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            }
        )