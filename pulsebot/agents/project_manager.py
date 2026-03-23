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
        self._write_project_metadata(
            project_id, name, description, agents, session_id
        )
        for spec in [manager_spec] + agents:
            self._write_agent_metadata(spec)

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

        Queries kanban_projects stream for the latest state of each project so
        that results survive agent restarts.

        Args:
            status: Optional filter ('active', 'completed', 'failed', 'cancelled').
        """
        try:
            rows = self._batch_client.query("""
                SELECT project_id, name, description, status, session_id, timestamp
                FROM table(pulsebot.kanban_projects)
                ORDER BY timestamp DESC
                LIMIT 1 BY project_id
            """)
        except Exception as e:
            logger.warning(f"Failed to query kanban_projects: {e}")
            rows = []

        # Merge with in-memory state so live in-progress projects are included
        # even before their first DB write.
        seen: set[str] = set()
        result: list[dict[str, Any]] = []

        for row in rows:
            pid = row["project_id"]
            seen.add(pid)
            row_status = row.get("status", "")
            if status is None or row_status == status:
                # Count agents from in-memory state if available, else 0
                in_mem = self._projects.get(pid)
                agent_count = len(in_mem.agent_ids) if in_mem else 0
                result.append({
                    "project_id": pid,
                    "name": row.get("name", ""),
                    "description": row.get("description", ""),
                    "status": row_status,
                    "agent_count": agent_count,
                    "session_id": row.get("session_id", ""),
                })

        # Include any in-memory projects not yet flushed to the stream
        for state in self._projects.values():
            if state.project_id not in seen:
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
        from pulsebot.timeplus.client import escape_sql_str

        # Check in-memory first (live projects)
        state = self._projects.get(project_id)
        if state is not None:
            return {
                "project_id": state.project_id,
                "name": state.name,
                "description": state.description,
                "status": state.status,
                "agent_ids": state.agent_ids,
                "session_id": state.session_id,
            }

        # Fall back to stream for past projects
        try:
            rows = self._batch_client.query(f"""
                SELECT project_id, name, description, status, session_id
                FROM table(pulsebot.kanban_projects)
                WHERE project_id = '{escape_sql_str(project_id)}'
                ORDER BY timestamp DESC LIMIT 1
            """)
            if not rows:
                return None
            row = rows[0]

            # Fetch agent IDs from kanban_agents
            agent_rows = self._batch_client.query(f"""
                SELECT agent_id FROM table(pulsebot.kanban_agents)
                WHERE project_id = '{escape_sql_str(project_id)}'
                ORDER BY timestamp DESC LIMIT 1 BY agent_id
            """)
            agent_ids = [r["agent_id"] for r in agent_rows]

            return {
                "project_id": row["project_id"],
                "name": row.get("name", ""),
                "description": row.get("description", ""),
                "status": row.get("status", ""),
                "agent_ids": agent_ids,
                "session_id": row.get("session_id", ""),
            }
        except Exception as e:
            logger.warning(f"Failed to query project status from stream: {e}")
            return None

    async def delete_project(self, project_id: str) -> bool:
        """Cancel a running project (if active) and delete all its metadata from streams.

        Returns:
            True if the project existed and was deleted.
        """
        from pulsebot.timeplus.client import escape_sql_str

        pid = escape_sql_str(project_id)

        # Check existence: in-memory or DB
        exists_in_mem = project_id in self._projects
        if not exists_in_mem:
            try:
                rows = self._batch_client.query(f"""
                    SELECT project_id FROM table(pulsebot.kanban_projects)
                    WHERE project_id = '{pid}'
                    LIMIT 1
                """)
                if not rows:
                    return False
            except Exception as e:
                logger.warning(f"Could not verify project existence: {e}")
                return False

        # Cancel any running tasks
        if exists_in_mem:
            state = self._projects[project_id]
            for agent_id in state.agent_ids:
                task = self._agent_tasks.pop(agent_id, None)
                if task and not task.done():
                    task.cancel()
            del self._projects[project_id]

        # Delete from streams
        try:
            self._batch_client.execute(
                f"DELETE FROM pulsebot.kanban_projects WHERE project_id = '{pid}'"
            )
            self._batch_client.execute(
                f"DELETE FROM pulsebot.kanban_agents WHERE project_id = '{pid}'"
            )
            self._batch_client.execute(
                f"DELETE FROM pulsebot.kanban WHERE project_id = '{pid}'"
            )
        except Exception as e:
            logger.error(f"Failed to delete project {project_id} from streams: {e}")
            raise

        logger.info(f"Project {project_id} deleted")
        return True

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

    def _write_project_metadata(
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

    def _write_agent_metadata(self, spec: SubAgentSpec) -> None:
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
