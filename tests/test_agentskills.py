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


@pytest.fixture
def openclaw_skill_dir(tmp_path: Path) -> Path:
    """Create a skill with OpenClaw metadata."""
    skill = tmp_path / "my-skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\n"
        "name: my-skill\n"
        "description: A test skill with OpenClaw metadata.\n"
        "version: '1.2.3'\n"
        "metadata:\n"
        "  openclaw:\n"
        "    requires:\n"
        "      env:\n"
        "        - MY_API_KEY\n"
        "      bins:\n"
        "        - curl\n"
        "      anyBins:\n"
        "        - jq\n"
        "        - python3\n"
        "    primaryEnv: MY_API_KEY\n"
        "    always: false\n"
        "    emoji: '🔧'\n"
        "    os:\n"
        "      - darwin\n"
        "      - linux\n"
        "---\n\n"
        "# My Skill\n\nInstructions here.\n"
    )
    return tmp_path


class TestOpenClawMetadata:
    def test_load_openclaw_metadata(self, openclaw_skill_dir: Path):
        meta = load_skill_metadata(openclaw_skill_dir / "my-skill")
        assert meta is not None
        assert meta.openclaw is not None
        assert meta.openclaw.requires.env == ["MY_API_KEY"]
        assert meta.openclaw.requires.bins == ["curl"]
        assert meta.openclaw.requires.any_bins == ["jq", "python3"]
        assert meta.openclaw.primary_env == "MY_API_KEY"
        assert meta.openclaw.always is False
        assert meta.openclaw.emoji == "🔧"
        assert meta.openclaw.os == ["darwin", "linux"]

    def test_plain_skill_has_no_openclaw(self, skill_dir: Path):
        """Backward compat: plain agentskills.io skill has openclaw=None."""
        meta = load_skill_metadata(skill_dir / "my-skill")
        assert meta is not None
        assert meta.openclaw is None

    def test_openclaw_alias_clawdbot(self, tmp_path: Path):
        """metadata.clawdbot is an alias for metadata.openclaw."""
        skill = tmp_path / "my-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\n"
            "name: my-skill\n"
            "description: Uses clawdbot alias.\n"
            "metadata:\n"
            "  clawdbot:\n"
            "    always: true\n"
            "---\n\nBody.\n"
        )
        meta = load_skill_metadata(tmp_path / "my-skill")
        assert meta is not None
        assert meta.openclaw is not None
        assert meta.openclaw.always is True

    def test_version_field_accepted(self, tmp_path: Path):
        """OpenClaw adds 'version' as a top-level frontmatter field."""
        skill = tmp_path / "my-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\n"
            "name: my-skill\n"
            "description: Has version.\n"
            "version: '2.0.0'\n"
            "---\n\nBody.\n"
        )
        meta = load_skill_metadata(tmp_path / "my-skill")
        assert meta is not None  # must not fail validation
        assert meta.version == "2.0.0"

    def test_openclaw_optional_fields_default(self, tmp_path: Path):
        """All OpenClaw fields are optional; empty block works fine."""
        skill = tmp_path / "my-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\n"
            "name: my-skill\n"
            "description: Empty openclaw block.\n"
            "metadata:\n"
            "  openclaw: {}\n"
            "---\n\nBody.\n"
        )
        meta = load_skill_metadata(tmp_path / "my-skill")
        assert meta is not None
        assert meta.openclaw is not None
        assert meta.openclaw.requires.env == []
        assert meta.openclaw.requires.bins == []
        assert meta.openclaw.always is False

    def test_openclaw_null_requires_fields_default_to_empty(self, tmp_path: Path):
        """Explicit YAML null for requires sub-keys should yield empty lists, not None."""
        skill = tmp_path / "my-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\n"
            "name: my-skill\n"
            "description: Tests null handling.\n"
            "metadata:\n"
            "  openclaw:\n"
            "    requires:\n"
            "      env:\n"  # YAML null (no value)
            "      bins: ~\n"  # Explicit YAML null
            "---\n\nBody.\n"
        )
        meta = load_skill_metadata(tmp_path / "my-skill")
        assert meta is not None
        assert meta.openclaw is not None
        assert meta.openclaw.requires.env == []
        assert meta.openclaw.requires.bins == []


