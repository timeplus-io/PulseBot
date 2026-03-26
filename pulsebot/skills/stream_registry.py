"""Stream-native skill registry backed by the pulsebot.skills Proton stream.

Uses an append-only stream for installs (upgrades re-insert) and physical
DELETE for removals, consistent with all other PulseBot metadata streams.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pulsebot.skills.lock import LockedSkill
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)

STREAM = "pulsebot.skills"

_LIST_QUERY = (
    "SELECT slug AS name, version, content_hash, source, installed_at"
    " FROM table(pulsebot.skills)"
    " ORDER BY created_at DESC"
    " LIMIT 1 BY slug"
)


class SkillStreamRegistry:
    """Read and write skill metadata to the pulsebot.skills Proton stream.

    Uses an event-sourcing pattern: each install/remove appends a record.
    The current state is derived by taking the latest action per slug.
    """

    def __init__(self, client: "TimeplusClient") -> None:
        self._client = client

    def read(self) -> dict[str, LockedSkill]:
        """Return all currently installed skills keyed by slug."""
        try:
            rows = self._client.query(_LIST_QUERY)
            return {
                row["name"]: LockedSkill(
                    slug=row["name"],
                    version=row["version"],
                    content_hash=row["content_hash"],
                    source=row["source"],
                    installed_at=row["installed_at"],
                )
                for row in rows
            }
        except Exception as e:
            logger.warning("Could not read skills stream: %s", e)
            return {}

    def add(self, skill: LockedSkill) -> None:
        """Record a skill installation (or upgrade via re-insert)."""
        self._client.insert(STREAM, [{
            "slug": skill.slug,
            "version": skill.version,
            "content_hash": skill.content_hash,
            "source": skill.source,
            "action": "install",
            "installed_at": skill.installed_at,
        }])

    def remove(self, slug: str) -> None:
        """Physically delete a skill from the registry."""
        self._client.execute(f"DELETE FROM {STREAM} WHERE slug = '{slug}'")
