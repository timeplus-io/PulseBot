"""Data models for agentskills.io skill packages."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class SkillSource(str, Enum):
    """Origin of a skill."""
    INTERNAL = "internal"
    EXTERNAL = "external"


class SkillMetadata(BaseModel):
    """Lightweight metadata loaded at startup (Tier 1).

    Only name + description are injected into the system prompt,
    keeping cost to ~24 tokens per skill.
    """
    name: str
    description: str
    source: SkillSource = SkillSource.EXTERNAL
    path: Path | None = None
    license: str | None = None
    compatibility: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    allowed_tools: str | None = None


class SkillContent(BaseModel):
    """Full skill content loaded on demand (Tier 2)."""
    metadata: SkillMetadata
    instructions: str
    scripts: dict[str, str] = Field(default_factory=dict)
    references: dict[str, str] = Field(default_factory=dict)
