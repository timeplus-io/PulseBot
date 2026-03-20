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


class SkillRequirements(BaseModel):
    """Runtime requirements declared in metadata.openclaw.requires."""
    env: list[str] = Field(default_factory=list)
    bins: list[str] = Field(default_factory=list)
    any_bins: list[str] = Field(default_factory=list)
    configs: list[str] = Field(default_factory=list)


class OpenClawMetadata(BaseModel):
    """OpenClaw-specific extensions found in metadata.openclaw (or aliases)."""
    requires: SkillRequirements = Field(default_factory=SkillRequirements)
    primary_env: str | None = None
    always: bool = False
    emoji: str | None = None
    homepage: str | None = None
    os: list[str] = Field(default_factory=list)
    skill_key: str | None = None


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
    metadata: dict[str, Any] = Field(default_factory=dict)
    allowed_tools: str | None = None
    version: str | None = None

    # OpenClaw extensions (None for plain agentskills.io skills)
    openclaw: OpenClawMetadata | None = None


class SkillContent(BaseModel):
    """Full skill content loaded on demand (Tier 2)."""
    metadata: SkillMetadata
    instructions: str
    scripts: dict[str, str] = Field(default_factory=dict)
    references: dict[str, str] = Field(default_factory=dict)
