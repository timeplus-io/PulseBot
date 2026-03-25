"""Built-in skill for creating and managing multi-agent projects."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult

if TYPE_CHECKING:
    from pulsebot.agents.project_manager import ProjectManager


class ProjectManagerSkill(BaseSkill):
    """Skill that exposes multi-agent project management tools to the main agent."""

    name = "project_manager"
    description = "Create and manage multi-agent projects that decompose complex tasks"

    def __init__(self, project_manager: ProjectManager) -> None:
        self._pm = project_manager

    def get_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="create_project",
                description=(
                    "Create a new multi-agent project. Spawns a manager agent "
                    "and worker sub-agents that collaborate via a kanban stream. "
                    "Use for complex tasks that benefit from parallel or sequential "
                    "decomposition (research + analysis + writing, etc.)."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Short human-readable project name",
                        },
                        "description": {
                            "type": "string",
                            "description": "What this project aims to accomplish",
                        },
                        "agents": {
                            "type": "array",
                            "description": "Worker agent specifications",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "Agent name (used to derive agent_id)"},
                                    "task_description": {"type": "string", "description": "System-level role instructions"},
                                    "target_agents": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Agent IDs that receive this agent's output. Empty = send to manager.",
                                    },
                                    "skills": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Skill names to load. Omit to inherit all main agent skills.",
                                    },
                                    "builtin_skills": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Builtin skills always available to this agent (default: file_ops, shell, workspace). Only applies when 'skills' is set.",
                                    },
                                    "model": {"type": "string", "description": "Override LLM model"},
                                    "provider": {"type": "string", "description": "Override LLM provider"},
                                },
                                "required": ["name", "task_description", "target_agents"],
                            },
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Current user session ID (for routing final result back to user)",
                        },
                        "initial_messages": {
                            "type": "array",
                            "description": "Initial task messages dispatched by the manager",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "target": {"type": "string", "description": "Agent ID to send task to"},
                                    "content": {"type": "string", "description": "Task content"},
                                },
                                "required": ["target", "content"],
                            },
                        },
                    },
                    "required": ["name", "description", "agents", "session_id"],
                },
            ),
            ToolDefinition(
                name="list_projects",
                description="List all active and recent multi-agent projects.",
                parameters={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["active", "completed", "failed", "cancelled"],
                            "description": "Filter by status. Omit to list all.",
                        },
                    },
                },
            ),
            ToolDefinition(
                name="cancel_project",
                description="Cancel a running multi-agent project and stop all its agents.",
                parameters={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string", "description": "Project ID to cancel"},
                    },
                    "required": ["project_id"],
                },
            ),
            ToolDefinition(
                name="get_project_status",
                description="Get detailed status of a specific project including all agent states.",
                parameters={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string", "description": "Project ID"},
                    },
                    "required": ["project_id"],
                },
            ),
            ToolDefinition(
                name="delete_project",
                description=(
                    "Cancel a project (if still running) and permanently delete all its metadata "
                    "from the projects, agents, and kanban message streams."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string", "description": "Project ID to delete"},
                    },
                    "required": ["project_id"],
                },
            ),
            ToolDefinition(
                name="create_event_driven_project",
                description=(
                    "Create a multi-agent project triggered by rows from a Proton streaming SQL query. "
                    "Each matching row fires one workflow run (drop-on-busy — events arriving during an "
                    "active run are skipped). The context field value is appended to the trigger prompt "
                    "for every run."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Human-readable project name"},
                        "description": {"type": "string", "description": "What this project accomplishes"},
                        "agents": {
                            "type": "array",
                            "description": "Worker agent specs",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "role": {"type": "string"},
                                    "skills": {"type": "array", "items": {"type": "string"}},
                                },
                                "required": ["name", "role"],
                            },
                        },
                        "session_id": {"type": "string", "description": "Session for routing output"},
                        "event_query": {
                            "type": "string",
                            "description": (
                                "Complete Proton streaming SQL to subscribe to. Must SELECT the context_field "
                                "column directly from a stream or view — nested subqueries are not supported "
                                "because _tp_sn may not propagate through subquery boundaries."
                            ),
                        },
                        "context_field": {
                            "type": "string",
                            "description": "Column name in the query result to extract as trigger context",
                        },
                        "trigger_prompt": {
                            "type": "string",
                            "description": (
                                "Instruction prefix prepended to the extracted context value: "
                                '"{trigger_prompt}\\n\\n{context_value}"'
                            ),
                        },
                        "initial_messages": {
                            "type": "array",
                            "description": "Optional messages dispatched once on project creation",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["name", "description", "agents", "session_id", "event_query", "context_field", "trigger_prompt"],
                },
            ),
            ToolDefinition(
                name="create_scheduled_project",
                description=(
                    "Create a scheduled multi-agent project that runs repeatedly on a timer. "
                    "Spawns long-running agents that idle between scheduled executions and resume "
                    "after restarts via checkpointing. Use for recurring analysis, monitoring, or "
                    "reporting tasks (e.g. daily summaries, hourly data checks)."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Short human-readable project name",
                        },
                        "description": {
                            "type": "string",
                            "description": "What this project aims to accomplish",
                        },
                        "agents": {
                            "type": "array",
                            "description": "Worker agent specifications",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "Agent name (used to derive agent_id)"},
                                    "task_description": {"type": "string", "description": "System-level role instructions"},
                                    "target_agents": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Agent IDs that receive this agent's output. Empty = send to manager.",
                                    },
                                    "skills": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Skill names to load. Omit to inherit all main agent skills.",
                                    },
                                    "builtin_skills": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Builtin skills always available to this agent (default: file_ops, shell, workspace). Only applies when 'skills' is set.",
                                    },
                                    "model": {"type": "string", "description": "Override LLM model"},
                                    "provider": {"type": "string", "description": "Override LLM provider"},
                                },
                                "required": ["name", "task_description", "target_agents"],
                            },
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Current user session ID (for routing results back to user)",
                        },
                        "schedule_type": {
                            "type": "string",
                            "enum": ["interval", "cron"],
                            "description": "Scheduling mechanism: 'interval' for fixed intervals (e.g. '30m', '2h'), 'cron' for calendar schedules (e.g. '0 9 * * 1-5')",
                        },
                        "schedule_expr": {
                            "type": "string",
                            "description": "Schedule expression. For interval: '15m', '1h', '30s'. For cron: standard 5-field cron (minute hour dom month dow).",
                        },
                        "trigger_prompt": {
                            "type": "string",
                            "description": "Default instruction sent to worker agents on each scheduled execution",
                        },
                        "initial_messages": {
                            "type": "array",
                            "description": "Optional task messages dispatched immediately on project creation (before first scheduled run)",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "target": {"type": "string", "description": "Agent name to send task to"},
                                    "content": {"type": "string", "description": "Task content"},
                                },
                                "required": ["target", "content"],
                            },
                        },
                    },
                    "required": ["name", "description", "agents", "session_id", "schedule_type", "schedule_expr", "trigger_prompt"],
                },
            ),
        ]

    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        try:
            if tool_name == "create_project":
                return await self._create_project(arguments)
            elif tool_name == "list_projects":
                return self._list_projects(arguments)
            elif tool_name == "cancel_project":
                return await self._cancel_project(arguments)
            elif tool_name == "get_project_status":
                return self._get_project_status(arguments)
            elif tool_name == "delete_project":
                return await self._delete_project(arguments)
            elif tool_name == "create_scheduled_project":
                return await self._create_scheduled_project(arguments)
            elif tool_name == "create_event_driven_project":
                return await self._create_event_driven_project(arguments)
            else:
                return ToolResult.fail(f"Unknown tool: {tool_name}")
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _create_project(self, args: dict) -> ToolResult:
        from pulsebot.agents.models import SubAgentSpec

        raw_agents = args.get("agents", [])
        specs = [
            SubAgentSpec(
                name=a["name"],
                task_description=a["task_description"],
                project_id="",  # set by ProjectManager
                target_agents=a.get("target_agents", []),
                skills=a.get("skills"),
                builtin_skills=a.get("builtin_skills"),
                model=a.get("model"),
                provider=a.get("provider"),
            )
            for a in raw_agents
        ]

        project_id = await self._pm.create_project(
            name=args["name"],
            description=args["description"],
            agents=specs,
            session_id=args["session_id"],
            initial_messages=args.get("initial_messages", []),
        )
        return ToolResult.ok(
            f"Project created: {project_id}\n"
            f"Spawned {len(specs)} worker agent(s). "
            f"The manager agent will deliver results to your session."
        )

    def _list_projects(self, args: dict) -> ToolResult:
        status_filter = args.get("status")
        projects = self._pm.list_projects(status=status_filter)
        if not projects:
            return ToolResult.ok("No projects found.")
        lines = ["Projects:"]
        for p in projects:
            lines.append(
                f"  [{p['status']}] {p['project_id']} — {p['name']} "
                f"({p['agent_count']} agents)"
            )
        return ToolResult.ok("\n".join(lines))

    async def _cancel_project(self, args: dict) -> ToolResult:
        project_id = args["project_id"]
        cancelled = await self._pm.cancel_project(project_id)
        if cancelled:
            return ToolResult.ok(f"Project {project_id} cancelled.")
        return ToolResult.fail(f"Project {project_id} not found.")

    def _get_project_status(self, args: dict) -> ToolResult:
        project_id = args["project_id"]
        status = self._pm.get_project_status(project_id)
        if status is None:
            return ToolResult.fail(f"Project {project_id} not found.")
        return ToolResult.ok(json.dumps(status, indent=2))

    async def _delete_project(self, args: dict) -> ToolResult:
        project_id = args["project_id"]
        deleted = await self._pm.delete_project(project_id)
        if deleted:
            return ToolResult.ok(
                f"Project {project_id} deleted. All metadata removed from projects, agents, and kanban streams."
            )
        return ToolResult.fail(f"Project {project_id} not found.")

    async def _create_scheduled_project(self, args: dict) -> ToolResult:
        from pulsebot.agents.models import SubAgentSpec

        raw_agents = args.get("agents", [])
        specs = [
            SubAgentSpec(
                name=a["name"],
                task_description=a["task_description"],
                project_id="",  # set by ProjectManager
                target_agents=a.get("target_agents", []),
                skills=a.get("skills"),
                builtin_skills=a.get("builtin_skills"),
                model=a.get("model"),
                provider=a.get("provider"),
            )
            for a in raw_agents
        ]

        project_id = await self._pm.create_scheduled_project(
            name=args["name"],
            description=args["description"],
            agents=specs,
            session_id=args["session_id"],
            schedule_type=args["schedule_type"],
            schedule_expr=args["schedule_expr"],
            trigger_prompt=args["trigger_prompt"],
            initial_messages=args.get("initial_messages", []),
        )
        return ToolResult.ok(
            f"Scheduled project created: {project_id}\n"
            f"Spawned {len(specs)} worker agent(s) with schedule: "
            f"{args['schedule_type']} ({args['schedule_expr']}). "
            f"Agents will idle and execute on each trigger."
        )

    async def _create_event_driven_project(self, args: dict) -> ToolResult:
        name = args["name"]
        description = args["description"]
        agents = args["agents"]
        session_id = args["session_id"]
        event_query = args["event_query"]
        context_field = args["context_field"]
        trigger_prompt = args["trigger_prompt"]
        initial_messages = args.get("initial_messages", [])

        project_id = await self._project_manager.create_event_driven_project(
            name=name,
            description=description,
            agents=agents,
            session_id=session_id,
            event_query=event_query,
            context_field=context_field,
            trigger_prompt=trigger_prompt,
            initial_messages=initial_messages,
        )
        return ToolResult.ok(
            f"Event-driven project '{name}' created (ID: {project_id}). "
            f"Listening on query: {event_query!r}. "
            f"Each row's '{context_field}' value will trigger a run."
        )
