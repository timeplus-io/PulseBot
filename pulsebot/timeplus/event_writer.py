"""Lightweight event emitter for pulsebot.events stream."""

from __future__ import annotations

import json
import logging
import traceback
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pulsebot.timeplus.streams import StreamWriter


logger = logging.getLogger(__name__)

_SEVERITY_LEVELS = {"debug": 0, "info": 1, "warning": 2, "error": 3, "critical": 4}

_EVENT_CATEGORIES = {
    "agent": "lifecycle",
    "subagent": "lifecycle",
    "manager": "lifecycle",
    "session": "session",
    "llm": "llm",
    "tool": "tool",
    "memory": "memory",
    "skill": "skill",
    "channel": "channel",
    "task": "task",
    "project": "multi-agent",
    "hook": "security",
    "context": "context",
    "system": "system",
}


class EventWriter:
    """Emit structured events to the pulsebot.events stream."""

    def __init__(
        self,
        writer: "StreamWriter | None",
        default_source: str = "system",
        default_tags: list[str] | None = None,
        min_severity: str = "debug",
    ) -> None:
        self._writer = writer
        self._default_source = default_source
        self._default_tags = default_tags or []
        self._min_severity_level = _SEVERITY_LEVELS.get(min_severity, 0)

    async def emit(
        self,
        event_type: str,
        *,
        severity: str = "info",
        source: str | None = None,
        payload: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> None:
        """Write a single event. Never raises."""
        if self._writer is None:
            return

        if _SEVERITY_LEVELS.get(severity, 0) < self._min_severity_level:
            return

        category = _EVENT_CATEGORIES.get(event_type.split(".")[0], "general")
        merged_tags = list(set(self._default_tags + (tags or []) + [category]))

        try:
            await self._writer.write({
                "event_type": event_type,
                "source": source or self._default_source,
                "severity": severity,
                "payload": json.dumps(payload or {}, default=str),
                "tags": merged_tags,
            })
        except Exception as _write_exc:
            logger.debug("EventWriter failed to emit %s: %s", event_type, _write_exc)

    async def emit_error(
        self,
        event_type: str,
        error: Exception,
        *,
        source: str | None = None,
        payload: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> None:
        """Emit an error event with traceback."""
        p = dict(payload or {})
        p["error"] = str(error)
        p["error_type"] = type(error).__name__
        p["traceback"] = traceback.format_exc()
        await self.emit(event_type, severity="error", source=source, payload=p, tags=tags)
