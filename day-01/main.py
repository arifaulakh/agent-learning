"""
Day 1 — minimal agent loop.

Run: python main.py
"""

import json
import sys
from dotenv import load_dotenv
import os
from anthropic import Anthropic

from tools import TOOLS

load_dotenv()

MAX_TURNS = 5

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.
Use tools when you need factual data you don't have.
For general knowledge or math, answer directly without tools."""



TIME_TOOL_SCHEMA = {
    "name": "get_current_time",
    "description": "Get the current UTC time. Return the time in the format YYYY-MM-DD HH:MM:SS. Milliseconds are optional.",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


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
    """The core agent loop — implement this."""

    messages: list[dict] = [
        {"role": "user", "content": user_input},
    ]

    for turn in range(1, MAX_TURNS + 1):
        print(f"\n--- turn {turn} ---")
        response = call_llm(messages, tools=[TIME_TOOL_SCHEMA])
        print(f"\n--- turn {turn} ---")
        print(f"Response content: {response.content}")
        tool_calls = [content for content in response.content if content.type == "tool_use"]
        if tool_calls:
            messages.append({"role": "assistant", "content": response.content})
            for tool_call in tool_calls:
                tool_name = tool_call.name
                tool_arguments = tool_call.input
                tool_result = run_tool(tool_name, json.dumps(tool_arguments))
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_call.id,
                            "content": tool_result,
                        }
                    ]
                })
            continue
        else:
            print(response.content[0].text)
            return


def main() -> None:
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        print("Set ANTHROPIC_API_KEY first.", file=sys.stderr)
        sys.exit(1)

    user_input = input("You: ").strip()
    if not user_input:
        sys.exit(0)

    agent_loop(user_input)


if __name__ == "__main__":
    main()
