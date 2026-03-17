# pulsebot/agents/manager_agent.py
"""ManagerAgent: coordinates a project and bridges kanban <-> messages."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from pulsebot.agents.sub_agent import SubAgent
from pulsebot.timeplus.streams import StreamWriter
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.agents.models import SubAgentSpec
    from pulsebot.config import Config
    from pulsebot.core.executor import ToolExecutor
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
        executor: ToolExecutor,
        config: Config,
        initial_messages: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(spec, timeplus, llm_provider, skill_loader, executor, config)
        self.worker_specs = worker_specs
        self.session_id = session_id
        self.initial_messages = initial_messages or []

        # messages stream has 'id' column so StreamWriter is fine here;
        # kanban_projects uses 'project_id' so we write via client.insert() directly.
        self.messages_writer = StreamWriter(self._batch_client, "messages")

    async def run(self) -> None:
        """Manager event loop: dispatch tasks, collect results, deliver output."""
        self._running = True

        # Write initial task messages to kanban
        await self._dispatch_initial_tasks()

        query = f"""
        SELECT *, _tp_sn FROM pulsebot.kanban
        WHERE target_id = '{self.agent_id}'
        AND project_id = '{self.project_id}'
        AND msg_type IN ('result', 'error', 'status')
        SETTINGS seek_to='latest'
        """

        logger.info(f"ManagerAgent {self.agent_id} listening for results")

        async for message in self.kanban_reader.stream(query):
            if not self._running:
                break

            msg_type = message.get("msg_type", "")

            if msg_type == "result":
                await self._deliver_result(message)
                await self._complete_project()
                break
            elif msg_type == "error":
                await self._handle_worker_error(message)
                break
            elif msg_type == "status":
                await self._forward_status(message)

            self._checkpoint_sn = message.get("_tp_sn", self._checkpoint_sn)
            await self._persist_checkpoint()

    async def _dispatch_initial_tasks(self) -> None:
        """Write the initial task messages to the kanban stream."""
        for msg in self.initial_messages:
            target = msg.get("target", "")
            content = msg.get("content", "")
            if not target:
                logger.warning("Initial message missing 'target' field, skipping")
                continue
            self._batch_client.insert("pulsebot.kanban", [{
                "project_id": self.project_id,
                "sender_id": self.agent_id,
                "target_id": target,
                "msg_type": "task",
                "content": content,
            }])
            logger.info(f"Dispatched task to {target}")

    async def _deliver_result(self, message: dict[str, Any]) -> None:
        """Write the final result to pulsebot.messages for the main agent."""
        await self.messages_writer.write({
            "session_id": self.session_id,
            "source": "agent",
            "target": "user",
            "message_type": "agent_response",
            "content": message.get("content", ""),
            "metadata": json.dumps({
                "project_id": self.project_id,
                "from_agent": message.get("sender_id", ""),
            }),
        })
        logger.info(f"ManagerAgent {self.agent_id} delivered final result")

    async def _handle_worker_error(self, message: dict[str, Any]) -> None:
        """Handle an unrecoverable error from a worker agent."""
        error_text = f"Multi-agent project failed: {message.get('content', 'unknown error')}"
        logger.error(f"Project {self.project_id} worker error: {error_text}")
        await self.messages_writer.write({
            "session_id": self.session_id,
            "source": "agent",
            "target": "user",
            "message_type": "agent_response",
            "content": error_text,
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
            "target": "user",
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
        await self._update_project_status("completed")
        self._running = False
        logger.info(f"Project {self.project_id} completed")

    async def _update_project_status(self, status: str) -> None:
        """Write a project status update to kanban_projects stream."""
        self._batch_client.insert("pulsebot.kanban_projects", [{
            "project_id": self.project_id,
            "name": "",
            "description": "",
            "status": status,
            "created_by": "main",
            "session_id": self.session_id,
            "agent_ids": [spec.agent_id for spec in self.worker_specs],
        }])
