"""SkillManagerSkill — lets the agent search, install, list, and remove ClawHub skills."""

from __future__ import annotations

import asyncio
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.config import SkillsConfig
    from pulsebot.skills.loader import SkillLoader
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


class SkillManagerSkill(BaseSkill):
    """LLM-callable tools for managing ClawHub skills.

    Exposes search, install, list, and remove operations that mirror
    the ``pulsebot skill`` CLI commands, allowing the agent to extend
    its own capabilities at runtime.

    Skill metadata is persisted in the ``pulsebot.skills`` Proton stream
    using an event-sourcing pattern (install/remove tombstones).

    After install the skill is hot-reloaded immediately. Removing a skill
    takes effect after the agent is restarted.
    """

    name = "skill_manager"
    description = "Search, install, list, and remove ClawHub skills"

    def __init__(
        self,
        skills_config: "SkillsConfig",
        client: "TimeplusClient",
        loader: "SkillLoader | None" = None,
    ) -> None:
        from pulsebot.skills.stream_registry import SkillStreamRegistry

        cfg = skills_config.clawhub
        self._site_url = cfg.site_url
        self._registry_url = cfg.registry_url
        self._auth_token_path = cfg.auth_token_path
        self._registry = SkillStreamRegistry(client)

        self._loader = loader

        # Resolve install directory: explicit config > first skill_dir > ./skills
        if cfg.install_dir:
            self._install_dir = Path(cfg.install_dir)
        elif skills_config.skill_dirs:
            self._install_dir = Path(skills_config.skill_dirs[0])
        else:
            self._install_dir = Path("./skills")

    def _make_client(self):
        from pulsebot.skills.clawhub_client import ClawHubClient

        auth_token = None
        if self._auth_token_path:
            token_path = Path(self._auth_token_path).expanduser()
            if token_path.exists():
                auth_token = token_path.read_text(encoding="utf-8").strip()

        return ClawHubClient(
            site_url=self._site_url,
            registry_url=self._registry_url,
            auth_token=auth_token,
        )

    def get_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="skill_search",
                description=(
                    "Search ClawHub for available skills matching a query. "
                    "Use this to discover skills before installing."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search terms, e.g. 'weather' or 'github'"},
                        "limit": {"type": "integer", "description": "Maximum number of results (default 10)"},
                    },
                    "required": ["query"],
                },
            ),
            ToolDefinition(
                name="skill_list",
                description="List all ClawHub skills currently installed.",
                parameters={"type": "object", "properties": {}},
            ),
            ToolDefinition(
                name="skill_install",
                description=(
                    "Install a skill from ClawHub by slug. "
                    "The skill is hot-reloaded immediately after installing — no restart needed."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "slug": {"type": "string", "description": "ClawHub skill slug, e.g. 'weather'"},
                        "version": {"type": "string", "description": "Version to install (default: latest)"},
                    },
                    "required": ["slug"],
                },
            ),
            ToolDefinition(
                name="skill_remove",
                description=(
                    "Remove an installed ClawHub skill by slug. "
                    "The skill files are deleted immediately; the change takes full effect after restart."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "slug": {"type": "string", "description": "ClawHub skill slug to remove"},
                    },
                    "required": ["slug"],
                },
            ),
        ]

    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        if tool_name == "skill_search":
            return await self._search(arguments)
        if tool_name == "skill_list":
            return await self._list()
        if tool_name == "skill_install":
            return await self._install(arguments)
        if tool_name == "skill_remove":
            return await self._remove(arguments)
        return ToolResult.fail(f"Unknown tool: {tool_name}")

    async def _search(self, args: dict) -> ToolResult:
        query = args.get("query", "").strip()
        limit = int(args.get("limit", 10))
        if not query:
            return ToolResult.fail("query is required")
        try:
            with self._make_client() as client:
                results = await asyncio.to_thread(client.search, query, limit)
            if not results:
                return ToolResult.ok(f"No skills found for '{query}'.")
            lines = [f"ClawHub skills matching '{query}':"]
            for s in results:
                lines.append(f"  - {s.slug} v{s.latest_version} — {s.summary} (by {s.owner_handle})")
            return ToolResult.ok("\n".join(lines))
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _list(self) -> ToolResult:
        try:
            skills = await asyncio.to_thread(self._registry.read)
            if not skills:
                return ToolResult.ok("No ClawHub skills installed.")
            lines = ["Installed ClawHub skills:"]
            for entry in skills.values():
                lines.append(
                    f"  - {entry.slug} v{entry.version}"
                    f" (installed {entry.installed_at[:10]})"
                )
            return ToolResult.ok("\n".join(lines))
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _install(self, args: dict) -> ToolResult:
        slug = args.get("slug", "").strip()
        version = args.get("version", "latest") or "latest"
        if not slug:
            return ToolResult.fail("slug is required")
        try:
            from pulsebot.skills.clawhub_client import IntegrityError, SecurityError
            from pulsebot.skills.lock import LockedSkill

            self._install_dir.mkdir(parents=True, exist_ok=True)

            def _do_install():
                with self._make_client() as client:
                    return client.download_and_install(slug, self._install_dir, version)

            target = await asyncio.to_thread(_do_install)

            content_hash = await asyncio.to_thread(
                lambda: __import__("pulsebot.skills.lock", fromlist=["LockFile"]).LockFile.compute_content_hash(target)
            )
            skill = LockedSkill(
                slug=slug,
                version=version,
                content_hash=content_hash,
                installed_at=datetime.now(timezone.utc).isoformat(),
                source="clawhub",
            )
            await asyncio.to_thread(self._registry.add, skill)

            logger.info("Installed skill", extra={"slug": slug, "version": version})
            if self._loader is not None:
                self._loader.reload_external_skills()
            return ToolResult.ok(
                f"Installed '{slug}' v{version} to {target}. "
                "The skill has been hot-reloaded and is now available."
            )
        except SecurityError as e:
            return ToolResult.fail(f"Security error: {e}")
        except IntegrityError as e:
            return ToolResult.fail(f"Integrity error: {e}")
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _remove(self, args: dict) -> ToolResult:
        slug = args.get("slug", "").strip()
        if not slug:
            return ToolResult.fail("slug is required")
        try:
            target = self._install_dir / slug
            if target.exists():
                await asyncio.to_thread(shutil.rmtree, target)
                removed_dir = True
            else:
                removed_dir = False

            await asyncio.to_thread(self._registry.remove, slug)
            logger.info("Removed skill", extra={"slug": slug})

            msg = f"Removed '{slug}'."
            if not removed_dir:
                msg += " (directory not found, record removed from stream)"
            msg += " The skill files have been deleted and will be fully unloaded on next restart."
            return ToolResult.ok(msg)
        except Exception as e:
            return ToolResult.fail(str(e))
