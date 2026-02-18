"""AgentSkills.io integration for PulseBot.

Implements the agentskills.io standard with metadata-first loading pattern.
Skills are discovered from configured directories by scanning for SKILL.md files.
"""

from pulsebot.skills.agentskills.models import SkillMetadata, SkillContent
from pulsebot.skills.agentskills.loader import (
    discover_skills,
    load_skill_metadata,
    load_skill_content,
    parse_frontmatter,
)

__all__ = [
    "SkillMetadata",
    "SkillContent",
    "discover_skills",
    "load_skill_metadata",
    "load_skill_content",
    "parse_frontmatter",
]
