# pulsebot/agents/event_watcher.py
"""EventWatcher: subscribes to a streaming query and triggers project runs per matching row."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Callable, Coroutine

from pulsebot.timeplus.client import TimeplusClient
from pulsebot.timeplus.streams import StreamReader
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.agents.project_manager import ProjectManager
    from pulsebot.config import Config

logger = get_logger(__name__)

_RECONNECT_DELAYS = [3, 10, 30]  # seconds
_MAX_CONSECUTIVE_FAILURES = 3    # zero-row attempts before marking project failed


class EventWatcher:
    """
    Subscribes to a user-defined Proton streaming SQL query and triggers
    a project workflow once per matching row (drop-on-busy model).

    Checkpoints the Proton _tp_sn after every row so that restarts resume
    from the last processed sequence number without missing or replaying events.
    """

    def __init__(
        self,
        project_id: str,
        event_query: str,
        context_field: str,
        trigger_prompt: str,
        project_manager: ProjectManager,
        timeplus: Any,
        config: Config,
        checkpoint_sn: int = 0,
        start_time: datetime | None = None,
        on_query_failed: Callable[[str, str], Coroutine[Any, Any, None]] | None = None,
    ) -> None:
        self.project_id = project_id
        self._event_query = event_query
        self._context_field = context_field
        self._trigger_prompt = trigger_prompt
        self._pm = project_manager
        self._checkpoint_sn = checkpoint_sn
        self._start_time = start_time or datetime.now(UTC)
        self._running = False
        self._on_query_failed = on_query_failed

        # Two dedicated clients: execute_iter blocks its connection, so reads and
        # writes must be on separate connections.
        read_client = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )
        # StreamReader stores the client as self.client; stream_name is unused
        # when calling stream() with a raw query string.
        self._reader = StreamReader(read_client, "kanban")
        # Separate write client so checkpoint inserts are never blocked by the
        # streaming read connection.
        self._batch_client = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )

    def _build_query(self) -> str:
        """Build the streaming query with seek control and optional _tp_sn filter.

        Appends the _tp_sn filter with WHERE or AND depending on whether the
        user's event_query already contains a WHERE clause.
        """
        if self._checkpoint_sn > 0:
            has_where = "WHERE" in self._event_query.upper()
            connector = "AND" if has_where else "WHERE"
            return (
                f"{self._event_query} {connector} _tp_sn > {self._checkpoint_sn} "
                f"SETTINGS seek_to='earliest'"
            )
        seek_ts = self._start_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self._event_query} SETTINGS seek_to='{seek_ts}'"

    async def _persist_checkpoint(self) -> None:
        """Write the current checkpoint_sn to kanban_agents."""
        agent_id = f"event_watcher_{self.project_id}"
        try:
            self._batch_client.insert("pulsebot.kanban_agents", [{
                "agent_id": agent_id,
                "project_id": self.project_id,
                "name": "EventWatcher",
                "role": "watcher",
                "task_description": "Streaming query event watcher",
                "target_agents": [],
                "status": "running",
                "skills": [],
                "skill_overrides": "{}",
                "config": "{}",
                "checkpoint_sn": self._checkpoint_sn,
            }])
        except Exception as e:
            logger.warning(
                f"EventWatcher {self.project_id} failed to persist checkpoint "
                f"(sn={self._checkpoint_sn}): {e}"
            )

    async def _process_row(self, row: dict[str, Any]) -> None:
        """Handle one row from the streaming query."""
        sn = row.get("_tp_sn", self._checkpoint_sn)

        _MISSING = object()
        context_value = row.get(self._context_field, _MISSING)
        if context_value is _MISSING:
            logger.warning(
                f"EventWatcher {self.project_id}: context_field "
                f"'{self._context_field}' not found in row — skipping"
            )
            self._checkpoint_sn = sn
            await self._persist_checkpoint()
            return
        if context_value is None or context_value == "":
            logger.warning(
                f"EventWatcher {self.project_id}: context_field value is empty — skipping"
            )
            self._checkpoint_sn = sn
            await self._persist_checkpoint()
            return

        if self._pm.is_project_busy(self.project_id):
            logger.debug(
                f"EventWatcher {self.project_id}: project busy — event skipped"
            )
            self._checkpoint_sn = sn
            await self._persist_checkpoint()
            return

        combined_prompt = f"{self._trigger_prompt}\n\n{context_value}"
        self._pm.trigger_project_with_context(self.project_id, combined_prompt)
        self._checkpoint_sn = sn
        await self._persist_checkpoint()
        logger.info(
            f"EventWatcher {self.project_id}: triggered run (sn={sn})"
        )

    async def run(self) -> None:
        """Main async loop: subscribe, process rows, reconnect on disconnect."""
        self._running = True
        delay_idx = 0
        logger.info(
            f"EventWatcher {self.project_id} starting "
            f"(checkpoint_sn={self._checkpoint_sn})"
        )

        consecutive_failures = 0
        while self._running:
            query = self._build_query()
            got_row = False
            try:
                async for row in self._reader.stream(query):
                    if not self._running:
                        break
                    await self._process_row(row)
                    got_row = True
                    delay_idx = 0          # successful row resets backoff
                    consecutive_failures = 0

                if not self._running:
                    break

                if got_row:
                    # Valid stream that disconnected — treat as transient.
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1

                delay = _RECONNECT_DELAYS[min(delay_idx, len(_RECONNECT_DELAYS) - 1)]
                logger.warning(
                    f"EventWatcher {self.project_id}: streaming query ended "
                    f"unexpectedly (no rows, failure {consecutive_failures}/"
                    f"{_MAX_CONSECUTIVE_FAILURES}), reconnecting in {delay}s..."
                )

                if consecutive_failures >= _MAX_CONSECUTIVE_FAILURES:
                    error_msg = (
                        f"Streaming query exited {consecutive_failures} consecutive "
                        f"times without returning any rows. "
                        f"Check that event_query is correct: {self._event_query!r}"
                    )
                    logger.error(f"EventWatcher {self.project_id}: {error_msg}")
                    if self._on_query_failed:
                        await self._on_query_failed(self.project_id, error_msg)
                    self._running = False
                    break

                await asyncio.sleep(delay)
                delay_idx += 1
            except Exception as e:
                if not self._running:
                    break
                consecutive_failures += 1
                delay = _RECONNECT_DELAYS[min(delay_idx, len(_RECONNECT_DELAYS) - 1)]
                logger.warning(
                    f"EventWatcher {self.project_id}: error in streaming query "
                    f"({e}, failure {consecutive_failures}/{_MAX_CONSECUTIVE_FAILURES})"
                    f", retrying in {delay}s"
                )

                if consecutive_failures >= _MAX_CONSECUTIVE_FAILURES:
                    error_msg = (
                        f"Streaming query failed {consecutive_failures} consecutive "
                        f"times: {e}. "
                        f"Check that event_query is correct: {self._event_query!r}"
                    )
                    logger.error(f"EventWatcher {self.project_id}: {error_msg}")
                    if self._on_query_failed:
                        await self._on_query_failed(self.project_id, error_msg)
                    self._running = False
                    break

                await asyncio.sleep(delay)
                delay_idx += 1

        logger.info(f"EventWatcher {self.project_id} stopped")

    def stop(self) -> None:
        """Signal the run loop to exit."""
        self._running = False
