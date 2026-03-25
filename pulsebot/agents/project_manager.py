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
from pulsebot.timeplus.client import escape_sql_str
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
        self._busy_projects: set[str] = set()   # project_ids with a run in progress

        # Dedicated batch client for metadata writes (kanban streams don't have
        # a generic 'id' column, so we use client.insert directly rather than
        # StreamWriter which auto-injects 'id').
        self._batch_client = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )

        # Schedule recovery of any scheduled projects that were running before
        # a restart. Runs asynchronously so __init__ stays synchronous.
        asyncio.create_task(
            self._recover_scheduled_projects(),
            name="recover_scheduled_projects",
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
        manager_id = f"manager_{project_id}"
        initial_messages = initial_messages or []

        # Set project_id on all specs
        for spec in agents:
            spec.project_id = project_id

        # Resolve target_agents: convert human-readable names to agent IDs.
        # Also add manager aliases so workers can write target_agents: ["Manager"].
        name_to_id = {spec.name: spec.agent_id for spec in agents}
        name_to_id["Manager"] = manager_id
        name_to_id["manager"] = manager_id
        for spec in agents:
            spec.target_agents = [name_to_id.get(t, t) for t in spec.target_agents]

        # Calculate fan-in: which agents send tasks to each agent.
        # Agents with multiple upstream senders must buffer until one message
        # from each upstream has arrived before synthesizing.
        upstream: dict[str, list[str]] = {spec.agent_id: [] for spec in agents}
        for spec in agents:
            for target_id in spec.target_agents:
                if target_id in upstream:
                    upstream[target_id].append(spec.agent_id)
        for spec in agents:
            spec.upstream_agent_ids = upstream[spec.agent_id]

        # Workers that report directly to the manager: those with no
        # target_agents (defaults to manager) or explicitly targeting the manager.
        reporting_agent_ids = [
            spec.agent_id for spec in agents
            if not spec.target_agents or manager_id in spec.target_agents
        ]

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
            reporting_agent_ids=reporting_agent_ids,
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
        state = self._projects.get(project_id)
        if exists_in_mem and state is not None:
            for agent_id in state.agent_ids:
                task = self._agent_tasks.pop(agent_id, None)
                if task and not task.done():
                    task.cancel()
            del self._projects[project_id]

        # Clear busy state
        self._busy_projects.discard(project_id)

        # Drop associated Timeplus Task for scheduled projects
        if state is not None and state.is_scheduled:
            from pulsebot.timeplus.tasks import TaskManager
            task_manager = TaskManager(self._batch_client)
            task_name = task_manager._sanitise_task_name(state.name)
            try:
                task_manager.drop_task(task_name)
            except Exception as e:
                logger.warning(
                    f"Could not drop Timeplus task '{task_name}' for project "
                    f"{project_id}: {e}"
                )

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
        is_scheduled: bool = False,
        schedule_type: str = "",
        schedule_expr: str = "",
        trigger_prompt: str = "",
    ) -> None:
        self._batch_client.insert("pulsebot.kanban_projects", [{
            "project_id": project_id,
            "name": name,
            "description": description,
            "status": "active",
            "created_by": "main",
            "session_id": session_id,
            "agent_ids": [s.agent_id for s in agents],
            "is_scheduled": is_scheduled,
            "schedule_type": schedule_type,
            "schedule_expr": schedule_expr,
            "trigger_prompt": trigger_prompt,
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

    # ── Scheduled project support ──────────────────────────────────────────────

    async def create_scheduled_project(
        self,
        name: str,
        description: str,
        agents: list[SubAgentSpec],
        session_id: str,
        schedule_type: str,
        schedule_expr: str,
        trigger_prompt: str,
        initial_messages: list[dict[str, Any]] | None = None,
        api_url: str | None = None,
    ) -> str:
        """Create a scheduled multi-agent project with long-running agents.

        Identical to create_project but marks the project as scheduled,
        sets up the Timeplus Task trigger, and wires the on_run_complete
        callback into the manager agent.

        Args:
            name: Human-readable project name.
            description: What this project accomplishes.
            agents: Worker agent specs.
            session_id: Session for routing final output to the user.
            schedule_type: 'interval' or 'cron'.
            schedule_expr: e.g. '30m' or '0 9 * * 1-5'.
            trigger_prompt: Instruction sent to the manager on each trigger.
            initial_messages: Optional messages dispatched on first run only.
            api_url: Base URL for the Timeplus Task UDF to call back.
                Defaults to config.workspace.api_server_url.

        Returns:
            The generated project_id.

        Raises:
            ValueError: If schedule_type is invalid, schedule_expr is empty,
                        or agent/project limits are exceeded.
        """
        if schedule_type not in ("interval", "cron"):
            raise ValueError(
                f"Invalid schedule_type '{schedule_type}'. Must be 'interval' or 'cron'."
            )
        if not schedule_expr.strip():
            raise ValueError("schedule_expr must not be empty.")

        max_agents = self.config.multi_agent.max_agents_per_project
        if len(agents) > max_agents:
            raise ValueError(f"Too many agents: {len(agents)} > max {max_agents}")
        max_projects = self.config.multi_agent.max_concurrent_projects
        active = sum(1 for p in self._projects.values() if p.status == "active")
        if active >= max_projects:
            raise ValueError(
                f"Too many concurrent projects: {active} >= max {max_projects}"
            )

        project_id = f"proj_{uuid.uuid4().hex[:12]}"
        manager_id = f"manager_{project_id}"
        initial_messages = initial_messages or []

        for spec in agents:
            spec.project_id = project_id
            spec.is_scheduled = True

        name_to_id = {spec.name: spec.agent_id for spec in agents}
        name_to_id["Manager"] = manager_id
        name_to_id["manager"] = manager_id
        for spec in agents:
            spec.target_agents = [name_to_id.get(t, t) for t in spec.target_agents]

        upstream: dict[str, list[str]] = {spec.agent_id: [] for spec in agents}
        for spec in agents:
            for target_id in spec.target_agents:
                if target_id in upstream:
                    upstream[target_id].append(spec.agent_id)
        for spec in agents:
            spec.upstream_agent_ids = upstream[spec.agent_id]

        reporting_agent_ids = [
            spec.agent_id for spec in agents
            if not spec.target_agents or manager_id in spec.target_agents
        ]

        manager_spec = SubAgentSpec(
            name="Manager",
            agent_id=manager_id,
            role="manager",
            task_description=(
                "You are the project manager for a scheduled recurring project. "
                "Coordinate worker agents, collect their results, and deliver "
                "the final output. You will be triggered repeatedly on schedule."
            ),
            project_id=project_id,
            target_agents=[],
            skills=[],
            is_scheduled=True,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            trigger_prompt=trigger_prompt,
        )

        self._write_project_metadata(
            project_id, name, description, agents, session_id,
            is_scheduled=True,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            trigger_prompt=trigger_prompt,
        )
        for spec in [manager_spec] + agents:
            self._write_agent_metadata(spec)

        state = ProjectState(
            project_id=project_id,
            name=name,
            description=description,
            session_id=session_id,
            agent_ids=[manager_id] + [spec.agent_id for spec in agents],
            is_scheduled=True,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            trigger_prompt=trigger_prompt,
        )
        self._projects[project_id] = state

        manager = ManagerAgent(
            spec=manager_spec,
            worker_specs=agents,
            session_id=session_id,
            timeplus=self.timeplus,
            llm_provider=self.llm,
            skill_loader=self.skills,
            config=self.config,
            initial_messages=initial_messages,
            reporting_agent_ids=reporting_agent_ids,
            on_run_complete=lambda: self.mark_project_idle(project_id),
        )
        self._agent_tasks[manager_id] = asyncio.create_task(
            manager.run(), name=f"manager_{project_id}"
        )

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

        # Create the Timeplus Task that will fire triggers on schedule
        resolved_api_url = api_url or self.config.workspace.api_server_url
        from pulsebot.timeplus.tasks import TaskManager
        task_manager = TaskManager(self._batch_client)
        if schedule_type == "interval":
            task_manager.create_project_interval_task(
                project_id=project_id,
                project_name=name,
                trigger_prompt=trigger_prompt,
                interval=schedule_expr,
                api_url=resolved_api_url,
            )
        else:
            task_manager.create_project_cron_task(
                project_id=project_id,
                project_name=name,
                trigger_prompt=trigger_prompt,
                cron=schedule_expr,
                api_url=resolved_api_url,
            )

        logger.info(
            f"Scheduled project {project_id} created ({schedule_type}: {schedule_expr})",
            extra={"project_id": project_id, "session_id": session_id},
        )
        return project_id

    def trigger_project(self, project_id: str, trigger_prompt: str | None = None) -> bool:
        """Attempt to trigger a scheduled project run.

        Checks whether the project is busy (run already in progress). If not,
        marks it busy and writes a 'trigger' message to the kanban stream for
        the manager to pick up.

        This method contains no await — the busy check and add are atomic
        from asyncio's perspective (no yield point between check and add).

        Args:
            project_id: The project to trigger.
            trigger_prompt: Instruction for this run; falls back to stored
                            trigger_prompt from ProjectState.

        Returns:
            True if the trigger was accepted; False if the project is busy or
            not found.
        """
        if project_id in self._busy_projects:
            logger.info(f"Project {project_id} is busy, trigger skipped")
            return False

        state = self._projects.get(project_id)
        if state is None:
            return False

        prompt = trigger_prompt or state.trigger_prompt
        self._busy_projects.add(project_id)

        manager_id = f"manager_{project_id}"
        self._batch_client.insert("pulsebot.kanban", [{
            "project_id": project_id,
            "sender_id": "scheduler",
            "target_id": manager_id,
            "msg_type": "trigger",
            "content": json.dumps({"prompt": prompt, "project_id": project_id}),
        }])

        logger.info(
            f"Trigger sent to project {project_id}",
            extra={"project_id": project_id, "manager_id": manager_id},
        )
        return True

    def mark_project_idle(self, project_id: str) -> None:
        """Clear the busy flag for a project after a run completes."""
        self._busy_projects.discard(project_id)
        logger.info(f"Project {project_id} is now idle")

    def is_project_busy(self, project_id: str) -> bool:
        """Return True if the project currently has a run in progress."""
        return project_id in self._busy_projects

    async def _recover_scheduled_projects(self) -> None:
        """Re-spawn agents for all scheduled projects on server startup.

        Queries kanban_projects for active scheduled projects, reads the
        latest checkpoint_sn per agent from kanban_agents, and re-creates
        the asyncio tasks so agents resume from where they left off.
        """
        try:
            rows = self._batch_client.query("""
                SELECT project_id, name, description, session_id,
                       schedule_type, schedule_expr, trigger_prompt, agent_ids
                FROM table(pulsebot.kanban_projects)
                WHERE is_scheduled = true AND status = 'active'
                ORDER BY timestamp DESC
                LIMIT 1 BY project_id
            """)
        except Exception as e:
            logger.warning(f"Could not query scheduled projects for recovery: {e}")
            return

        if not rows:
            logger.info("No scheduled projects to recover")
            return

        for row in rows:
            project_id = row["project_id"]
            if project_id in self._projects:
                logger.debug(f"Project {project_id} already in memory, skipping recovery")
                continue

            try:
                await self._recover_project(row)
            except Exception as e:
                logger.error(
                    f"Failed to recover scheduled project {project_id}: {e}",
                    exc_info=True,
                )

    async def _recover_project(self, row: dict[str, Any]) -> None:
        """Re-spawn agents for a single recovered scheduled project."""
        project_id = row["project_id"]
        name = row.get("name", "")
        description = row.get("description", "")
        session_id = row.get("session_id", "")
        schedule_type = row.get("schedule_type", "interval")
        schedule_expr = row.get("schedule_expr", "")
        trigger_prompt = row.get("trigger_prompt", "")

        # Load agent metadata
        try:
            agent_rows = self._batch_client.query(f"""
                SELECT agent_id, name, role, task_description, target_agents,
                       skills, skill_overrides, config, checkpoint_sn
                FROM table(pulsebot.kanban_agents)
                WHERE project_id = '{escape_sql_str(project_id)}'
                ORDER BY timestamp DESC
                LIMIT 1 BY agent_id
            """)
        except Exception as e:
            logger.warning(
                f"Could not load agent metadata for project {project_id}: {e}"
            )
            return

        if not agent_rows:
            logger.warning(f"No agents found for project {project_id}, skipping")
            return

        manager_id = f"manager_{project_id}"
        manager_row = next((r for r in agent_rows if r["agent_id"] == manager_id), None)
        worker_rows = [r for r in agent_rows if r["agent_id"] != manager_id]

        def _build_spec(r: dict[str, Any]) -> SubAgentSpec:
            cfg = json.loads(r.get("config", "{}"))
            return SubAgentSpec(
                name=r["name"],
                agent_id=r["agent_id"],
                role=r.get("role", "worker"),
                task_description=r.get("task_description", ""),
                project_id=project_id,
                target_agents=list(r.get("target_agents", [])),
                skills=list(r.get("skills", [])),
                skill_overrides=json.loads(r.get("skill_overrides", "{}")),
                model=cfg.get("model"),
                provider=cfg.get("provider"),
                temperature=cfg.get("temperature"),
                max_tokens=cfg.get("max_tokens"),
                max_iterations=cfg.get("max_iterations", 5),
                enable_memory=cfg.get("enable_memory", False),
                checkpoint_sn=r.get("checkpoint_sn", 0),
                is_scheduled=True,
                schedule_type=schedule_type,
                schedule_expr=schedule_expr,
                trigger_prompt=trigger_prompt,
            )

        worker_specs = [_build_spec(r) for r in worker_rows]

        manager_spec_data = manager_row or {}
        manager_spec = SubAgentSpec(
            name="Manager",
            agent_id=manager_id,
            role="manager",
            task_description=manager_spec_data.get("task_description", ""),
            project_id=project_id,
            target_agents=[],
            skills=[],
            checkpoint_sn=manager_spec_data.get("checkpoint_sn", 0),
            is_scheduled=True,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            trigger_prompt=trigger_prompt,
        )

        reporting_agent_ids = [
            spec.agent_id for spec in worker_specs
            if not spec.target_agents or manager_id in spec.target_agents
        ]

        state = ProjectState(
            project_id=project_id,
            name=name,
            description=description,
            session_id=session_id,
            agent_ids=[manager_id] + [s.agent_id for s in worker_specs],
            is_scheduled=True,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            trigger_prompt=trigger_prompt,
        )
        self._projects[project_id] = state

        # Spawn manager (skip if already running)
        if manager_id not in self._agent_tasks or self._agent_tasks[manager_id].done():
            manager = ManagerAgent(
                spec=manager_spec,
                worker_specs=worker_specs,
                session_id=session_id,
                timeplus=self.timeplus,
                llm_provider=self.llm,
                skill_loader=self.skills,
                config=self.config,
                reporting_agent_ids=reporting_agent_ids,
                on_run_complete=lambda: self.mark_project_idle(project_id),
            )
            self._agent_tasks[manager_id] = asyncio.create_task(
                manager.run(), name=f"manager_{project_id}"
            )

        # Spawn workers (skip already running)
        for spec in worker_specs:
            if spec.agent_id not in self._agent_tasks or self._agent_tasks[spec.agent_id].done():
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
            f"Recovered scheduled project {project_id} "
            f"({schedule_type}: {schedule_expr}) with "
            f"{len(worker_specs)} worker(s)"
        )
