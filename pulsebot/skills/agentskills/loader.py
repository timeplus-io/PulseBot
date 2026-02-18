"""SKILL.md parser and directory scanner for agentskills.io packages."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import yaml

from pulsebot.skills.agentskills.models import SkillContent, SkillMetadata, SkillSource

logger = logging.getLogger(__name__)

# Regex for YAML frontmatter extraction
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)", re.DOTALL)

# agentskills.io name validation: lowercase, digits, hyphens
NAME_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")

# Valid frontmatter fields per agentskills.io spec
VALID_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def parse_frontmatter(skill_md_path: Path) -> tuple[dict, str]:
    """Parse SKILL.md into (frontmatter_dict, body_markdown)."""
    content = skill_md_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError(f"No valid YAML frontmatter in {skill_md_path}")
    frontmatter = yaml.safe_load(match.group(1))
    body = match.group(2).strip()
    return frontmatter, body


def validate_metadata(fm: dict, dir_name: str) -> list[str]:
    """Validate frontmatter against agentskills.io spec. Returns list of errors."""
    errors = []

    for key in fm:
        if key not in VALID_FIELDS:
            errors.append(f"Unknown frontmatter field: {key}")

    name = fm.get("name")
    if not name:
        errors.append("Missing required field: name")
    elif not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"Invalid name: {name}")
    elif name != dir_name:
        errors.append(f"name '{name}' doesn't match directory '{dir_name}'")

    desc = fm.get("description")
    if not desc:
        errors.append("Missing required field: description")
    elif len(desc) > 1024:
        errors.append("description exceeds 1024 characters")

    return errors


def load_skill_metadata(skill_dir: Path) -> SkillMetadata | None:
    """Load only metadata from a skill package (Tier 1 - cheap)."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None

    try:
        fm, _ = parse_frontmatter(skill_md)
        errors = validate_metadata(fm, skill_dir.name)
        if errors:
            logger.warning("Skill '%s' has validation errors: %s", skill_dir.name, errors)
            return None

        return SkillMetadata(
            name=fm["name"],
            description=fm["description"],
            source=SkillSource.EXTERNAL,
            path=skill_dir,
            license=fm.get("license"),
            compatibility=fm.get("compatibility"),
            metadata=fm.get("metadata", {}),
            allowed_tools=fm.get("allowed-tools"),
        )
    except Exception as e:
        logger.warning("Failed to load skill metadata from %s: %s", skill_dir, e)
        return None


def load_skill_content(meta: SkillMetadata) -> SkillContent:
    """Load full skill content on demand (Tier 2 - expensive)."""
    if meta.path is None:
        raise ValueError("Cannot load content for skill without path")

    skill_md = meta.path / "SKILL.md"
    _, body = parse_frontmatter(skill_md)

    scripts: dict[str, str] = {}
    scripts_dir = meta.path / "scripts"
    if scripts_dir.exists():
        for f in scripts_dir.iterdir():
            if f.is_file():
                scripts[f.name] = f.read_text(encoding="utf-8")

    references: dict[str, str] = {}
    refs_dir = meta.path / "references"
    if refs_dir.exists():
        for f in refs_dir.iterdir():
            if f.is_file():
                references[f.name] = f.read_text(encoding="utf-8")

    return SkillContent(
        metadata=meta,
        instructions=body,
        scripts=scripts,
        references=references,
    )


def discover_skills(skill_dirs: list[str]) -> list[SkillMetadata]:
    """Scan configured directories for agentskills.io packages.

    Directories are scanned in order; first occurrence of a skill name wins.
    """
    skills: list[SkillMetadata] = []
    seen_names: set[str] = set()

    for dir_path in skill_dirs:
        base = Path(dir_path)
        if not base.exists():
            logger.debug("Skill directory does not exist: %s", base)
            continue
        for child in sorted(base.iterdir()):
            if child.is_dir() and (child / "SKILL.md").exists():
                meta = load_skill_metadata(child)
                if meta and meta.name not in seen_names:
                    skills.append(meta)
                    seen_names.add(meta.name)

    return skills
