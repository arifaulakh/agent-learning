# Day 2 — Multiple Tools

**Date:** Sept 4, 2026  
**Time budget:** 60–90 min  
**Rule:** Still no agent frameworks. Extend your Day 1 loop.

---

## Start here

Day 2 is a **copy of your Day 1 code**, not a rewrite. Each day folder is its own snapshot so you can diff them later:

```bash
diff -u day-01/main.py day-02/main.py
```

If Day 1 isn't working yet, finish that first — Day 2 builds on the same loop.

---

## Today's goal

Extend the agent with a second tool: `calculate`.

1. Pass **both** tool schemas to the LLM on every turn.
2. Implement `calculate(expression: str) -> str` in `tools.py`.
3. Design the `calculate` schema (this one has **parameters** — new skill).
4. Handle cases where the model calls **zero, one, or multiple** tools in a single turn.

Your Day 1 loop already loops over `tool_calls` — that's the right pattern. Today you stress-test it with richer routing.

---



## What you'll learn

- Designing schemas **with parameters** (name, type, description per field)
- Tool routing: model picks the right tool (or none) from a set
- Multiple `tool_use` blocks in one assistant message
- Keeping schema and Python function signatures in sync

---



## Files to change

```
day-02/
├── README.md       ← you are here
├── main.py         ← add CALCULATE_TOOL_SCHEMA, pass both tools
└── tools.py        ← implement calculate, register in TOOLS
```

---



## Step-by-step



### 1. Run Day 1 baseline (5 min)

```bash
cd day-02
uv run python main.py
```

Confirm time queries still work before adding anything new.

### 2. Implement `calculate` (15 min)

In `tools.py`, implement:

```python
def calculate(expression: str) -> str:
    """Evaluate a math expression and return the result as a string."""
```

**Constraint:** only allow digits, whitespace, and `+ - * / ( ) .` — reject anything else.

Hint: parse with Python's `ast` module instead of bare `eval()`. See [safe arithmetic eval patterns](https://docs.python.org/3/library/ast.html#ast.literal_eval) — you'll need a small walker for operators (literal_eval alone won't handle `2 + 2`).

Register it in `TOOLS`.

### 3. Design the `calculate` schema (15 min)

Fill in `CALCULATE_TOOL_SCHEMA` in `main.py`. Think about:


| Field              | Your design choice               |
| ------------------ | -------------------------------- |
| `name`             | Must match `TOOLS` key           |
| `description`      | When to use vs doing mental math |
| `expression` param | Type, description, required?     |


Compare to `TIME_TOOL_SCHEMA` — same structure, but now `properties` is non-empty.

### 4. Wire both tools into the loop (10 min)

Change:

```python
tools=[TIME_TOOL_SCHEMA]
```

to pass both schemas. Everything else in the loop stays the same.

### 5. Update the system prompt (5 min)

Your Day 1 prompt says "answer math directly without tools." That conflicts with Day 2. Revise it so the model knows:

- Use `get_current_time` for current time
- Use `calculate` for non-trivial math (or all math — pick a policy and test it)
- Use neither for greetings / general chat



### 6. Test (15 min)


| Prompt                                 | Expected                |
| -------------------------------------- | ----------------------- |
| "What time is it?"                     | `get_current_time` only |
| "What is 847 * 293?"                   | `calculate` only        |
| "Hello!"                               | no tools                |
| "What time is it, and what's 100 / 4?" | both tools in one turn  |


For the last case: one assistant message may contain **two** `tool_use` blocks. Your loop should run both and append both `tool_result` messages before the next LLM call.

### 7. Reflect (5 min)

Write `day-02/notes.md`:

1. How did your `calculate` description change model behavior?
2. What happened with the two-tool prompt — one turn or two?
3. What breaks if schema `required` fields don't match your Python function?

---



## Self-check

- [x] Both tools registered and passed to the LLM
- [ ] `calculate` rejects unsafe input
- [x] Multi-tool prompt works in a single turn
- [x] You can explain each field in both schemas
- [ ] `notes.md` written

---



## Day 3 preview

Structured logging: print a readable trace of each turn (tool name, args, result) so you can debug without reading raw message blobs.

---



## References

- Anthropic tool use: [https://docs.anthropic.com/en/docs/build-with-claude/tool-use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- Day 1 notes on schema design (description = routing logic)

