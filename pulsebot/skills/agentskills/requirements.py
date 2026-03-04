"""Runtime requirement checker for OpenClaw skill metadata."""

from __future__ import annotations

import os
import platform
import shutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulsebot.skills.agentskills.models import SkillMetadata

PLATFORM_MAP = {
    "Darwin": "darwin",
    "Linux": "linux",
    "Windows": "win32",
}


class RequirementChecker:
    """Validates that a skill's runtime requirements are satisfied.

    Checks declared bins, environment variables, and OS restrictions from
    the OpenClaw metadata block. Results for binary lookups are cached.
    Plain agentskills.io skills (no openclaw metadata) always pass.
    """

    def __init__(self):
        self._bin_cache: dict[str, bool] = {}
        self._current_os = PLATFORM_MAP.get(platform.system(), "")

    def check(self, skill: "SkillMetadata") -> tuple[bool, str | None]:
        """Check if a skill's requirements are satisfied.

        Args:
            skill: SkillMetadata to check.

        Returns:
            (True, None) if requirements satisfied, (False, reason) otherwise.
        """
        meta = skill.openclaw
        if meta is None:
            return True, None  # No OpenClaw requirements declared

        if meta.always:
            return True, None  # always=true skills bypass requirement checks

        # OS check
        if meta.os and self._current_os not in meta.os:
            return False, f"Requires OS {meta.os}, current is {self._current_os}"

        # Required binaries (ALL must exist)
        for binary in meta.requires.bins:
            if not self._check_bin(binary):
                return False, f"Required binary not found: {binary}"

        # Any-of binaries (at least ONE must exist)
        if meta.requires.any_bins:
            if not any(self._check_bin(b) for b in meta.requires.any_bins):
                return False, (
                    f"None of required binaries found: {meta.requires.any_bins}"
                )

        # Required environment variables
        for env_var in meta.requires.env:
            if not os.environ.get(env_var):
                return False, f"Required environment variable not set: {env_var}"

        return True, None

    def _check_bin(self, name: str) -> bool:
        if name not in self._bin_cache:
            self._bin_cache[name] = shutil.which(name) is not None
        return self._bin_cache[name]

    def invalidate_cache(self) -> None:
        """Clear binary lookup cache (call when PATH may have changed)."""
        self._bin_cache.clear()