class TestSkillLoaderRequirementFiltering:
    def test_skill_filtered_when_binary_missing(self, tmp_path: Path):
        """Skills whose required binary is absent should not appear in external_skills."""
        skill = tmp_path / "my-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\n"
            "name: my-skill\n"
            "description: Needs a rare binary.\n"
            "metadata:\n"
            "  openclaw:\n"
            "    requires:\n"
            "      bins:\n"
            "        - totally-nonexistent-bin-xyz\n"
            "---\n\nBody.\n"
        )
        from pulsebot.config import SkillsConfig
        from pulsebot.skills.loader import SkillLoader

        config = SkillsConfig(builtin=[], skill_dirs=[str(tmp_path)])
        loader = SkillLoader.from_config(config)

        assert "my-skill" not in loader.external_skills

    def test_skill_passes_when_requirements_met(self, tmp_path: Path):
        """Skill with satisfied requirements should appear in external_skills."""
        skill = tmp_path / "my-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\n"
            "name: my-skill\n"
            "description: Needs python3.\n"
            "metadata:\n"
            "  openclaw:\n"
            "    requires:\n"
            "      bins:\n"
            "        - python3\n"
            "---\n\nBody.\n"
        )
        from pulsebot.config import SkillsConfig
        from pulsebot.skills.loader import SkillLoader
        from unittest.mock import patch

        config = SkillsConfig(builtin=[], skill_dirs=[str(tmp_path)])
        with patch("shutil.which", return_value="/usr/bin/python3"):
            loader = SkillLoader.from_config(config)

        assert "my-skill" in loader.external_skills

    def test_always_true_skill_never_filtered(self, tmp_path: Path):
        """Skills with always=true pass regardless of env/bins."""
        skill = tmp_path / "my-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\n"
            "name: my-skill\n"
            "description: Always active.\n"
            "metadata:\n"
            "  openclaw:\n"
            "    always: true\n"
            "    requires:\n"
            "      env:\n"
            "        - NONEXISTENT_ENV_XYZ\n"
            "---\n\nBody.\n"
        )
        from pulsebot.config import SkillsConfig
        from pulsebot.skills.loader import SkillLoader

        config = SkillsConfig(builtin=[], skill_dirs=[str(tmp_path)])
        loader = SkillLoader.from_config(config)

        assert "my-skill" in loader.external_skills


class TestClawHubConfig:
    def test_default_clawhub_config(self):
        from pulsebot.config import SkillsConfig
        config = SkillsConfig()
        assert config.clawhub.enabled is True
        assert config.clawhub.site_url == "https://clawhub.ai"
        assert config.clawhub.install_dir is None
        assert config.clawhub.verify_checksums is True

    def test_clawhub_config_from_dict(self):
        from pulsebot.config import SkillsConfig
        config = SkillsConfig(
            clawhub={
                "enabled": False,
                "site_url": "https://my-registry.example.com",
                "install_dir": "./my-skills",
            }
        )
        assert config.clawhub.enabled is False
        assert config.clawhub.site_url == "https://my-registry.example.com"
        assert config.clawhub.install_dir == "./my-skills"


class TestSkillCLI:
    def test_skill_list_no_skills(self, tmp_path: Path):
        """pulsebot skill list with no installed skills prints a message."""
        from click.testing import CliRunner
        from pulsebot.cli import cli

        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["skill", "list"])
        assert result.exit_code == 0
        assert "No ClawHub skills" in result.output

    def test_skill_remove_nonexistent(self, tmp_path: Path):
        """pulsebot skill remove with a slug not in lock file exits cleanly."""
        from click.testing import CliRunner
        from pulsebot.cli import cli

        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["skill", "remove", "nonexistent-skill"])
        assert result.exit_code == 0
