# Day 3 — Observability (structured traces)

**Date:** Sept 16, 2026  
**Time budget:** 60–90 min  
**Rule:** Still no agent frameworks. Same loop, better visibility.

---

## Should you jump to OpenAI's Agents API?

**Not yet — finish this week first.**

OpenAI now has three layers ([docs](https://developers.openai.com/api/docs/guides/agents)):

| Layer | What it is | Who runs the loop |
|-------|-----------|-------------------|
| **Responses API** | Raw model + tools | You |
| **Agents SDK** | Code-first loop in *your* app | SDK in your process |
| **Agents API** | Managed Codex harness + sessions + sandbox | OpenAI |

You're currently at row 1 — building the loop yourself. That's intentional.

The [Agents API](https://openai.com/index/introducing-the-agents-api/) is powerful for **production apps** where OpenAI manages sessions, context compaction, sandboxes, and recovery. But it hides the exact thing you're learning: the message loop, tool routing, and stop conditions.

**Recommended path for this repo:**

| When | What |
|------|------|
| Days 1–5 | Fundamentals (loop, tools, traces, errors) |
| Days 6–7 | Conversation state + a small multi-step task |
| ~Day 10 | **Compare day:** rebuild time+calculate with OpenAI Agents SDK side-by-side |
| After that | Agents API — same agent, managed harness |

When you do reach the Agents API, you'll recognize everything it automates because you built it by hand first.

---

## Today's goal

Add a **structured trace** so you can debug agent runs without reading raw `response.content` blobs.

After today, a run should produce a readable log like:

```
[turn 1] llm → tool_use: get_current_time({})
[turn 1] tool → get_current_time → "2026-09-17T03:00:00+00:00"
[turn 2] llm → text: "The current UTC time is ..."
[done] turns=2
```

---

## What you'll learn

- Why observability matters before adding complexity
- Separating **agent logic** from **logging** (extract a `trace.py` module)
- Event-shaped logs you can grep, save, or replay later
- Foundation for evals (Day 8+) — you can't measure what you can't see

---

## Files

```
day-03/
├── README.md
├── main.py       ← wire in trace calls (TODOs marked)
├── tools.py      ← copied from Day 2 (done)
└── trace.py      ← implement Trace class (TODO)
```

---

## Step-by-step

### 1. Confirm baseline (5 min)

```bash
cd day-03
uv run python main.py
```

Day 2 behavior should still work before you touch logging.

### 2. Implement `trace.py` (30 min)

Build a small `Trace` class that records events. Each event is a dict:

```python
{"event": "tool_call", "turn": 1, "name": "calculate", "input": {"expression": "2+2"}}
```

Required event types:

| Event | When |
|-------|------|
| `turn_start` | Top of each loop iteration |
| `llm_response` | After model returns (note: tool_use or text) |
| `tool_call` | Before executing a tool |
| `tool_result` | After executing a tool |
| `final_answer` | Model returned text, loop exits |
| `max_turns` | Hit the turn limit |

Methods to implement:

```python
class Trace:
    def emit(self, event: str, **data) -> None: ...
    def summary(self) -> dict: ...  # e.g. {"turns": 2, "tool_calls": 1}
```

Print each event as a single line (your choice: human-readable or JSON).

### 3. Wire traces into `main.py` (20 min)

Replace ad-hoc `print()` calls with `trace.emit(...)`. The loop logic stays identical — only logging changes.

**Constraint:** `agent_loop` should not contain formatting logic. All output goes through `Trace`.

### 4. Add trace-to-file (optional stretch, 15 min)

```bash
uv run python main.py 2>&1 | tee run.log
```

Or add `Trace(path="runs/2026-09-16.jsonl")` that appends JSON lines. Useful when you start running many test prompts.

### 5. Test (10 min)

Run the Day 2 test prompts and confirm the trace tells the full story:

| Prompt | Trace should show |
|--------|-------------------|
| "What time is it?" | 1 tool call, 2 turns |
| "What is 847 * 293?" | calculate called once |
| "Hello!" | 0 tool calls, 1 turn |
| "What time is it, and what's 100 / 4?" | 2 tool calls in turn 1 |

### 6. Reflect (5 min)

Write `day-03/notes.md`:

1. What was hardest to debug in Day 1/2 that traces make obvious now?
2. If a tool returned `"Error: ..."`, would your trace distinguish that from success?
3. What would OpenAI's Agents API be doing for you that you're still doing manually?

---

## Self-check

- [ ] Trace module separate from agent loop
- [ ] Every turn and tool call visible in output
- [ ] `summary()` reports turn count and tool call count
- [ ] Day 2 functionality unchanged
- [ ] `notes.md` written

---

## Day 4 preview

Error handling: what happens when a tool fails, the model hallucinates a tool name, or JSON args are malformed? Make the agent recover gracefully instead of crashing.

---

## References

- OpenAI: [Agents overview](https://developers.openai.com/api/docs/guides/agents) — save for ~Day 10
- OpenAI: [Introducing the Agents API](https://openai.com/index/introducing-the-agents-api/) — read the "what the harness manages" section after today
- Anthropic: [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — "prioritize transparency by showing planning steps"
