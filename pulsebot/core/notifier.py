"""NotificationDispatcher: writes task_notification events to the events stream."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.streams import StreamWriter

logger = get_logger(__name__)


class NotificationDispatcher:
    """Broadcasts scheduled-task results to all channels via the events stream.

    Channel adapters (Telegram, WebSocket) subscribe to the events stream and
    fan out any ``task_notification`` events to their active connections.
    """

    def __init__(self, events_writer: "StreamWriter") -> None:
        self._writer = events_writer

    async def broadcast_task_result(
        self,
        task_name: str,
        text: str,
        session_id: str,
    ) -> None:
        """Write a task_notification event for all channel adapters to pick up.

        Args:
            task_name: Sanitised internal task name.
            text: The agent's response text to broadcast.
            session_id: The global session ID for this task run.
        """
        try:
            await self._writer.write({
                "event_type": "task_notification",
                "source": "agent",
                "severity": "info",
                "payload": json.dumps({
                    "task_name": task_name,
                    "text": text,
                    "session_id": session_id,
                }),
                "tags": ["task", "broadcast"],
            })
            logger.info("Broadcast task result", extra={"task_name": task_name})
        except Exception as e:
            logger.warning(
                "NotificationDispatcher failed to write event",
                extra={"task_name": task_name, "error": str(e)},
            )
