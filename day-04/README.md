# Day 4 — Error Handling

**Date:** Sept 17, 2026  
**Time budget:** 60–90 min  
**Rule:** Still no agent frameworks.

---

## Today's goal

Make the agent **recover gracefully** when things go wrong — instead of crashing or silently hiding failures.

After today:

- Tool failures are visible in traces (`success: false`)
- Unknown tool names don't crash the loop
- Bad arguments are caught and returned to the model
- Max turns exits cleanly with a user-facing message

The loop keeps going after errors — the model sees the error and decides what to do next.

---

## What you'll learn

- Tools should return **results**, not raise exceptions into the loop
- The model can recover from tool errors if you feed them back clearly
- Difference between "tool returned an error string" vs "tool execution failed"
- Defensive design at the agent-computer interface (ACI)

---



## Files to change

```
day-04/
├── README.md
├── main.py       ← refactor run_tool, harden agent_loop
├── tools.py      ← optional: structured errors from calculate
└── trace.py      ← track tool_errors in summary
```

---



## Step-by-step



### 1. Introduce `ToolResult` (15 min)

In `tools.py`, implement the stub:

```python
@dataclass
class ToolResult:
    success: bool
    output: str
    error: str | None = None
```

Refactor `run_tool()` in `main.py` to return `ToolResult` instead of a bare string.


| Case             | success | output     | error                                |
| ---------------- | ------- | ---------- | ------------------------------------ |
| Happy path       | `True`  | `"248171"` | `None`                               |
| Unknown tool     | `False` | `""`       | `"Unknown tool: get_weather"`        |
| Bad args         | `False` | `""`       | `"Missing required arg: expression"` |
| Tool logic error | `False` | `""`       | `"division by zero"`                 |


**Important:** still send *something* back to the model as the tool result content — even on failure. The model needs the error message to respond intelligently.

### 2. Update traces (10 min)

Change `tool_result` events to include `success`:

```python
trace.emit("tool_result", turn=1, name="calculate", result="...", success=True)
trace.emit("tool_result", turn=1, name="calculate", result="...", success=False, error="division by zero")
```

Update `summary()` to count `tool_errors`.

### 3. Harden `run_tool` (20 min)

Handle these cases without crashing:

```python
# Unknown tool name
run_tool("get_weather", {})

# Missing required argument
run_tool("calculate", {})

# Malformed input (if you still accept str)
run_tool("calculate", "not valid json")

# Python exception inside tool
run_tool("calculate", {"expression": "100 / 0"})
```

Wrap the tool dispatch in try/except — the loop must never die on a tool failure.

### 4. Fix `max_turns` exit (10 min)

Day 3 emits `max_turns` but never tells the user. On max turns:

- Emit `max_turns` trace event
- Print a friendly message: *"I wasn't able to finish in time."*
- Emit `done` with summary (same as happy path)

To test max turns, temporarily set `MAX_TURNS = 1` and ask *"What time is it?"* (needs 2 turns). Reset to 5 when done.

### 5. Simplify tool args (optional, 5 min)

`tool_call.input` is already a `dict`. Refactor `run_tool` to accept `dict` directly instead of `json.dumps` → `json.loads`.

### 6. Test (15 min)


| Prompt                         | Expected behavior                                      |
| ------------------------------ | ------------------------------------------------------ |
| `"What is 847 * 293?"`         | Still works (regression)                               |
| `"What is 100 / 0?"`           | Tool error traced, model explains the problem          |
| `"What's the weather in NYC?"` | Model may call unknown tool OR say it can't — no crash |
| `"Calculate:"` (no expression) | Bad args handled gracefully                            |




### 7. Reflect (5 min)

Write `day-04/notes.md`:

1. Did the model recover well from tool errors? What did it say?
2. Why feed errors back to the model instead of stopping the loop?
3. What's still not handled that could crash the agent?

---



## Self-check

- [x] `ToolResult` used throughout tool dispatch
- [x] Traces distinguish success vs failure
- [x] Unknown tool / bad args don't crash
- [x] Max turns exits cleanly with `done` event
- [x] Regression test passes (`847 * 293`)
- [ ] `notes.md` written

---



## Day 5 preview

Conversation state: run multiple turns in one session so the agent remembers prior messages (`"What time is it?"` → `"Now divide that year by 2"`).

---



## Key idea

```
Tool fails → return error to model → model adapts → user gets useful reply
```

Not:

```
Tool fails → exception → agent crashes → user sees nothing
```

This is how production agents stay reliable.