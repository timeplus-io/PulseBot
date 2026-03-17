# pulsebot/agents/project_manager.py
"""ProjectManager: creates, monitors, and cancels multi-agent projects."""

from __future__ import annotations

import asyncio
import json
import uuid
from typing import TYPE_CHECKING, Any

from pulsebot.agents.manager_agent import ManagerAgent
from pulsebot.agents.models import ProjectState, SubAgentSpec
from pulsebot.agents.sub_agent import SubAgent
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.config import Config
    from pulsebot.core.executor import ToolExecutor
    from pulsebot.providers.base import LLMProvider
    from pulsebot.skills.loader import SkillLoader
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


class ProjectManager:
    """
    Manages the lifecycle of multi-agent projects.

    Provides create/cancel/status operations used by the project_manager skill.
    Each project spawns a ManagerAgent + worker SubAgents as asyncio tasks.
    """

    def __init__(
        self,
        config: Config,
        timeplus: TimeplusClient,
        llm_provider: LLMProvider,
        skill_loader: SkillLoader,
        executor: ToolExecutor,
    ) -> None:
        from pulsebot.timeplus.client import TimeplusClient

        self.config = config
        self.timeplus = timeplus
        self.llm = llm_provider
        self.skills = skill_loader
        self.executor = executor

        self._projects: dict[str, ProjectState] = {}
        self._agent_tasks: dict[str, asyncio.Task] = {}

        # Dedicated batch client for metadata writes (kanban streams don't have
        # a generic 'id' column, so we use client.insert directly rather than
        # StreamWriter which auto-injects 'id').
        self._batch_client = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )

    async def create_project(
        self,
        name: str,
        description: str,
        agents: list[SubAgentSpec],
        session_id: str,
        initial_messages: list[dict[str, Any]] | None = None,
    ) -> str:
        """Create a new project, persist metadata, and spawn all agents.

        Returns:
            The generated project_id.

        Raises:
            ValueError: If agent or project limits are exceeded.
        """
        max_agents = self.config.multi_agent.max_agents_per_project
        if len(agents) > max_agents:
            raise ValueError(
                f"Too many agents: {len(agents)} > max {max_agents}"
            )
        max_projects = self.config.multi_agent.max_concurrent_projects
        active = sum(1 for p in self._projects.values() if p.status == "active")
        if active >= max_projects:
            raise ValueError(
                f"Too many concurrent projects: {active} >= max {max_projects}"
            )

        project_id = f"proj_{uuid.uuid4().hex[:12]}"
        initial_messages = initial_messages or []

        # Set project_id on all specs
        for spec in agents:
            spec.project_id = project_id

        # Resolve target_agents: convert human-readable names to agent IDs
        # e.g. "Analyst" -> "agent_analyst", "manager" stays as-is
        name_to_id = {spec.name: spec.agent_id for spec in agents}
        for spec in agents:
            spec.target_agents = [name_to_id.get(t, t) for t in spec.target_agents]

        manager_spec = SubAgentSpec(
            name="Manager",
            agent_id=f"manager_{project_id}",
            role="manager",
            task_description=(
                "You are the project manager. Coordinate worker agents, "
                "collect their results, and deliver the final output."
            ),
            project_id=project_id,
            target_agents=[],
            skills=[],
        )

        # Persist project and agent metadata
        await self._write_project_metadata(
            project_id, name, description, agents, session_id
        )
        for spec in [manager_spec] + agents:
            await self._write_agent_metadata(spec)

        # Track state
        self._projects[project_id] = ProjectState(
            project_id=project_id,
            name=name,
            description=description,
            session_id=session_id,
            agent_ids=[manager_spec.agent_id] + [spec.agent_id for spec in agents],
        )

        # Spawn Manager Agent
        manager = ManagerAgent(
            spec=manager_spec,
            worker_specs=agents,
            session_id=session_id,
            timeplus=self.timeplus,
            llm_provider=self.llm,
            skill_loader=self.skills,
            executor=self.executor,
            config=self.config,
            initial_messages=initial_messages,
        )
        self._agent_tasks[manager_spec.agent_id] = asyncio.create_task(
            manager.run(), name=f"manager_{project_id}"
        )

        # Spawn worker sub-agents
        for spec in agents:
            agent = SubAgent(
                spec=spec,
                timeplus=self.timeplus,
                llm_provider=self.llm,
                skill_loader=self.skills,
                executor=self.executor,
                config=self.config,
            )
            self._agent_tasks[spec.agent_id] = asyncio.create_task(
                agent.run(), name=spec.agent_id
            )

        logger.info(
            f"Project {project_id} created with {len(agents)} worker(s)",
            extra={"project_id": project_id, "session_id": session_id},
        )
        return project_id

    def list_projects(self, status: str | None = None) -> list[dict[str, Any]]:
        """Return summary dicts for all tracked projects.

        Args:
            status: Optional filter ('active', 'completed', 'failed', 'cancelled').
        """
        result = []
        for state in self._projects.values():
            if status is None or state.status == status:
                result.append({
                    "project_id": state.project_id,
                    "name": state.name,
                    "description": state.description,
                    "status": state.status,
                    "agent_count": len(state.agent_ids),
                    "session_id": state.session_id,
                })
        return result

    def get_project_status(self, project_id: str) -> dict[str, Any] | None:
        """Return detailed status for a specific project, or None if not found."""
        state = self._projects.get(project_id)
        if state is None:
            return None
        return {
            "project_id": state.project_id,
            "name": state.name,
            "description": state.description,
            "status": state.status,
            "agent_ids": state.agent_ids,
            "session_id": state.session_id,
        }

    async def cancel_project(self, project_id: str) -> bool:
        """Cancel a running project by cancelling all asyncio tasks.

        Returns:
            True if project was found and cancelled.
        """
        state = self._projects.get(project_id)
        if state is None:
            return False

        for agent_id in state.agent_ids:
            task = self._agent_tasks.pop(agent_id, None)
            if task and not task.done():
                task.cancel()

        state.status = "cancelled"
        logger.info(f"Project {project_id} cancelled")
        return True

    async def _write_project_metadata(
        self,
        project_id: str,
        name: str,
        description: str,
        agents: list[SubAgentSpec],
        session_id: str,
    ) -> None:
        self._batch_client.insert("pulsebot.kanban_projects", [{
            "project_id": project_id,
            "name": name,
            "description": description,
            "status": "active",
            "created_by": "main",
            "session_id": session_id,
            "agent_ids": [s.agent_id for s in agents],
        }])

    async def _write_agent_metadata(self, spec: SubAgentSpec) -> None:
        self._batch_client.insert("pulsebot.kanban_agents", [{
            "agent_id": spec.agent_id,
            "project_id": spec.project_id,
            "name": spec.name,
            "role": spec.role,
            "task_description": spec.task_description,
            "target_agents": spec.target_agents,
            "status": "pending",
            "skills": spec.skills or [],
            "skill_overrides": json.dumps(spec.skill_overrides or {}),
            "config": json.dumps({
                "model": spec.model,
                "provider": spec.provider,
                "temperature": spec.temperature,
                "max_tokens": spec.max_tokens,
                "max_iterations": spec.max_iterations,
                "enable_memory": spec.enable_memory,
            }),
            "checkpoint_sn": 0,
        }])
