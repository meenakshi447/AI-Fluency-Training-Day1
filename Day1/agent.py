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
            "description": "Get the fee for a course using its course code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101, AI202, or DS303."
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
                        "type": "string",
                        "description": "Mathematical expression to calculate."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


def run_tool(name, arguments):
    if name == "get_course_fee":
        return get_course_fee(arguments["course_code"])

    if name == "calculator":
        return calculator(arguments["expression"])

    return "Unknown tool"


question = input("Ask a question: ")

messages = [
    {
        "role": "system",
        "content": (
            "You are a college fee assistant. "
            "Never guess course fees. "
            "Use get_course_fee when you need a course fee. "
            "Use calculator for arithmetic. "
            "Available courses are CS101, AI202, and DS303."
        )
    },
    {
        "role": "user",
        "content": question
    }
]


for step in range(5):

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

        result = run_tool(tool_name, arguments)

        print(f"Tool result: {result}")

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            }
        )

else:
    print("Agent stopped after maximum steps.")