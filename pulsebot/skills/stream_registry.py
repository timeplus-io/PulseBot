"""Stream-native skill registry backed by the pulsebot.skills Proton stream.

Replaces the file-based .clawhub/lock.json with an event-sourced stream:
- install → appends action='install' record
- remove  → appends action='remove' tombstone
- read    → queries latest action per slug, excludes removed
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
    "SELECT name, version, content_hash, source, installed_at FROM ("
    "  SELECT slug AS name,"
    "         arg_max(version,      created_at) AS version,"
    "         arg_max(content_hash, created_at) AS content_hash,"
    "         arg_max(source,       created_at) AS source,"
    "         arg_max(installed_at, created_at) AS installed_at,"
    "         arg_max(action,       created_at) AS action"
    "  FROM table(pulsebot.skills)"
    "  GROUP BY slug"
    ") WHERE action != 'remove'"
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
        """Record a skill installation."""
        self._client.insert(STREAM, [{
            "slug": skill.slug,
            "version": skill.version,
            "content_hash": skill.content_hash,
            "source": skill.source,
            "action": "install",
            "installed_at": skill.installed_at,
        }])

    def remove(self, slug: str) -> None:
        """Record a skill removal (tombstone)."""
        self._client.insert(STREAM, [{
            "slug": slug,
            "version": "",
            "content_hash": "",
            "source": "",
            "action": "remove",
            "installed_at": "",
        }])
