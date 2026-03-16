# pulsebot/agents/sub_agent.py
"""SubAgent: a worker agent that reads from kanban and writes results back."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from pulsebot.timeplus.streams import StreamReader, StreamWriter
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.agents.models import SubAgentSpec
    from pulsebot.config import Config
    from pulsebot.core.executor import ToolExecutor
    from pulsebot.providers.base import LLMProvider
    from pulsebot.skills.loader import SkillLoader
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


class SubAgent:
    """
    A sub-agent that participates in a multi-agent project.

    Reads task messages from the kanban stream, processes them through
    an LLM + tool loop, and writes results back to kanban.
    """

    def __init__(
        self,
        spec: SubAgentSpec,
        timeplus: TimeplusClient,
        llm_provider: LLMProvider,
        skill_loader: SkillLoader,
        executor: ToolExecutor,
        config: Config,
    ) -> None:
        from pulsebot.timeplus.client import TimeplusClient

        self.spec = spec
        self.agent_id = spec.agent_id
        self.project_id = spec.project_id

        # Resolve LLM provider (override model/provider if specified)
        self.llm = self._resolve_provider(spec, llm_provider, config)

        # Resolve skill set for this sub-agent
        self._skill_loader = self._resolve_skills(spec, skill_loader)
        self.executor = executor

        # Use a dedicated batch client for writes to avoid conflicts with
        # the streaming query connection.
        batch_client = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )

        self.kanban_reader = StreamReader(timeplus, "kanban")
        self.kanban_writer = StreamWriter(batch_client, "kanban")
        self.agents_writer = StreamWriter(batch_client, "kanban_agents")

        self._checkpoint_sn: int = spec.checkpoint_sn
        self._running = False
        self._batch_client = batch_client

    def _resolve_provider(
        self,
        spec: SubAgentSpec,
        default_provider: LLMProvider,
        config: Config,
    ) -> LLMProvider:
        """Use spec overrides if set; otherwise inherit the main provider."""
        if spec.model is None and spec.provider is None:
            return default_provider
        # Re-create provider with overrides applied
        import copy

        from pulsebot.factory import create_provider
        overridden = copy.deepcopy(config)
        if spec.provider:
            overridden.agent.provider = spec.provider
        if spec.model:
            overridden.agent.model = spec.model
        if spec.temperature is not None:
            overridden.agent.temperature = spec.temperature
        if spec.max_tokens is not None:
            overridden.agent.max_tokens = spec.max_tokens
        return create_provider(overridden)

    def _resolve_skills(
        self,
        spec: SubAgentSpec,
        skill_loader: SkillLoader,
    ) -> SkillLoader:
        """Return the appropriate SkillLoader for this sub-agent.

        - spec.skills is None  -> inherit all skills from parent loader
        - spec.skills is a list -> create subset with only those skills
        """
        if spec.skills is None:
            return skill_loader
        return skill_loader.create_subset(spec.skills)

    def _get_manager_id(self) -> str:
        return f"manager_{self.project_id}"

    def _build_system_prompt(self) -> str:
        tools = self._skill_loader.get_tools()
        if tools:
            tools_text = "\n\nAvailable tools:\n" + "\n".join(
                f"- {t.name}: {t.description}" for t in tools
            )
            return self.spec.task_description + tools_text
        return self.spec.task_description

    async def run(self) -> None:
        """Main event loop — pull tasks from kanban, process, push results."""
        self._running = True

        sn_filter = (
            f"AND _tp_sn > {self._checkpoint_sn}"
            if self._checkpoint_sn > 0
            else ""
        )
        query = f"""
        SELECT *, _tp_sn FROM pulsebot.kanban
        WHERE target_id = '{self.agent_id}'
        AND project_id = '{self.project_id}'
        AND msg_type IN ('task', 'control')
        {sn_filter}
        SETTINGS seek_to='latest'
        """

        logger.info(f"SubAgent {self.agent_id} starting kanban loop")

        async for message in self.kanban_reader.stream(query):
            if not self._running:
                break

            msg_type = message.get("msg_type", "")
            try:
                if msg_type == "control":
                    await self._handle_control(message)
                elif msg_type == "task":
                    await self._process_task(message)
            except Exception as e:
                logger.error(
                    f"SubAgent {self.agent_id} error processing message: {e}",
                    exc_info=True,
                )
                await self._write_error(message, str(e))

            self._checkpoint_sn = message.get("_tp_sn", self._checkpoint_sn)
            await self._persist_checkpoint()

    async def _handle_control(self, message: dict[str, Any]) -> None:
        """Handle control messages (cancel, pause, resume)."""
        command = message.get("content", "").strip().lower()
        if command == "cancel":
            logger.info(f"SubAgent {self.agent_id} received cancel")
            self._running = False
        else:
            logger.warning(f"SubAgent {self.agent_id} unknown control: {command!r}")

    async def _process_task(self, message: dict[str, Any]) -> None:
        """Process a task message: run LLM loop, write result to kanban."""
        content = message.get("content", "")
        system_prompt = self._build_system_prompt()

        result_text = await self._reason(system_prompt, content)

        targets = self.spec.target_agents or [self._get_manager_id()]
        for target in targets:
            await self.kanban_writer.write({
                "project_id": self.project_id,
                "sender_id": self.agent_id,
                "target_id": target,
                "msg_type": "result",
                "content": result_text,
                "metadata": json.dumps({
                    "source_msg_id": message.get("msg_id", ""),
                }),
            })

    async def _reason(self, system_prompt: str, user_content: str) -> str:
        """Run the LLM + tool loop for a single task. Returns final text."""
        raw_tools = self._skill_loader.get_tools()
        tools = self.llm.get_tool_definitions(raw_tools) if raw_tools else None

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": user_content}
        ]

        response = None
        for _ in range(self.spec.max_iterations):
            response = await self.llm.chat(
                messages=messages,
                system=system_prompt,
                tools=tools,
            )

            if response.tool_calls:
                # Add assistant turn with tool calls
                tool_call_dicts = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments),
                        },
                    }
                    for tc in response.tool_calls
                ]
                messages.append({
                    "role": "assistant",
                    "content": response.content or "",
                    "tool_calls": tool_call_dicts,
                })

                # Execute tools and add results
                for tc in response.tool_calls:
                    result = await self.executor.execute(
                        tool_name=tc.name,
                        arguments=tc.arguments,
                        session_id=f"{self.project_id}:{self.agent_id}",
                    )
                    result_str = (
                        str(result.get("output", ""))
                        if result.get("success")
                        else f"Error: {result.get('error', '')}"
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result_str,
                    })
            else:
                return response.content or ""

        # Max iterations reached — return last content
        return response.content or "" if response is not None else ""

    async def _write_error(self, source_message: dict[str, Any], error: str) -> None:
        """Write an error message to kanban targeting the manager."""
        await self.kanban_writer.write({
            "project_id": self.project_id,
            "sender_id": self.agent_id,
            "target_id": self._get_manager_id(),
            "msg_type": "error",
            "content": error,
            "metadata": json.dumps({
                "source_msg_id": source_message.get("msg_id", ""),
            }),
        })

    async def _load_checkpoint(self) -> int:
        """Load last checkpoint from kanban_agents stream."""
        rows = self._batch_client.query(f"""
            SELECT checkpoint_sn FROM table(pulsebot.kanban_agents)
            WHERE agent_id = '{self.agent_id}'
            AND project_id = '{self.project_id}'
            ORDER BY timestamp DESC LIMIT 1
        """)
        return rows[0]["checkpoint_sn"] if rows else 0

    async def _persist_checkpoint(self) -> None:
        """Write current checkpoint to agent metadata stream."""
        await self.agents_writer.write({
            "agent_id": self.agent_id,
            "project_id": self.project_id,
            "name": self.spec.name,
            "role": self.spec.role,
            "task_description": self.spec.task_description,
            "target_agents": self.spec.target_agents,
            "status": "running",
            "skills": self.spec.skills or [],
            "skill_overrides": json.dumps(self.spec.skill_overrides or {}),
            "config": json.dumps({
                "model": self.spec.model,
                "provider": self.spec.provider,
                "temperature": self.spec.temperature,
                "max_tokens": self.spec.max_tokens,
                "max_iterations": self.spec.max_iterations,
                "enable_memory": self.spec.enable_memory,
            }),
            "checkpoint_sn": self._checkpoint_sn,
        })

    async def stop(self) -> None:
        """Stop this sub-agent and persist final checkpoint."""
        self._running = False
        await self._persist_checkpoint()
