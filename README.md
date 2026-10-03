# Agents from Scratch — Sept 2 → Dec 31

Daily exercises to learn agent fundamentals by building, not by copying frameworks.

## Setup

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv sync
cp .env.example .env   # add your API key
```

Run a day's exercise from its folder:

```bash
cd day-01   # or day-02, day-03, day-04, …
uv run python main.py
```

Each day copies forward from the previous one so you can `diff` them and see what changed.

## How to use this repo

- One folder per day: `day-01/`, `day-02/`, …
- Each day has a `README.md` with goals, constraints, and a self-check.
- **You write the code.** Stubs and TODOs only — no solutions.
- Dependencies live in the root `pyproject.toml` (shared across all days).

## Core progression (high level)

| Phase | Focus |
|-------|--------|
| Week 1 | Agent loop, tools, traces, error handling |
| Week 2 | Multi-step tasks, conversation state, evals |
| ~Day 10 | Compare: rebuild same agent with OpenAI Agents SDK |
| Week 3+ | Agents API, workflows, routing |

## Sources worth bookmarking

- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic Cookbook — basic workflows](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents)
- [OpenAI — Agents SDK docs](https://openai.github.io/openai-agents-python/) (read *after* you build your own loop)
