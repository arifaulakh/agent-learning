# Day 1 — The Agent Loop (from scratch)

**Date:** Sept 2, 2026  
**Time budget:** 60–90 min  
**Rule:** No agent frameworks (LangChain, CrewAI, OpenAI Agents SDK, etc.). Raw API only.

---

## Why start here?

Both Anthropic and OpenAI agree on the same foundation:

1. An **agent** is an LLM + **tools** + a **loop** that keeps going until the task is done.
2. You should understand that loop yourself before using a framework.
3. Start with **one agent**, **one tool**, **one task**.

Anthropic calls this the "augmented LLM." OpenAI calls it the "agent loop" (model → tool call → execute → feed result back → repeat).

---

## Today's goal

Build a CLI program that:

1. Takes a user question from the terminal.
2. Sends it to an LLM with **one tool** available: `get_current_time`.
3. If the model requests the tool, **you** run it locally and send the result back.
4. Repeats until the model returns a final text answer (no more tool calls).
5. Prints the answer.

Example session:

```
You: What time is it in UTC?
Agent: The current UTC time is 2026-09-03T04:30:00Z.
```

---

## What you'll learn

- The **messages array** (system / user / assistant / tool roles)
- **Tool schemas** (name, description, parameters as JSON Schema)
- **Tool call parsing** from the model response
- The **while loop** that makes an agent an agent

---

## Constraints

- Python 3.11+ (or TypeScript if you prefer — but pick one language for the whole journey).
- Use **one** provider: OpenAI *or* Anthropic (either is fine for Day 1).
- Max **5 turns** in the loop (safety rail).
- Log each turn to stdout so you can see what happened.

---

## Files to implement

```
day-01/
├── README.md          ← you are here
├── main.py            ← entry point + agent loop (TODO)
└── tools.py           ← get_current_time implementation (TODO)

Dependencies are in the repo root: ../pyproject.toml (managed with uv)
```

---

## Step-by-step (do in order)

### 1. Set up (10 min)

From the repo root (first time only):

```bash
uv sync
cp .env.example .env   # add OPENAI_API_KEY (or ANTHROPIC_API_KEY)
```

Then run today's exercise:

```bash
cd day-01
uv run python main.py
```

### 2. Implement the tool (10 min)

In `tools.py`, write `get_current_time() -> str` that returns ISO-8601 UTC time.

Register it in a dict: `TOOLS = {"get_current_time": get_current_time}`.

### 3. Define the tool schema (10 min)

The model needs a JSON-schema description of your tool. Look up **function calling** / **tool use** for your provider:

- OpenAI: https://platform.openai.com/docs/guides/function-calling
- Anthropic: https://docs.anthropic.com/en/docs/build-with-claude/tool-use

Write the schema for `get_current_time` (no parameters needed).

### 4. Build the loop (30 min) — the core exercise

Pseudocode:

```
messages = [system_prompt, user_message]

while turn < MAX_TURNS:
    response = call_llm(messages, tools=[time_tool_schema])

    if response has tool_calls:
        append assistant message with tool_calls to messages
        for each tool_call:
            result = TOOLS[name](**args)
            append tool result message to messages
        continue

    else:
        print(response.text)
        break
```

**You must implement this yourself.** The stubs in `main.py` are intentionally incomplete.

### 5. Test (10 min)

Try these prompts:

| Prompt | Expected behavior |
|--------|-------------------|
| "What time is it?" | Calls tool, returns time |
| "Hello!" | No tool call, just replies |
| "What is 2+2?" | No tool call, just replies |

### 6. Reflect (5 min)

Answer in a new file `day-01/notes.md`:

1. What did the messages array look like after a tool call?
2. What would break if you forgot to append the tool result?
3. Why is `max_turns` important?

---

## Self-check (done when all true)

- [X] Loop runs without a framework
- [X] Tool is only called when needed
- [X] You can explain each message in the transcript
- [X] Loop stops on final answer or max turns
- [ ] `notes.md` written

---

## Tomorrow (Day 2 preview)

Add a second tool (`calculate`) and handle **multiple tool calls in one turn**. Same loop — slightly richer tool routing.

---

## References

- Anthropic: [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — start with augmented LLM, add complexity only when needed
- OpenAI: [Running agents](https://openai.github.io/openai-agents-python/running_agents/) — read *after* today to compare your loop to theirs
