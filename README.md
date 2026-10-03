# Agent Learning

Learning to build AI agents from the ground up — no frameworks, raw API first.

## Setup

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv sync
cp .env.example .env   # add your API key
```

Run from any module folder:

```bash
cd day-01   # day-02, day-03, day-04, …
uv run python main.py
```

Each `day-XX/` folder builds on the previous one. Use `diff` to see what changed.

## Progress

| Module | Focus |
|--------|--------|
| day-01 | Agent loop, one tool |
| day-02 | Multiple tools |
| day-03 | Structured tracing |
| day-04 | Error handling |

## References

- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic Cookbook — basic workflows](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents)
- [OpenAI — Agents SDK docs](https://openai.github.io/openai-agents-python/)
