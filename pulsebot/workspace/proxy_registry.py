"""ProxyRegistry — API server side in-memory registry.

Maps  session_id → task_id → agent_base_url  so the proxy router knows
where to forward requests.

Starts empty on API server boot. Populated at runtime when the agent calls
POST /internal/workspace/register. Lost on API server restart (v1 scope —
designed to be swapped for a persistent store later without interface changes).

Thread-safe: uses asyncio.Lock for all mutations.
"""

from __future__ import annotations

import asyncio
from typing import Any


class ProxyRegistry:
    """In-memory workspace proxy registry.

    Example::

        registry = ProxyRegistry()
        registry.register("abc-123", "cpu-monitor", "http://agent:8001", "fullstack_app")
        agent_url = registry.lookup("abc-123", "cpu-monitor")
        registry.deregister("abc-123", "cpu-monitor")
    """

    def __init__(self) -> None:
        # { session_id: { task_id: { agent_url, artifact_type } } }
        self._data: dict[str, dict[str, dict[str, str]]] = {}
        self._lock = asyncio.Lock()

    async def register(
        self,
        session_id: str,
        task_id: str,
        agent_url: str,
        artifact_type: str,
    ) -> None:
        """Add or update a task registration.

        Args:
            session_id: Conversation session ID.
            task_id: Task slug.
            agent_url: Base URL of the agent WorkspaceServer (e.g. http://agent:8001).
            artifact_type: One of "file", "html_app", "fullstack_app".
        """
        async with self._lock:
            self._data.setdefault(session_id, {})[task_id] = {
                "agent_url": agent_url.rstrip("/"),
                "artifact_type": artifact_type,
            }

    async def deregister(self, session_id: str, task_id: str) -> bool:
        """Remove a task registration.

        Returns:
            True if the entry existed and was removed, False otherwise.
        """
        async with self._lock:
            session = self._data.get(session_id, {})
            if task_id in session:
                del session[task_id]
                if not session:
                    del self._data[session_id]
                return True
            return False

    def lookup(self, session_id: str, task_id: str) -> str | None:
        """Return the agent_url for a registered task, or None.

        This is called on every proxy request — no lock needed for reads
        on CPython's GIL, but we return a copy to be safe.
        """
        entry = self._data.get(session_id, {}).get(task_id)
        return entry["agent_url"] if entry else None

    def list_all(self) -> list[dict[str, Any]]:
        """Return all registered entries (for debugging / admin)."""
        result = []
        for session_id, tasks in self._data.items():
            for task_id, info in tasks.items():
                result.append({
                    "session_id": session_id,
                    "task_id": task_id,
                    **info,
                })
        return result
