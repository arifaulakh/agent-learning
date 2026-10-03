"""
Day 2 — multiple tools.

Run: uv run python main.py
"""

import json
import os
import sys

from anthropic import Anthropic
from dotenv import load_dotenv

from tools import TOOLS

load_dotenv()

MAX_TURNS = 5

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.
Use tools when you need factual data you don't have.
For math, use the calculate tool."""

TIME_TOOL_SCHEMA = {
    "name": "get_current_time",
    "description": "Get the current UTC time. Return the time in the format YYYY-MM-DD HH:MM:SS. Milliseconds are optional.",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

CALCULATE_TOOL_SCHEMA = {
    "name": "calculate",
    "description": "Use when the user asks for a numeric calculation. Use this tool for any math-related questions.",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "A math expression to evaluate. Only allow: digits, whitespace, + - * / ( ) .",
            },
        },
        "required": ["expression"],
    },
}

TOOL_SCHEMAS = [
    TIME_TOOL_SCHEMA,
    CALCULATE_TOOL_SCHEMA,
]


def call_llm(messages: list[dict], tools: list[dict]) -> dict:
    """Call the model. Return the raw response message."""
    client = Anthropic()
    message = client.messages.create(
        model="claude-opus-5",
        messages=messages,
        tools=tools,
        system=SYSTEM_PROMPT,
        max_tokens=1024,
    )
    return message


def run_tool(name: str, arguments: str) -> str:
    """Execute a tool by name and return string result."""
    if name not in TOOLS:
        return json.dumps({"error": f"Unknown tool: {name}"})
    args = json.loads(arguments) if arguments else {}
    result = TOOLS[name](**args)
    return str(result)


def agent_loop(user_input: str) -> None:
    """Agent loop — same as Day 1, now with multiple tools."""
    messages: list[dict] = [
        {"role": "user", "content": user_input},
    ]

    for turn in range(1, MAX_TURNS + 1):
        print(f"\n--- turn {turn} ---")
        response = call_llm(messages, tools=TOOL_SCHEMAS)
        print(f"Response content: {response.content}")

        tool_calls = [block for block in response.content if block.type == "tool_use"]
        if tool_calls:
            messages.append({"role": "assistant", "content": response.content})
            for tool_call in tool_calls:
                print(f"  tool: {tool_call.name}({tool_call.input})")
                tool_result = run_tool(tool_call.name, json.dumps(tool_call.input))
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_call.id,
                            "content": tool_result,
                        }
                    ],
                })
            continue

        text_blocks = [block for block in response.content if block.type == "text"]
        if text_blocks:
            print(text_blocks[0].text)
        return

    print("Max turns reached.", file=sys.stderr)


def main() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY in .env first.", file=sys.stderr)
        sys.exit(1)

    user_input = input("You: ").strip()
    if not user_input:
        sys.exit(0)

    agent_loop(user_input)


if __name__ == "__main__":
    main()
