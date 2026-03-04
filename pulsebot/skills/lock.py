"""Lock file manager for ClawHub-installed skills."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class LockedSkill:
    """Record of a ClawHub-installed skill stored in lock.json."""
    slug: str
    version: str
    content_hash: str
    installed_at: str      # ISO 8601 timestamp
    source: str = "clawhub"


class LockFile:
    """Manages .clawhub/lock.json for tracking installed skills.

    The file format is compatible with the ClawHub CLI's lock.json so
    users can mix tools.
    """

    def __init__(self, workdir: Path):
        self.lock_path = workdir / ".clawhub" / "lock.json"

    def read(self) -> dict[str, LockedSkill]:
        """Read all locked skills from disk."""
        if not self.lock_path.exists():
            return {}
        data = json.loads(self.lock_path.read_text(encoding="utf-8"))
        return {
            slug: LockedSkill(**entry)
            for slug, entry in data.get("skills", {}).items()
        }

    def write(self, skills: dict[str, LockedSkill]) -> None:
        """Write all locked skills to disk atomically."""
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": 1,
            "skills": {slug: asdict(entry) for slug, entry in skills.items()},
        }
        self.lock_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add(self, skill: LockedSkill) -> None:
        """Add or update a skill entry in the lock file."""
        skills = self.read()
        skills[skill.slug] = skill
        self.write(skills)

    def remove(self, slug: str) -> None:
        """Remove a skill from the lock file."""
        skills = self.read()
        skills.pop(slug, None)
        self.write(skills)

    @staticmethod
    def compute_content_hash(skill_dir: Path) -> str:
        """Compute SHA256 hash of all files in a skill directory."""
        hasher = hashlib.sha256()
        for file_path in sorted(skill_dir.rglob("*")):
            if file_path.is_file():
                hasher.update(str(file_path.relative_to(skill_dir)).encode())
                hasher.update(file_path.read_bytes())
        return hasher.hexdigest()
