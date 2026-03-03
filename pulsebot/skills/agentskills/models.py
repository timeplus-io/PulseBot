"""Data models for agentskills.io skill packages."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class SkillSource(str, Enum):
    """Origin of a skill."""
    INTERNAL = "internal"
    EXTERNAL = "external"


@dataclass
class SkillRequirements:
    """Runtime requirements declared in metadata.openclaw.requires."""
    env: list[str] = field(default_factory=list)
    bins: list[str] = field(default_factory=list)
    any_bins: list[str] = field(default_factory=list)
    configs: list[str] = field(default_factory=list)


@dataclass
class OpenClawMetadata:
    """OpenClaw-specific extensions found in metadata.openclaw (or aliases)."""
    requires: SkillRequirements = field(default_factory=SkillRequirements)
    primary_env: str | None = None
    always: bool = False
    emoji: str | None = None
    homepage: str | None = None
    os: list[str] = field(default_factory=list)
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

    model_config = {"arbitrary_types_allowed": True}


class SkillContent(BaseModel):
    """Full skill content loaded on demand (Tier 2)."""
    metadata: SkillMetadata
    instructions: str
    scripts: dict[str, str] = Field(default_factory=dict)
    references: dict[str, str] = Field(default_factory=dict)
