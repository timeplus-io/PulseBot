# pulsebot/agents/sub_agent.py
"""SubAgent: a worker agent that reads from kanban and writes results back."""

from __future__ import annotations

import asyncio
import datetime
import json
import time
from typing import TYPE_CHECKING, Any

from pulsebot.timeplus.client import escape_sql_str
from pulsebot.timeplus.event_writer import EventWriter
from pulsebot.timeplus.streams import StreamReader, StreamWriter
from pulsebot.utils import get_logger, truncate_string

if TYPE_CHECKING:
    from pulsebot.agents.models import SubAgentSpec
    from pulsebot.config import Config
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
        config: Config,
    ) -> None:
        from pulsebot.timeplus.client import TimeplusClient

        self.spec = spec
        self.agent_id = spec.agent_id
        self.project_id = spec.project_id

        # Resolve LLM provider (override model/provider if specified)
        self.llm = self._resolve_provider(spec, llm_provider, config)

        # Resolve skill set for this sub-agent and build a matching executor.
        # Tool definitions (sent to LLM) and tool execution must use the same
        # skill loader — sharing the main executor would cause a mismatch where
        # the LLM sees filtered tools but execution routes through the full set.
        self._skill_loader = self._resolve_skills(spec, skill_loader)
        from pulsebot.core.executor import ToolExecutor
        self.executor = ToolExecutor(self._skill_loader, events=None)

        # Each sub-agent needs its OWN dedicated clients to avoid
        # "Simultaneous queries on single connection" errors with the main
        # agent's messages stream reader (which shares the same TimeplusClient
        # instance passed in from ProjectManager).
        read_client = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )
        batch_client = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )

        self.kanban_reader = StreamReader(read_client, "kanban")
        # kanban streams use msg_id/agent_id, not the generic 'id' column that
        # StreamWriter auto-injects, so we write via client.insert() directly.

        self._checkpoint_sn: int = spec.checkpoint_sn
        self._running = False
        self._batch_client = batch_client
        self.events = EventWriter(
            StreamWriter(batch_client, "events"),
            default_source=f"subagent:{spec.agent_id}",
            default_tags=[f"agent:{spec.agent_id}", f"project:{spec.project_id}"],
        )
        self._llm_logger = StreamWriter(batch_client, "llm_logs")
        self._tool_logger = StreamWriter(batch_client, "tool_logs")
        # Record creation time so the kanban stream query starts from here,
        # capturing tasks dispatched during the startup race window.
        self._start_time = datetime.datetime.now(datetime.timezone.utc)

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
        - spec.skills is a list -> create subset with those skills + configured builtins
        """
        if spec.skills is None:
            return skill_loader
        return skill_loader.create_subset(spec.skills, builtin_skills=spec.builtin_skills)

    def _get_manager_id(self) -> str:
        return f"manager_{self.project_id}"

    def _build_system_prompt(self) -> str:
        parts = [self.spec.task_description]
        skills_index = self._skill_loader.format_skills_for_prompt()
        if skills_index:
            parts.append(skills_index)
        return "\n\n".join(parts)

    async def run(self) -> None:
        """Main event loop — pull tasks from kanban, process, push results."""
        self._running = True
        await self.events.emit("subagent.started", payload={
            "agent_id": self.agent_id,
            "project_id": self.project_id,
            "role": self.spec.role,
            "model": self.llm.model,
        })
        try:
            if self._checkpoint_sn > 0:
                # Resume from last checkpoint
                sn_filter = f"AND _tp_sn > {self._checkpoint_sn}"
                seek_to = "latest"
            else:
                # Use creation time so tasks dispatched during the race window
                # between ManagerAgent.run() dispatch and this query start are captured.
                sn_filter = ""
                seek_to = self._start_time.strftime('%Y-%m-%d %H:%M:%S')

            query = f"""
            SELECT *, _tp_sn FROM pulsebot.kanban
            WHERE target_id = '{escape_sql_str(self.agent_id)}'
            AND project_id = '{escape_sql_str(self.project_id)}'
            AND msg_type IN ('task', 'control')
            {sn_filter}
            SETTINGS seek_to='{seek_to}'
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
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    logger.error(
                        f"SubAgent {self.agent_id} error processing message: {e}",
                        exc_info=True,
                    )
                    await self._write_error(message, str(e))

                self._checkpoint_sn = message.get("_tp_sn", self._checkpoint_sn)
                await self._persist_checkpoint()
        except asyncio.CancelledError:
            # Clean shutdown: task was cancelled (either via kanban cancel message
            # or external ProjectManager.cancel_project). This is not an error.
            logger.info(f"SubAgent {self.agent_id} cancelled cleanly")
        except Exception as e:
            await self.events.emit_error("subagent.error", e, payload={
                "agent_id": self.agent_id,
                "project_id": self.project_id,
            })
            raise
        finally:
            await self._persist_checkpoint(status="cancelled")
            await self.events.emit("subagent.stopped", payload={
                "agent_id": self.agent_id,
                "project_id": self.project_id,
            })

    async def _handle_control(self, message: dict[str, Any]) -> None:
        """Handle control messages (cancel, pause, resume)."""
        command = message.get("content", "").strip().lower()
        if command == "cancel":
            logger.info(f"SubAgent {self.agent_id} received cancel")
            self._running = False
            # Cancel the current asyncio task so the stream loop exits immediately
            # rather than blocking indefinitely waiting for the next kanban message.
            task = asyncio.current_task()
            if task is not None:
                task.cancel()
        else:
            logger.warning(f"SubAgent {self.agent_id} unknown control: {command!r}")

    async def _process_task(self, message: dict[str, Any]) -> None:
        """Process a task message: run LLM loop, write result to kanban."""
        content = message.get("content", "")
        system_prompt = self._build_system_prompt()

        result_text = await self._reason(system_prompt, content)

        manager_id = self._get_manager_id()
        targets = self.spec.target_agents or [manager_id]
        for target in targets:
            # Use "task" when routing to another worker so it can pick it up,
            # "result" when routing to the manager which listens for results.
            msg_type = "result" if target == manager_id else "task"
            self._batch_client.insert("pulsebot.kanban", [{
                "project_id": self.project_id,
                "sender_id": self.agent_id,
                "target_id": target,
                "msg_type": msg_type,
                "content": result_text,
                "metadata": json.dumps({
                    "source_msg_id": message.get("msg_id", ""),
                }),
            }])

    async def _reason(self, system_prompt: str, user_content: str) -> str:
        """Run the LLM + tool loop for a single task. Returns final text."""
        raw_tools = self._skill_loader.get_tools()
        tools = self.llm.get_tool_definitions(raw_tools) if raw_tools else None

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": user_content}
        ]

        # Track recent tool calls to detect infinite loops
        recent_calls: list[tuple[str, str]] = []

        session_id = f"{self.project_id}:{self.agent_id}"
        response = None
        for _ in range(self.spec.max_iterations):
            t0 = time.monotonic()
            response = await self.llm.chat(
                messages=messages,
                system=system_prompt,
                tools=tools,
            )
            latency_ms = int((time.monotonic() - t0) * 1000)
            await self._log_llm_call(session_id, system_prompt, messages, response, latency_ms)

            if response.tool_calls:
                # Detect repeated identical tool calls (infinite loop guard)
                call_fingerprints = [
                    (tc.name, json.dumps(tc.arguments, sort_keys=True))
                    for tc in response.tool_calls
                ]
                if call_fingerprints == recent_calls:
                    logger.warning(
                        f"SubAgent {self.agent_id} detected repeated identical tool calls "
                        f"{[f for f, _ in call_fingerprints]}, forcing text response"
                    )
                    break
                recent_calls = call_fingerprints

                # Add assistant turn with tool calls.
                # Include tc.extra in the function dict so provider-specific
                # fields (e.g. Gemini's thought_signature) are preserved for
                # subsequent API calls.
                tool_call_dicts = []
                for tc in response.tool_calls:
                    tc_dict = {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments),
                        },
                    }
                    if tc.extra:
                        tc_dict["function"].update(tc.extra)
                    tool_call_dicts.append(tc_dict)
                messages.append({
                    "role": "assistant",
                    "content": response.content or "",
                    "tool_calls": tool_call_dicts,
                })

                # Execute tools and add results
                for tc in response.tool_calls:
                    t_tool = time.monotonic()
                    result = await self.executor.execute(
                        tool_name=tc.name,
                        arguments=tc.arguments,
                        session_id=session_id,
                    )
                    tool_duration_ms = int((time.monotonic() - t_tool) * 1000)
                    tool_success = result.get("success", False)
                    result_str = (
                        str(result.get("output", ""))
                        if tool_success
                        else f"Error: {result.get('error', '')}"
                    )
                    await self._log_tool_call(
                        session_id=session_id,
                        tool_name=tc.name,
                        arguments=tc.arguments,
                        result=result_str,
                        status="success" if tool_success else "error",
                        duration_ms=tool_duration_ms,
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result_str,
                    })
            else:
                return response.content or ""

        # Max iterations reached (or loop detected) while still in a tool call.
        # Force one final text-only response so the result is never empty.
        if response is not None and response.tool_calls:
            logger.warning(
                f"SubAgent {self.agent_id} hit iteration limit mid-tool-call, "
                "requesting final text synthesis"
            )
            messages.append({
                "role": "user",
                "content": (
                    "You have reached the maximum number of tool calls. "
                    "Based on the information gathered so far, please provide "
                    "your best response now as plain text."
                ),
            })
            try:
                final = await self.llm.chat(
                    messages=messages,
                    system=system_prompt,
                    tools=None,  # no tools — force a text response
                )
                return final.content or "(No response generated)"
            except Exception as e:
                logger.error(f"SubAgent {self.agent_id} final synthesis failed: {e}")
                return response.content or "(Max iterations reached with no text response)"

        return response.content or "" if response is not None else ""

    async def _log_llm_call(
        self,
        session_id: str,
        system_prompt: str,
        messages: list[dict[str, Any]],
        response: Any,
        latency_ms: int,
    ) -> None:
        usage = response.usage if response else None
        await self._llm_logger.write({
            "session_id": session_id,
            "model": self.llm.model,
            "provider": self.llm.provider_name,
            "input_tokens": usage.input_tokens if usage else 0,
            "output_tokens": usage.output_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
            "estimated_cost_usd": self.llm.estimate_cost(usage) if usage else 0.0,
            "latency_ms": latency_ms,
            "system_prompt_preview": truncate_string(system_prompt, 200),
            "user_message_preview": truncate_string(
                messages[-1].get("content", "") if messages else "", 200
            ),
            "assistant_response_preview": truncate_string(response.content or "", 200) if response else "",
            "full_response_content": response.content or "" if response else "",
            "messages_count": len(messages),
            "tools_called": [tc.name for tc in (response.tool_calls or [])] if response else [],
            "tool_call_count": len(response.tool_calls or []) if response else 0,
            "status": "success",
            "caller": self.agent_id,
        })

    async def _log_tool_call(
        self,
        session_id: str,
        tool_name: str,
        arguments: dict[str, Any],
        result: str,
        status: str,
        duration_ms: int,
    ) -> None:
        await self._tool_logger.write({
            "session_id": session_id,
            "llm_request_id": "",
            "tool_name": tool_name,
            "skill_name": tool_name.split("_")[0] if "_" in tool_name else tool_name,
            "arguments": json.dumps(arguments),
            "status": status,
            "result_preview": truncate_string(result, 500),
            "error_message": result if status == "error" else "",
            "duration_ms": duration_ms,
            "caller": self.agent_id,
        })

    async def _write_error(self, source_message: dict[str, Any], error: str) -> None:
        """Write an error message to kanban targeting the manager."""
        self._batch_client.insert("pulsebot.kanban", [{
            "project_id": self.project_id,
            "sender_id": self.agent_id,
            "target_id": self._get_manager_id(),
            "msg_type": "error",
            "content": error,
            "metadata": json.dumps({
                "source_msg_id": source_message.get("msg_id", ""),
            }),
        }])

    async def _load_checkpoint(self) -> int:
        """Load last checkpoint from kanban_agents stream."""
        rows = self._batch_client.query(f"""
            SELECT checkpoint_sn FROM table(pulsebot.kanban_agents)
            WHERE agent_id = '{escape_sql_str(self.agent_id)}'
            AND project_id = '{escape_sql_str(self.project_id)}'
            ORDER BY timestamp DESC LIMIT 1
        """)
        return rows[0]["checkpoint_sn"] if rows else 0

    async def _persist_checkpoint(self, status: str = "running") -> None:
        """Write current checkpoint to agent metadata stream."""
        self._batch_client.insert("pulsebot.kanban_agents", [{
            "agent_id": self.agent_id,
            "project_id": self.project_id,
            "name": self.spec.name,
            "role": self.spec.role,
            "task_description": self.spec.task_description,
            "target_agents": self.spec.target_agents,
            "status": status,
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
        }])

    async def stop(self) -> None:
        """Stop this sub-agent and persist final checkpoint."""
        self._running = False
        await self._persist_checkpoint(status="cancelled")
