# pulsebot/agents/manager_agent.py
"""ManagerAgent: coordinates a project and bridges kanban <-> messages."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from pulsebot.agents.sub_agent import SubAgent
from pulsebot.timeplus.client import escape_sql_str
from pulsebot.timeplus.event_writer import EventWriter
from pulsebot.timeplus.streams import StreamWriter
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.agents.models import SubAgentSpec
    from pulsebot.config import Config
    from pulsebot.providers.base import LLMProvider
    from pulsebot.skills.loader import SkillLoader
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


class ManagerAgent(SubAgent):
    """
    A special sub-agent that coordinates a project.

    Responsibilities:
    1. Dispatch initial task messages to worker agents via kanban.
    2. Listen on kanban for results/errors from workers.
    3. Write the final result to pulsebot.messages for the main agent.
    4. Cancel all workers and mark project complete/failed.
    """

    def __init__(
        self,
        spec: SubAgentSpec,
        worker_specs: list[SubAgentSpec],
        session_id: str,
        timeplus: TimeplusClient,
        llm_provider: LLMProvider,
        skill_loader: SkillLoader,
        config: Config,
        project_name: str = "",
        project_description: str = "",
        initial_messages: list[dict[str, Any]] | None = None,
        reporting_agent_ids: list[str] | None = None,
        on_run_complete: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(spec, timeplus, llm_provider, skill_loader, config)
        self.worker_specs = worker_specs
        self.session_id = session_id
        self.project_name = project_name
        self.project_description = project_description
        self.initial_messages = initial_messages or []
        # Agent IDs expected to report a result. Complete once all have reported
        # at least once — ignores duplicate reports from the same sender.
        self._reporting_agent_ids: set[str] = set(reporting_agent_ids or [])
        # Called (with no args) after each run completes in scheduled mode.
        self._on_run_complete = on_run_complete

        # messages stream has 'id' column so StreamWriter is fine here;
        # kanban_projects uses 'project_id' so we write via client.insert() directly.
        self.messages_writer = StreamWriter(self._batch_client, "messages")

        # Override the events writer created by SubAgent.__init__ with manager-specific metadata
        self.events = EventWriter(
            StreamWriter(self._batch_client, "events"),
            default_source=f"manager:{self.agent_id}",
            default_tags=[f"agent:{self.agent_id}", f"project:{self.project_id}"],
        )

    async def run(self) -> None:
        """Manager event loop: dispatch tasks, collect results, deliver output."""
        self._running = True
        await self.events.emit("project.created", payload={
            "project_id": self.project_id,
            "agent_count": len(self.worker_specs),
            "agent_ids": [s.agent_id for s in self.worker_specs],
            "session_id": self.session_id,
            "is_scheduled": self.spec.is_scheduled,
        })
        try:
            if self.spec.is_scheduled:
                await self._run_scheduled()
            else:
                await self._run_oneshot()
        except Exception as e:
            await self.events.emit_error("manager.error", e, payload={
                "agent_id": self.agent_id,
                "project_id": self.project_id,
            })
            raise
        finally:
            await self.events.emit("manager.stopped", payload={
                "agent_id": self.agent_id,
                "project_id": self.project_id,
            })

    async def _run_oneshot(self) -> None:
        """Original one-shot logic: dispatch, collect results, complete."""
        await self._dispatch_initial_tasks()

        seek_to = self._start_time.strftime('%Y-%m-%d %H:%M:%S')
        query = f"""
        SELECT *, _tp_sn FROM pulsebot.kanban
        WHERE target_id = '{escape_sql_str(self.agent_id)}'
        AND project_id = '{escape_sql_str(self.project_id)}'
        AND msg_type IN ('result', 'error', 'status')
        SETTINGS seek_to='{seek_to}'
        """

        logger.info(
            f"ManagerAgent {self.agent_id} listening for results "
            f"(expecting: {self._reporting_agent_ids})"
        )

        reported: set[str] = set()

        async for message in self.kanban_reader.stream(query):
            if not self._running:
                break

            msg_type = message.get("msg_type", "")

            if msg_type == "result":
                sender_id = message.get("sender_id", "")
                await self.events.emit("manager.result_received", payload={
                    "agent_id": self.agent_id,
                    "project_id": self.project_id,
                    "sender_id": sender_id,
                    "reported": list(reported | {sender_id}),
                    "expected": list(self._reporting_agent_ids),
                })
                await self._deliver_result(message)
                reported.add(sender_id)
                if self._reporting_agent_ids.issubset(reported):
                    await self._complete_project()
                    break
            elif msg_type == "error":
                await self._handle_worker_error(message)
                break
            elif msg_type == "status":
                await self._forward_status(message)

            self._checkpoint_sn = message.get("_tp_sn", self._checkpoint_sn)
            await self._persist_checkpoint()

    async def _run_scheduled(self) -> None:
        """Scheduled long-running loop: idle until trigger, execute run, repeat.

        Listens for 'trigger' messages from kanban. On each trigger, dispatches
        tasks to entry-point workers and collects results. After delivering the
        result, restarts the streaming query from the new checkpoint so that the
        connection never goes stale between runs.
        """
        if self.initial_messages:
            await self._dispatch_initial_tasks()

        logger.info(f"ManagerAgent {self.agent_id} idle, waiting for triggers")

        collecting = False   # True while a run is in progress
        reported: set[str] = set()

        while self._running:
            # Rebuild the streaming query on every outer-loop iteration so that
            # a fresh connection is used after each completed run (avoids the
            # Proton behaviour where a historical seek_to query stops delivering
            # new rows after the initial catch-up batch).
            if self._checkpoint_sn > 0:
                sn_filter = f"AND _tp_sn > {self._checkpoint_sn}"
                seek_to = "earliest"
            else:
                seek_to = self._start_time.strftime('%Y-%m-%d %H:%M:%S')
                sn_filter = ""

            query = f"""
            SELECT *, _tp_sn FROM pulsebot.kanban
            WHERE target_id = '{escape_sql_str(self.agent_id)}'
            AND project_id = '{escape_sql_str(self.project_id)}'
            AND msg_type IN ('trigger', 'result', 'error', 'status', 'control')
            {sn_filter}
            SETTINGS seek_to='{seek_to}'
            """

            run_completed = False

            async for message in self.kanban_reader.stream(query):
                if not self._running:
                    break

                msg_type = message.get("msg_type", "")

                if msg_type == "trigger":
                    if collecting:
                        # Should not happen (API guards this), but be defensive.
                        logger.warning(
                            f"ManagerAgent {self.agent_id} received trigger while run "
                            "is in progress — skipping"
                        )
                    else:
                        trigger_prompt = self._extract_trigger_prompt(message)
                        logger.info(
                            f"ManagerAgent {self.agent_id} trigger received, starting run"
                        )
                        await self.events.emit("manager.triggered", payload={
                            "agent_id": self.agent_id,
                            "project_id": self.project_id,
                            "prompt": trigger_prompt,
                        })
                        await self._dispatch_trigger_tasks(trigger_prompt)
                        collecting = True
                        reported = set()

                elif msg_type == "result" and collecting:
                    sender_id = message.get("sender_id", "")
                    await self.events.emit("manager.result_received", payload={
                        "agent_id": self.agent_id,
                        "project_id": self.project_id,
                        "sender_id": sender_id,
                        "reported": list(reported | {sender_id}),
                        "expected": list(self._reporting_agent_ids),
                    })
                    await self._deliver_result(message)
                    reported.add(sender_id)
                    if self._reporting_agent_ids.issubset(reported):
                        self._checkpoint_sn = message.get("_tp_sn", self._checkpoint_sn)
                        await self._persist_checkpoint()
                        await self._finish_scheduled_run()
                        collecting = False
                        run_completed = True
                        break  # restart streaming query from updated checkpoint

                elif msg_type == "error" and collecting:
                    await self._handle_worker_error_scheduled(message)
                    collecting = False
                    run_completed = True
                    break  # restart streaming query

                elif msg_type == "status":
                    await self._forward_status(message)

                elif msg_type == "control" and message.get("content") == "cancel":
                    logger.info(f"ManagerAgent {self.agent_id} received cancel control")
                    self._running = False
                    break

                self._checkpoint_sn = message.get("_tp_sn", self._checkpoint_sn)
                await self._persist_checkpoint()

            if not run_completed and self._running:
                # Stream ended unexpectedly (connection drop). Log and reconnect.
                logger.warning(
                    f"ManagerAgent {self.agent_id} kanban stream ended unexpectedly, "
                    "reconnecting..."
                )

    async def _dispatch_initial_tasks(self) -> None:
        """Write the initial task messages to the kanban stream."""
        # Build name->agent_id map so callers can use human-readable names
        name_to_id = {spec.name: spec.agent_id for spec in self.worker_specs}

        for msg in self.initial_messages:
            target = msg.get("target", "")
            content = msg.get("content", "")
            if not target:
                logger.warning("Initial message missing 'target' field, skipping")
                continue
            # Resolve agent name to agent_id (fall back to value as-is if not found)
            target_id = name_to_id.get(target, target)
            self._batch_client.insert("pulsebot.kanban", [{
                "project_id": self.project_id,
                "sender_id": self.agent_id,
                "target_id": target_id,
                "msg_type": "task",
                "content": content,
            }])
            logger.info(f"Dispatched task to {target_id} (resolved from '{target}')")

        dispatched_ids = list({
            name_to_id.get(msg.get("target", ""), msg.get("target", ""))
            for msg in self.initial_messages
            if msg.get("target", "")
        })
        await self.events.emit("manager.dispatched", payload={
            "agent_id": self.agent_id,
            "project_id": self.project_id,
            "target_ids": dispatched_ids,
            "task_count": len(self.initial_messages),
        })

    async def _deliver_result(self, message: dict[str, Any]) -> None:
        """Broadcast the final result to all active channels via task_notification event."""
        result_text = message.get("content", "")
        await self.events.emit("task_notification", payload={
            "task_name": self.spec.name,
            "text": result_text,
            "session_id": self.session_id,
        })
        logger.info(f"ManagerAgent {self.agent_id} delivered final result")

    async def _dispatch_trigger_tasks(self, trigger_prompt: str) -> None:
        """Dispatch tasks to entry-point workers using the trigger prompt.

        Only dispatches to "source" workers — those whose agent_id does not
        appear in any other worker's target_agents list. Workers that receive
        input from peer workers will get their task from those peers, not from
        the manager directly.
        """
        all_peer_targets: set[str] = set()
        for spec in self.worker_specs:
            all_peer_targets.update(spec.target_agents)

        source_workers = [
            spec for spec in self.worker_specs
            if spec.agent_id not in all_peer_targets
        ]
        # Fallback: if the topology analysis yields nothing (e.g. a cycle),
        # dispatch to all workers.
        if not source_workers:
            source_workers = list(self.worker_specs)

        for spec in source_workers:
            self._batch_client.insert("pulsebot.kanban", [{
                "project_id": self.project_id,
                "sender_id": self.agent_id,
                "target_id": spec.agent_id,
                "msg_type": "task",
                "content": trigger_prompt,
            }])
        await self.events.emit("manager.dispatched", payload={
            "agent_id": self.agent_id,
            "project_id": self.project_id,
            "target_ids": [spec.agent_id for spec in source_workers],
            "task_count": len(source_workers),
        })

    def _extract_trigger_prompt(self, message: dict[str, Any]) -> str:
        """Extract the prompt from a trigger kanban message."""
        content = message.get("content", "")
        try:
            data = json.loads(content)
            return data.get("prompt", content)
        except (json.JSONDecodeError, AttributeError):
            return content

    async def _finish_scheduled_run(self) -> None:
        """Complete one scheduled run: update status, notify callback, stay alive."""
        await self.events.emit("manager.run_completed", payload={
            "agent_id": self.agent_id,
            "project_id": self.project_id,
        })
        await self._update_project_status("active")  # stays active for next run
        if self._on_run_complete is not None:
            self._on_run_complete()
        logger.info(
            f"ManagerAgent {self.agent_id} run completed, returning to idle"
        )

    async def _handle_worker_error_scheduled(self, message: dict[str, Any]) -> None:
        """Handle a worker error in scheduled mode: deliver error, stay alive."""
        error_text = (
            f"Scheduled run failed: {message.get('content', 'unknown error')}"
        )
        logger.error(f"Project {self.project_id} scheduled run error: {error_text}")
        await self.events.emit("task_notification", payload={
            "task_name": self.spec.name,
            "text": error_text,
            "session_id": self.session_id,
        })
        if self._on_run_complete is not None:
            self._on_run_complete()
        logger.info(
            f"ManagerAgent {self.agent_id} returning to idle after run error"
        )

    async def _handle_worker_error(self, message: dict[str, Any]) -> None:
        """Handle an unrecoverable error from a worker agent (one-shot mode)."""
        error_text = f"Multi-agent project failed: {message.get('content', 'unknown error')}"
        logger.error(f"Project {self.project_id} worker error: {error_text}")
        await self.events.emit("task_notification", payload={
            "task_name": self.spec.name,
            "text": error_text,
            "session_id": self.session_id,
        })
        await self._update_project_status("failed")
        self._running = False

    async def _forward_status(self, message: dict[str, Any]) -> None:
        """Forward progress status to the user session."""
        sender = message.get("sender_id", "sub-agent")
        content = message.get("content", "")
        status_text = f"[{sender}] {content}"
        await self.messages_writer.write({
            "session_id": self.session_id,
            "source": "agent",
            "target": "channel:webchat",
            "message_type": "tool_result",
            "content": json.dumps({"status": status_text}),
        })

    async def _complete_project(self) -> None:
        """Cancel all workers, update project status, stop self."""
        for spec in self.worker_specs:
            self._batch_client.insert("pulsebot.kanban", [{
                "project_id": self.project_id,
                "sender_id": self.agent_id,
                "target_id": spec.agent_id,
                "msg_type": "control",
                "content": "cancel",
            }])
        await self.events.emit("manager.completed", payload={
            "agent_id": self.agent_id,
            "project_id": self.project_id,
            "status": "completed",
        })
        await self._update_project_status("completed")
        self._running = False
        logger.info(f"Project {self.project_id} completed")

    async def _update_project_status(self, status: str) -> None:
        """Write a project status update to kanban_projects stream.

        All scheduling and event fields are always included so that
        LIMIT 1 BY project_id queries return consistent data regardless
        of which row is most recent.
        """
        self._batch_client.insert("pulsebot.kanban_projects", [{
            "project_id": self.project_id,
            "name": self.project_name,
            "description": self.project_description,
            "status": status,
            "created_by": "main",
            "session_id": self.session_id,
            "agent_ids": [spec.agent_id for spec in self.worker_specs],
            "config_overrides": "{}",
            "is_scheduled": self.spec.is_scheduled,
            "schedule_type": self.spec.schedule_type if self.spec.is_scheduled else "",
            "schedule_expr": self.spec.schedule_expr if self.spec.is_scheduled else "",
            "trigger_prompt": self.spec.trigger_prompt if self.spec.is_scheduled else "",
            "event_query": self.spec.event_query,
            "context_field": self.spec.context_field,
        }])
