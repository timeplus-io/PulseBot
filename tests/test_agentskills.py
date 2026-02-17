"""Tests for agentskills.io integration."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from pulsebot.skills.agentskills.loader import (
    discover_skills,
    load_skill_content,
    load_skill_metadata,
    parse_frontmatter,
    validate_metadata,
)
from pulsebot.skills.agentskills.models import SkillMetadata, SkillSource
from pulsebot.skills.builtin.agentskills_bridge import AgentSkillsBridge


@pytest.fixture
def skill_dir(tmp_path: Path) -> Path:
    """Create a valid skill package in a temp directory."""
    skill = tmp_path / "my-skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\n"
        "name: my-skill\n"
        "description: A test skill for unit tests.\n"
        "license: MIT\n"
        "metadata:\n"
        "  author: test\n"
        "  version: '1.0'\n"
        "---\n\n"
        "# My Skill\n\n"
        "These are the full instructions for my-skill.\n\n"
        "## Usage\n"
        "Do the thing.\n"
    )
    scripts = skill / "scripts"
    scripts.mkdir()
    (scripts / "helper.py").write_text("print('hello')\n")

    refs = skill / "references"
    refs.mkdir()
    (refs / "guide.md").write_text("# Guide\nSome reference content.\n")

    return tmp_path


@pytest.fixture
def invalid_skill_dir(tmp_path: Path) -> Path:
    """Create skill packages with various validation issues."""
    # Missing name
    bad1 = tmp_path / "bad-skill-1"
    bad1.mkdir()
    (bad1 / "SKILL.md").write_text(
        "---\n"
        "description: Missing name field.\n"
        "---\n\n"
        "Body text.\n"
    )

    # Name doesn't match directory
    bad2 = tmp_path / "bad-skill-2"
    bad2.mkdir()
    (bad2 / "SKILL.md").write_text(
        "---\n"
        "name: wrong-name\n"
        "description: Name mismatch.\n"
        "---\n\n"
        "Body text.\n"
    )

    # No frontmatter
    bad3 = tmp_path / "bad-skill-3"
    bad3.mkdir()
    (bad3 / "SKILL.md").write_text("Just plain text, no frontmatter.\n")

    return tmp_path


class TestParseFrontmatter:
    def test_valid_frontmatter(self, skill_dir: Path):
        skill_md = skill_dir / "my-skill" / "SKILL.md"
        fm, body = parse_frontmatter(skill_md)
        assert fm["name"] == "my-skill"
        assert fm["description"] == "A test skill for unit tests."
        assert "full instructions" in body

    def test_no_frontmatter(self, invalid_skill_dir: Path):
        skill_md = invalid_skill_dir / "bad-skill-3" / "SKILL.md"
        with pytest.raises(ValueError, match="No valid YAML frontmatter"):
            parse_frontmatter(skill_md)


class TestValidateMetadata:
    def test_valid_metadata(self):
        fm = {"name": "my-skill", "description": "Does something."}
        errors = validate_metadata(fm, "my-skill")
        assert errors == []

    def test_missing_name(self):
        fm = {"description": "No name."}
        errors = validate_metadata(fm, "some-dir")
        assert any("Missing required field: name" in e for e in errors)

    def test_name_mismatch(self):
        fm = {"name": "wrong-name", "description": "Mismatch."}
        errors = validate_metadata(fm, "correct-name")
        assert any("doesn't match directory" in e for e in errors)

    def test_invalid_name_format(self):
        fm = {"name": "Invalid_Name", "description": "Bad format."}
        errors = validate_metadata(fm, "Invalid_Name")
        assert any("Invalid name" in e for e in errors)

    def test_description_too_long(self):
        fm = {"name": "my-skill", "description": "x" * 1025}
        errors = validate_metadata(fm, "my-skill")
        assert any("exceeds 1024" in e for e in errors)

    def test_unknown_fields(self):
        fm = {"name": "my-skill", "description": "OK.", "bogus_field": "bad"}
        errors = validate_metadata(fm, "my-skill")
        assert any("Unknown frontmatter field" in e for e in errors)


class TestLoadSkillMetadata:
    def test_load_valid(self, skill_dir: Path):
        meta = load_skill_metadata(skill_dir / "my-skill")
        assert meta is not None
        assert meta.name == "my-skill"
        assert meta.description == "A test skill for unit tests."
        assert meta.source == SkillSource.EXTERNAL
        assert meta.license == "MIT"
        assert meta.metadata == {"author": "test", "version": "1.0"}

    def test_load_missing_skill_md(self, tmp_path: Path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        assert load_skill_metadata(empty_dir) is None

    def test_load_invalid_returns_none(self, invalid_skill_dir: Path):
        # Missing name field
        assert load_skill_metadata(invalid_skill_dir / "bad-skill-1") is None
        # Name mismatch
        assert load_skill_metadata(invalid_skill_dir / "bad-skill-2") is None


class TestLoadSkillContent:
    def test_load_full_content(self, skill_dir: Path):
        meta = load_skill_metadata(skill_dir / "my-skill")
        assert meta is not None
        content = load_skill_content(meta)
        assert "full instructions" in content.instructions
        assert "helper.py" in content.scripts
        assert "print('hello')" in content.scripts["helper.py"]
        assert "guide.md" in content.references


class TestDiscoverSkills:
    def test_discover(self, skill_dir: Path):
        skills = discover_skills([str(skill_dir)])
        assert len(skills) == 1
        assert skills[0].name == "my-skill"

    def test_discover_nonexistent_dir(self):
        skills = discover_skills(["/nonexistent/path"])
        assert skills == []

    def test_discover_deduplication(self, skill_dir: Path):
        # Same directory listed twice
        skills = discover_skills([str(skill_dir), str(skill_dir)])
        assert len(skills) == 1

    def test_discover_skips_invalid(self, invalid_skill_dir: Path):
        skills = discover_skills([str(invalid_skill_dir)])
        assert len(skills) == 0


class TestAgentSkillsBridge:
    def test_get_tools(self):
        bridge = AgentSkillsBridge()
        tools = bridge.get_tools()
        assert len(tools) == 2
        names = {t.name for t in tools}
        assert names == {"load_skill", "read_skill_file"}

    @pytest.mark.asyncio
    async def test_load_skill(self, skill_dir: Path):
        meta = load_skill_metadata(skill_dir / "my-skill")
        assert meta is not None
        bridge = AgentSkillsBridge(skill_registry={meta.name: meta})

        result = await bridge.execute("load_skill", {"skill_name": "my-skill"})
        assert result.success
        assert "full instructions" in result.output

    @pytest.mark.asyncio
    async def test_load_skill_not_found(self):
        bridge = AgentSkillsBridge(skill_registry={})
        result = await bridge.execute("load_skill", {"skill_name": "nope"})
        assert not result.success
        assert "not found" in result.error

    @pytest.mark.asyncio
    async def test_read_skill_file(self, skill_dir: Path):
        meta = load_skill_metadata(skill_dir / "my-skill")
        assert meta is not None
        bridge = AgentSkillsBridge(skill_registry={meta.name: meta})

        result = await bridge.execute(
            "read_skill_file",
            {"skill_name": "my-skill", "file_path": "helper.py"},
        )
        assert result.success
        assert "print('hello')" in result.output

    @pytest.mark.asyncio
    async def test_read_skill_file_not_found(self, skill_dir: Path):
        meta = load_skill_metadata(skill_dir / "my-skill")
        assert meta is not None
        bridge = AgentSkillsBridge(skill_registry={meta.name: meta})

        result = await bridge.execute(
            "read_skill_file",
            {"skill_name": "my-skill", "file_path": "nonexistent.py"},
        )
        assert not result.success
        assert "not found" in result.error


class TestSkillLoaderIntegration:
    def test_from_config_with_skill_dirs(self, skill_dir: Path):
        from pulsebot.config import SkillsConfig
        from pulsebot.skills.loader import SkillLoader

        config = SkillsConfig(
            builtin=[],
            skill_dirs=[str(skill_dir)],
        )
        loader = SkillLoader.from_config(config)

        assert "my-skill" in loader.external_skills
        assert "agentskills_bridge" in loader.loaded_skills
        assert "load_skill" in loader.available_tools
        assert "read_skill_file" in loader.available_tools

    def test_format_skills_for_prompt(self, skill_dir: Path):
        from pulsebot.config import SkillsConfig
        from pulsebot.skills.loader import SkillLoader

        config = SkillsConfig(
            builtin=[],
            skill_dirs=[str(skill_dir)],
        )
        loader = SkillLoader.from_config(config)
        prompt = loader.format_skills_for_prompt()

        assert "my-skill" in prompt
        assert "A test skill for unit tests" in prompt
        assert "load_skill" in prompt

    def test_no_external_skills(self):
        from pulsebot.config import SkillsConfig
        from pulsebot.skills.loader import SkillLoader

        config = SkillsConfig(builtin=[], skill_dirs=[])
        loader = SkillLoader.from_config(config)

        assert loader.format_skills_for_prompt() == ""
        assert "agentskills_bridge" not in loader.loaded_skills

    def test_disabled_skills(self, skill_dir: Path):
        from pulsebot.config import SkillsConfig
        from pulsebot.skills.loader import SkillLoader

        config = SkillsConfig(
            builtin=[],
            skill_dirs=[str(skill_dir)],
            disabled_skills=["my-skill"],
        )
        loader = SkillLoader.from_config(config)

        assert "my-skill" not in loader.external_skills
        # Bridge should not be loaded since no external skills found
        assert "agentskills_bridge" not in loader.loaded_skills
