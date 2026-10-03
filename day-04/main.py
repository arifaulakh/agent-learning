"""
Day 4 — error handling.

Run: uv run python main.py
"""

import os
import sys

from anthropic import Anthropic
from dotenv import load_dotenv

from tools import TOOLS, ToolResult
from trace import Trace

load_dotenv()

MAX_TURNS = 5

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.
Use tools when you need factual data you don't have.
For math, use the calculate tool.
If a tool returns an error, explain the problem to the user clearly."""

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


def run_tool(name: str, arguments: dict) -> ToolResult:
    """Execute a tool by name. Never raise — always return ToolResult.

    TODO: handle these cases:
      - unknown tool name
      - missing required arguments
      - exceptions inside tool functions
    """
    if name not in TOOLS:
        return ToolResult(
            success=False,
            output="",
            error=f"unknown tool: {name}"
        )
    try:
        result = TOOLS[name](**arguments)
        return ToolResult(
            success=True,
            output=result,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            output="",
            error=str(e)
        )


def agent_loop(user_input: str, trace: Trace) -> None:
    """Agent loop — same as Day 3, with error handling."""
    messages: list[dict] = [
        {"role": "user", "content": user_input},
    ]

    for turn in range(1, MAX_TURNS + 1):
        trace.emit("turn_start", turn=turn)

        response = call_llm(messages, tools=TOOL_SCHEMAS)

        content_types = [block.type for block in response.content]
        trace.emit(
            "llm_response",
            turn=turn,
            stop_reason=response.stop_reason,
            content_types=content_types,
        )

        tool_calls = [block for block in response.content if block.type == "tool_use"]
        if tool_calls:
            messages.append({"role": "assistant", "content": response.content})
            for tool_call in tool_calls:
                trace.emit("tool_call", turn=turn, name=tool_call.name, input=tool_call.input)

                result = run_tool(tool_call.name, tool_call.input)

                trace.emit(
                    "tool_result",
                    turn=turn,
                    name=tool_call.name,
                    result=result.output,
                    success=result.success,
                    error=result.error,
                )

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_call.id,
                            "content": result.for_model()
                        }
                    ],
                })
            continue

        text_blocks = [block for block in response.content if block.type == "text"]
        if text_blocks:
            answer = text_blocks[0].text
            trace.emit("final_answer", turn=turn, text=answer)
            print(f"\nAgent: {answer}")
            trace.emit("done", **trace.summary())
            return

    trace.emit("max_turns",turn=MAX_TURNS)
    print("I wasn't able to finish in time")
    trace.emit("done", **trace.summary())


def main() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY in .env first.", file=sys.stderr)
        sys.exit(1)

    user_input = input("You: ").strip()
    if not user_input:
        sys.exit(0)

    trace = Trace()
    agent_loop(user_input, trace)


if __name__ == "__main__":
    main()
