"""Bridge skill that exposes agentskills.io packages as LLM-callable tools.

Provides two tools:
- load_skill: Load full instructions for a skill by name (Tier 2)
- read_skill_file: Read a specific file from a skill package
"""

from __future__ import annotations

import logging
from typing import Any

from pulsebot.skills.agentskills.loader import load_skill_content
from pulsebot.skills.agentskills.models import SkillContent, SkillMetadata
from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult

logger = logging.getLogger(__name__)


class AgentSkillsBridge(BaseSkill):
    """Provides load_skill and read_skill_file tools for external skills."""

    name = "agentskills_bridge"
    description = "Load and read agentskills.io skill packages"

    def __init__(self, skill_registry: dict[str, SkillMetadata] | None = None):
        self._registry: dict[str, SkillMetadata] = skill_registry or {}
        self._content_cache: dict[str, SkillContent] = {}

    def set_registry(self, registry: dict[str, SkillMetadata]) -> None:
        """Update the skill registry (called after discovery)."""
        self._registry = registry

    def get_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="load_skill",
                description=(
                    "Load the full instructions for an agentskills.io skill by name. "
                    "Call this when you need detailed instructions to perform a task "
                    "matching an available skill from the skill index."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "skill_name": {
                            "type": "string",
                            "description": "Name of the skill to load",
                        }
                    },
                    "required": ["skill_name"],
                },
            ),
            ToolDefinition(
                name="read_skill_file",
                description=(
                    "Read a specific file from a skill package. "
                    "Use for scripts or references listed in skill instructions."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "skill_name": {
                            "type": "string",
                            "description": "Name of the skill",
                        },
                        "file_path": {
                            "type": "string",
                            "description": (
                                "Path of the file to read, including the directory prefix "
                                "as listed in the skill instructions."
                            ),
                        },
                    },
                    "required": ["skill_name", "file_path"],
                },
            ),
        ]

    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        if tool_name == "load_skill":
            return await self._load_skill(arguments.get("skill_name", ""))
        elif tool_name == "read_skill_file":
            return await self._read_skill_file(
                arguments.get("skill_name", ""),
                arguments.get("file_path", ""),
            )
        return ToolResult.fail(f"Unknown tool: {tool_name}")

    async def _load_skill(self, skill_name: str) -> ToolResult:
        meta = self._registry.get(skill_name)
        if not meta:
            available = ", ".join(sorted(self._registry.keys()))
            return ToolResult.fail(
                f"Skill '{skill_name}' not found. Available skills: {available}"
            )

        try:
            content = self._get_content(meta)
            result = self._format_instructions(content)
            return ToolResult.ok(result)
        except Exception as e:
            logger.error("Failed to load skill '%s': %s", skill_name, e)
            return ToolResult.fail(f"Failed to load skill '{skill_name}': {e}")

    async def _read_skill_file(self, skill_name: str, file_path: str) -> ToolResult:
        meta = self._registry.get(skill_name)
        if not meta:
            return ToolResult.fail(f"Skill '{skill_name}' not found.")

        try:
            content = self._get_content(meta)

            # file_path includes the directory prefix, e.g. "references/RANDOM_STREAMS.md"
            if file_path.startswith("scripts/"):
                name = file_path[len("scripts/"):]
                if name in content.scripts:
                    return ToolResult.ok(content.scripts[name])
            elif file_path.startswith("references/"):
                name = file_path[len("references/"):]
                if name in content.references:
                    return ToolResult.ok(content.references[name])
            else:
                # bare filename — check both buckets as fallback
                if file_path in content.scripts:
                    return ToolResult.ok(content.scripts[file_path])
                if file_path in content.references:
                    return ToolResult.ok(content.references[file_path])

            available = (
                [f"scripts/{f}" for f in content.scripts]
                + [f"references/{f}" for f in content.references]
            )
            return ToolResult.fail(
                f"File '{file_path}' not found in skill '{skill_name}'. "
                f"Available files: {available}"
            )
        except Exception as e:
            logger.error("Failed to read file from skill '%s': %s", skill_name, e)
            return ToolResult.fail(f"Failed to read file: {e}")

    def _get_content(self, meta: SkillMetadata) -> SkillContent:
        """Load and cache skill content."""
        if meta.name not in self._content_cache:
            self._content_cache[meta.name] = load_skill_content(meta)
        return self._content_cache[meta.name]

    def _format_instructions(self, content: SkillContent) -> str:
        """Format skill content for LLM consumption."""
        parts = [f"# Skill: {content.metadata.name}\n"]
        parts.append(content.instructions)

        if content.references:
            parts.append("\n\n## Available References")
            for fname in content.references:
                parts.append(f"- references/{fname}")

        if content.scripts:
            parts.append("\n\n## Available Scripts")
            for fname in content.scripts:
                parts.append(f"- scripts/{fname}")
            parts.append(
                "\nUse the read_skill_file tool to read any script or reference file, "
                "passing the full path as shown above. "
                "To execute a script, first read it with read_skill_file, "
                "then run it using the run_command tool."
            )

        return "\n".join(parts)
