"""Dynamic skill loader for PulseBot."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

from pulsebot.skills.agentskills.loader import discover_skills
from pulsebot.skills.agentskills.models import SkillMetadata
from pulsebot.skills.base import BaseSkill, ToolDefinition
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.config import SkillsConfig
    from pulsebot.timeplus.event_writer import EventWriter

logger = get_logger(__name__)

# Registry of built-in skills
BUILTIN_SKILLS = {
    "web_search": "pulsebot.skills.builtin.web_search.WebSearchSkill",
    "file_ops": "pulsebot.skills.builtin.file_ops.FileOpsSkill",
    "shell": "pulsebot.skills.builtin.shell.ShellSkill",
    "workspace":  "pulsebot.skills.builtin.workspace.WorkspaceSkill",
    "scheduler": "pulsebot.skills.builtin.scheduler.SchedulerSkill",
    "project_manager": "pulsebot.skills.builtin.project_manager.ProjectManagerSkill",
}


class SkillLoader:
    """Load and manage skills dynamically.
    
    Handles:
    - Loading built-in skills by name
    - Loading custom skills from module paths
    - Providing tool definitions to the agent
    - Routing tool calls to the correct skill
    
    Example:
        >>> loader = SkillLoader()
        >>> loader.load_builtin("web_search", api_key="...")
        >>> tools = loader.get_tools()
        >>> skill = loader.get_skill_for_tool("web_search")
    """

    def __init__(self):
        """Initialize skill loader."""
        self._skills: dict[str, BaseSkill] = {}
        self._tool_to_skill: dict[str, str] = {}
        self._external_skills: dict[str, SkillMetadata] = {}
        # Stored for hot-reload
        self._skill_dirs: list[str] = []
        self._disabled_skills: list[str] = []
        self._builtin_names: set[str] = set()
        self._events: "EventWriter | None" = None

    @classmethod
    def from_config(cls, config: SkillsConfig, **skill_configs: dict[str, Any]) -> SkillLoader:
        """Create loader and load skills from configuration.

        Args:
            config: Skills configuration
            **skill_configs: Per-skill configuration (e.g., web_search={"api_key": "..."})

        Returns:
            Configured skill loader
        """
        loader = cls()

        # Load built-in skills
        for skill_name in config.builtin:
            skill_config = skill_configs.get(skill_name, {})
            try:
                loader.load_builtin(skill_name, **skill_config)
            except Exception as e:
                logger.warning(f"Failed to load builtin skill {skill_name}: {e}")

        # Load custom skills
        for module_path in config.custom:
            try:
                loader.load_custom(module_path)
            except Exception as e:
                logger.warning(f"Failed to load custom skill {module_path}: {e}")

        # Discover external agentskills.io skills
        if config.skill_dirs:
            loader._skill_dirs = list(config.skill_dirs)
            loader._disabled_skills = list(config.disabled_skills or [])
            loader._discover_external_skills(
                skill_dirs=config.skill_dirs,
                disabled=config.disabled_skills,
            )

        return loader

    def _discover_external_skills(
        self, skill_dirs: list[str], disabled: list[str] | None = None
    ) -> None:
        """Discover agentskills.io packages and register the bridge skill.

        Args:
            skill_dirs: Directories to scan for SKILL.md files
            disabled: Skill names to skip
        """
        from pulsebot.skills.agentskills.requirements import RequirementChecker

        disabled_set = set(disabled or [])
        discovered = discover_skills(skill_dirs)
        checker = RequirementChecker()

        new_skills: list[str] = []
        for meta in discovered:
            if meta.name in disabled_set:
                continue
            if meta.name in self._external_skills:
                continue  # Already loaded
            satisfied, reason = checker.check(meta)
            if not satisfied:
                logger.info(
                    "Skill '%s' skipped: %s", meta.name, reason,
                    extra={"skill": meta.name, "reason": reason},
                )
                continue
            self._external_skills[meta.name] = meta
            new_skills.append(meta.name)

        if self._external_skills:
            from pulsebot.skills.builtin.agentskills_bridge import AgentSkillsBridge
            bridge = AgentSkillsBridge(skill_registry=self._external_skills)
            self._skills["agentskills_bridge"] = bridge
            for tool in bridge.get_tools():
                self._tool_to_skill[tool.name] = "agentskills_bridge"

        if new_skills:
            logger.info(
                f"Loaded {len(new_skills)} new external skill(s): {new_skills}"
            )

    def reload_external_skills(self) -> bool:
        """Re-scan skill directories and register any newly installed skills.

        Only picks up skills added since last load — never removes existing ones.

        Returns:
            True if at least one new skill was registered.
        """
        if not self._skill_dirs:
            return False
        before = set(self._external_skills.keys())
        self._discover_external_skills(self._skill_dirs, self._disabled_skills)
        changed = set(self._external_skills.keys()) != before
        # asyncio.create_task() is safe here: reload_external_skills() is only
        # called from _watch_skills(), which runs as an async task inside the loop.
        if self._events and changed:
            import asyncio
            asyncio.create_task(self._events.emit("skill.hot_reloaded", payload={
                "external_skill_count": len(self._external_skills),
            }))
        return changed

    async def set_events(self, events: "EventWriter") -> None:
        """Inject the EventWriter and retroactively emit skill.loaded for all loaded skills.

        Called from Agent.run() (inside async context) after the event loop is running.
        """
        self._events = events
        # Emit skill.loaded for skills that were already loaded synchronously
        for skill_name, skill_instance in self._skills.items():
            tools = skill_instance.get_tools()
            await events.emit("skill.loaded", payload={
                "skill_name": skill_name,
                "tool_count": len(tools),
                "tool_names": [t.name for t in tools],
                "source": "builtin" if skill_name in self._builtin_names else "external",
            })

    def load_builtin(self, name: str, **config: Any) -> None:
        """Load a built-in skill by name.
        
        Args:
            name: Built-in skill name (e.g., 'web_search')
            **config: Skill-specific configuration
        """
        if name not in BUILTIN_SKILLS:
            raise ValueError(f"Unknown built-in skill: {name}. Available: {list(BUILTIN_SKILLS.keys())}")

        module_path = BUILTIN_SKILLS[name]
        self._load_skill(name, module_path, config)
        self._builtin_names.add(name)

    def load_custom(self, module_path: str, **config: Any) -> None:
        """Load a custom skill from a module path.
        
        Args:
            module_path: Full module path to the skill class
            **config: Skill-specific configuration
        """
        # Derive name from class name
        name = module_path.split(".")[-1].lower()
        self._load_skill(name, module_path, config)

    def _load_skill(self, name: str, module_path: str, config: dict[str, Any]) -> None:
        """Internal skill loading.
        
        Args:
            name: Skill name
            module_path: Full module.ClassName path
            config: Skill configuration
        """
        try:
            # Split module and class
            parts = module_path.rsplit(".", 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid module path: {module_path}")

            module_name, class_name = parts

            # Import module
            module = importlib.import_module(module_name)

            # Get class
            skill_class = getattr(module, class_name)

            # Instantiate
            if config:
                skill = skill_class(**config)
            else:
                skill = skill_class()

            # Register skill and its tools
            self._skills[name] = skill

            for tool in skill.get_tools():
                self._tool_to_skill[tool.name] = name

            logger.info(
                f"Loaded skill: {name}",
                extra={"tools": [t.name for t in skill.get_tools()]}
            )

        except Exception as e:
            logger.error(f"Failed to load skill {name}: {e}")
            raise

    def get_skill(self, name: str) -> BaseSkill | None:
        """Get a loaded skill by name.
        
        Args:
            name: Skill name
            
        Returns:
            Skill instance or None
        """
        return self._skills.get(name)

    def get_skill_for_tool(self, tool_name: str) -> BaseSkill | None:
        """Get the skill that provides a specific tool.
        
        Args:
            tool_name: Tool name
            
        Returns:
            Skill instance or None
        """
        skill_name = self._tool_to_skill.get(tool_name)
        if skill_name:
            return self._skills.get(skill_name)
        return None

    def get_tools(self) -> list[ToolDefinition]:
        """Get all tool definitions from loaded skills.
        
        Returns:
            List of all tool definitions
        """
        tools = []
        for skill in self._skills.values():
            tools.extend(skill.get_tools())
        return tools

    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """Get all tool definitions in OpenAI format.

        Returns:
            List of tool definitions in OpenAI format
        """
        return [tool.to_openai_format() for tool in self.get_tools()]

    def get_loaded_skills(self) -> list[BaseSkill]:
        """Return all currently loaded skill instances.

        Returns:
            List of loaded BaseSkill instances.
        """
        return list(self._skills.values())

    def create_subset(self, names: list[str]) -> SkillLoader:
        """Create a new SkillLoader containing only the named skills.

        Skills not present in this loader are silently skipped.
        Useful for sub-agent skill isolation.

        Args:
            names: Skill names to include.

        Returns:
            New SkillLoader with only the named skills.
        """
        subset = SkillLoader()
        for name in names:
            skill = self._skills.get(name)
            if skill is None:
                logger.warning(f"Skill '{name}' not found in loader, skipping")
                continue
            subset._skills[name] = skill
            for tool in skill.get_tools():
                subset._tool_to_skill[tool.name] = name
        return subset

    @property
    def loaded_skills(self) -> list[str]:
        """List of loaded skill names."""
        return list(self._skills.keys())

    @property
    def available_tools(self) -> list[str]:
        """List of available tool names."""
        return list(self._tool_to_skill.keys())

    @property
    def external_skills(self) -> dict[str, SkillMetadata]:
        """Registry of discovered external agentskills.io skills."""
        return self._external_skills

    def format_skills_for_prompt(self) -> str:
        """Generate compact skill index for the system prompt.

        Only external agentskills.io skills are listed here. Built-in skills
        are already registered as regular tools.

        Returns:
            Formatted string for system prompt injection, or empty string.
        """
        if not self._external_skills:
            return ""

        lines = [
            "## Available Skills",
            "You have access to the following agentskills.io skills. "
            "To use a skill, call the `load_skill` tool with the skill name "
            "to get its full instructions. If a skill includes scripts, "
            "use `read_skill_file` to read the script, then `run_command` to execute it.\n",
        ]
        for meta in self._external_skills.values():
            lines.append(f"- **{meta.name}**: {meta.description}")

        return "\n".join(lines)
