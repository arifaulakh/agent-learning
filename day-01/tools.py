"""Day 1 tools — implement these yourself."""

from datetime import datetime, timezone


def get_current_time() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


# Map tool names to Python functions. The agent loop looks up by name.
TOOLS: dict[str, callable] = {
    "get_current_time": get_current_time,
}
