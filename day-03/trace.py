"""Day 3 — structured trace for agent runs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Trace:
    """Record agent events as a structured log.
    """

    run_id: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"))
    events: list[dict[str, Any]] = field(default_factory=list)

    def emit(self, event: str, **data: Any) -> None:
        """Record one event and print it.

        Example:
            trace.emit("tool_call", turn=1, name="calculate", input={"expression": "2+2"})
        """
        event_data = {
            "event": event,
            "run_id": self.run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **data
        }
        self.events.append(event_data)
        print(event_data)

    def summary(self) -> dict[str, Any]:
        """Return run stats: turns, tool_calls, final event type."""
        num_tool_calls = 0
        for event in self.events:
            if event["event"] == "tool_call":
                num_tool_calls +=1 
        return {
            "run_id": self.run_id,
            "turns": self.events[-1]["turn"], 
            "tool_calls": num_tool_calls,
            "final_event_type": self.events[-1]["event"]
        }

    def _format(self, record: dict[str, Any]) -> str:
        """Format a record for stdout. Default: JSON lines."""
        return json.dumps(record, default=str)
