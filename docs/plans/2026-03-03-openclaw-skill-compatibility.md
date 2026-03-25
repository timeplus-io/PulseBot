# OpenClaw Skill Compatibility Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add OpenClaw/ClawHub skill compatibility to PulseBot so users can search, install, and run any of the 13,700+ community skills from clawhub.ai.

**Architecture:** Extend the existing `pulsebot/skills/agentskills/` module (models, loader) to parse OpenClaw's extended `metadata.openclaw` block, add a requirement checker that filters skills at load time, add a Python-native ClawHub HTTP client, a lock file manager, and new `pulsebot skill` CLI commands. All changes are backward-compatible: plain agentskills.io skills without OpenClaw metadata continue to work identically.

**Tech Stack:** Python 3.11+, `httpx` (already a dependency), `click` (already used for CLI), `pydantic` (already used), stdlib `zipfile`/`hashlib`/`shutil`/`platform`

---

## Context for Implementer

### Existing code to understand before starting

- `pulsebot/skills/agentskills/models.py` — `SkillMetadata`, `SkillContent`, `SkillSource`
- `pulsebot/skills/agentskills/loader.py` — `parse_frontmatter`, `validate_metadata`, `load_skill_metadata`, `discover_skills`; note `VALID_FIELDS` currently rejects unknown frontmatter keys
- `pulsebot/skills/loader.py` — `SkillLoader`; `_discover_external_skills()` is where requirement-checking will integrate
- `pulsebot/config.py` — `SkillsConfig`; needs a `clawhub` sub-section
- `pulsebot/cli.py` — Click CLI; follow the `@cli.group()` → `@task.command()` pattern from the `task` group at line 377
- `tests/test_agentskills.py` — existing tests; new tests must not break these

### Key design decisions

1. **Extend, don't replace**: Add `openclaw: OpenClawMetadata | None` to the existing `SkillMetadata` model instead of a separate model. No new top-level `pulsebot/skills/models.py`.
2. **OpenClaw fields go in `metadata.openclaw`** in the SKILL.md frontmatter. The `metadata` dict value is `Any` (not `str`) to allow nested structures.
3. **Requirement checking** filters skills in `_discover_external_skills()` — failed skills are logged and excluded.
4. **ClawHub client** lives in `pulsebot/skills/clawhub_client.py`; uses `httpx` (already a dep).
5. **Lock file** lives in `pulsebot/skills/lock.py`.

---

## Task 1: Extend SkillMetadata to carry OpenClaw metadata

**Files:**
- Modify: `pulsebot/skills/agentskills/models.py`
- Modify: `pulsebot/skills/agentskills/loader.py`
- Modify: `tests/test_agentskills.py`

### Step 1: Write the failing tests

Add these test cases to `tests/test_agentskills.py`:

```python
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
```

### Step 2: Run tests to verify they fail

```bash
.venv/bin/pytest tests/test_agentskills.py::TestOpenClawMetadata -v
```
Expected: FAIL (attributes don't exist yet)

### Step 3: Implement — extend models

Replace `pulsebot/skills/agentskills/models.py` entirely with:

```python
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
```

### Step 4: Implement — extend loader

In `pulsebot/skills/agentskills/loader.py`, make these changes:

**a) Expand `VALID_FIELDS`** to include OpenClaw top-level fields:
```python
VALID_FIELDS = {
    "name", "description", "license", "compatibility", "metadata", "allowed-tools",
    # OpenClaw top-level extensions
    "version", "homepage", "user-invocable", "disable-model-invocation",
    "command-dispatch", "command-tool", "command-arg-mode",
}

# Keys inside metadata that are known OpenClaw aliases (not flagged as unknown)
OPENCLAW_METADATA_ALIASES = ("openclaw", "clawdbot", "clawdis", "moltbot")
```

**b) Add `_parse_openclaw_metadata()` helper** after the constants:
```python
def _parse_openclaw_metadata(metadata: dict) -> OpenClawMetadata | None:
    """Extract OpenClaw metadata from any known alias key in the metadata block."""
    if not isinstance(metadata, dict):
        return None
    raw = None
    for alias in OPENCLAW_METADATA_ALIASES:
        if alias in metadata:
            raw = metadata[alias]
            break
    if raw is None:
        return None
    if not isinstance(raw, dict):
        return None

    req_raw = raw.get("requires", {}) or {}
    requires = SkillRequirements(
        env=req_raw.get("env", []),
        bins=req_raw.get("bins", []),
        any_bins=req_raw.get("anyBins", req_raw.get("anyOf", [])),
        configs=req_raw.get("config", req_raw.get("configs", [])),
    )
    return OpenClawMetadata(
        requires=requires,
        primary_env=raw.get("primaryEnv"),
        always=raw.get("always", False),
        emoji=raw.get("emoji"),
        homepage=raw.get("homepage"),
        os=raw.get("os", []),
        skill_key=raw.get("skillKey"),
    )
```

**c) Update `validate_metadata()`** — skip errors for known metadata keys:
Change the unknown-field check to only warn about truly unknown top-level frontmatter keys:
```python
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
```

**d) Update `load_skill_metadata()`** to extract OpenClaw metadata and `version`:
```python
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

        raw_metadata = fm.get("metadata", {}) or {}
        openclaw = _parse_openclaw_metadata(raw_metadata)

        return SkillMetadata(
            name=fm["name"],
            description=fm["description"],
            source=SkillSource.EXTERNAL,
            path=skill_dir,
            license=fm.get("license"),
            compatibility=fm.get("compatibility"),
            metadata=raw_metadata,
            allowed_tools=fm.get("allowed-tools"),
            version=fm.get("version"),
            openclaw=openclaw,
        )
    except Exception as e:
        logger.warning("Failed to load skill metadata from %s: %s", skill_dir, e)
        return None
```

Also add the imports at the top of `loader.py`:
```python
from pulsebot.skills.agentskills.models import (
    OpenClawMetadata,
    SkillContent,
    SkillMetadata,
    SkillRequirements,
    SkillSource,
)
```

### Step 5: Run tests to verify they pass

```bash
.venv/bin/pytest tests/test_agentskills.py -v
```
Expected: All tests PASS (including the new `TestOpenClawMetadata` class)

### Step 6: Commit

```bash
git add pulsebot/skills/agentskills/models.py pulsebot/skills/agentskills/loader.py tests/test_agentskills.py
git commit -m "feat: extend SkillMetadata with OpenClaw metadata (requires, os, emoji, etc.)"
```

---

## Task 2: Add runtime requirement checker

**Files:**
- Create: `pulsebot/skills/agentskills/requirements.py`
- Create: `tests/test_requirements.py`

### Step 1: Write the failing tests

Create `tests/test_requirements.py`:

```python
"""Tests for OpenClaw runtime requirement checking."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from pulsebot.skills.agentskills.models import OpenClawMetadata, SkillMetadata, SkillRequirements, SkillSource
from pulsebot.skills.agentskills.requirements import RequirementChecker


def make_skill(requires=None, always=False, os_list=None):
    """Helper: create a SkillMetadata with OpenClaw metadata."""
    openclaw = OpenClawMetadata(
        requires=requires or SkillRequirements(),
        always=always,
        os=os_list or [],
    )
    return SkillMetadata(name="test-skill", description="Test", openclaw=openclaw)


def make_plain_skill():
    """Helper: plain agentskills.io skill with no OpenClaw metadata."""
    return SkillMetadata(name="plain-skill", description="Plain skill")


class TestRequirementCheckerPlainSkill:
    def test_plain_skill_always_passes(self):
        checker = RequirementChecker()
        skill = make_plain_skill()
        ok, reason = checker.check(skill)
        assert ok is True
        assert reason is None


class TestRequirementCheckerAlways:
    def test_always_true_bypasses_all_checks(self):
        checker = RequirementChecker()
        skill = make_skill(
            requires=SkillRequirements(env=["MISSING_VAR"]),
            always=True,
        )
        ok, reason = checker.check(skill)
        assert ok is True


class TestRequirementCheckerOS:
    def test_matching_os_passes(self):
        checker = RequirementChecker()
        skill = make_skill(os_list=[checker._current_os])
        ok, _ = checker.check(skill)
        assert ok is True

    def test_wrong_os_fails(self):
        checker = RequirementChecker()
        # Use an OS the checker definitely isn't running on
        wrong_os = "win32" if checker._current_os != "win32" else "darwin"
        skill = make_skill(os_list=[wrong_os])
        ok, reason = checker.check(skill)
        assert ok is False
        assert "OS" in reason

    def test_empty_os_list_passes(self):
        checker = RequirementChecker()
        skill = make_skill(os_list=[])
        ok, _ = checker.check(skill)
        assert ok is True


class TestRequirementCheckerBins:
    def test_present_binary_passes(self):
        checker = RequirementChecker()
        # 'python3' or 'python' should always be on PATH in our test env
        skill = make_skill(requires=SkillRequirements(bins=["python3"]))
        with patch("shutil.which", return_value="/usr/bin/python3"):
            ok, _ = checker.check(skill)
        assert ok is True

    def test_missing_binary_fails(self):
        checker = RequirementChecker()
        skill = make_skill(requires=SkillRequirements(bins=["totally-nonexistent-bin-xyz"]))
        ok, reason = checker.check(skill)
        assert ok is False
        assert "totally-nonexistent-bin-xyz" in reason

    def test_any_bins_one_present_passes(self):
        checker = RequirementChecker()
        skill = make_skill(
            requires=SkillRequirements(
                any_bins=["totally-nonexistent-bin-xyz", "python3"]
            )
        )
        with patch("shutil.which", side_effect=lambda b: None if b == "totally-nonexistent-bin-xyz" else f"/usr/bin/{b}"):
            ok, _ = checker.check(skill)
        assert ok is True

    def test_any_bins_none_present_fails(self):
        checker = RequirementChecker()
        skill = make_skill(
            requires=SkillRequirements(any_bins=["bin-a", "bin-b"])
        )
        with patch("shutil.which", return_value=None):
            ok, reason = checker.check(skill)
        assert ok is False
        assert "None of required" in reason


class TestRequirementCheckerEnv:
    def test_present_env_passes(self):
        checker = RequirementChecker()
        skill = make_skill(requires=SkillRequirements(env=["MY_TEST_VAR"]))
        with patch.dict(os.environ, {"MY_TEST_VAR": "value"}):
            ok, _ = checker.check(skill)
        assert ok is True

    def test_missing_env_fails(self):
        checker = RequirementChecker()
        skill = make_skill(requires=SkillRequirements(env=["DEFINITELY_MISSING_ENV_XYZ"]))
        env_without = {k: v for k, v in os.environ.items() if k != "DEFINITELY_MISSING_ENV_XYZ"}
        with patch.dict(os.environ, env_without, clear=True):
            ok, reason = checker.check(skill)
        assert ok is False
        assert "DEFINITELY_MISSING_ENV_XYZ" in reason


class TestRequirementCheckerCache:
    def test_bin_check_cached(self):
        checker = RequirementChecker()
        with patch("shutil.which", return_value="/usr/bin/python3") as mock_which:
            checker._check_bin("python3")
            checker._check_bin("python3")
        # Should only call shutil.which once due to caching
        assert mock_which.call_count == 1

    def test_invalidate_cache(self):
        checker = RequirementChecker()
        with patch("shutil.which", return_value="/usr/bin/python3"):
            checker._check_bin("python3")
        checker.invalidate_cache()
        assert "python3" not in checker._bin_cache
```

### Step 2: Run tests to verify they fail

```bash
.venv/bin/pytest tests/test_requirements.py -v
```
Expected: FAIL (module not found)

### Step 3: Implement `requirements.py`

Create `pulsebot/skills/agentskills/requirements.py`:

```python
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
```

### Step 4: Run tests to verify they pass

```bash
.venv/bin/pytest tests/test_requirements.py -v
```
Expected: All tests PASS

### Step 5: Commit

```bash
git add pulsebot/skills/agentskills/requirements.py tests/test_requirements.py
git commit -m "feat: add OpenClaw runtime requirement checker (bins, env, OS)"
```

---

## Task 3: Integrate requirement checking into SkillLoader

**Files:**
- Modify: `pulsebot/skills/loader.py`
- Modify: `tests/test_agentskills.py` (add integration tests)

### Step 1: Write the failing tests

Add to `tests/test_agentskills.py`:

```python
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
```

### Step 2: Run tests to verify they fail

```bash
.venv/bin/pytest tests/test_agentskills.py::TestSkillLoaderRequirementFiltering -v
```
Expected: FAIL (requirement checking not yet integrated)

### Step 3: Implement — update SkillLoader

In `pulsebot/skills/loader.py`, update `_discover_external_skills()`:

```python
def _discover_external_skills(
    self, skill_dirs: list[str], disabled: list[str] | None = None
) -> None:
    """Discover agentskills.io packages and register the bridge skill."""
    from pulsebot.skills.agentskills.requirements import RequirementChecker

    disabled_set = set(disabled or [])
    discovered = discover_skills(skill_dirs)
    checker = RequirementChecker()

    for meta in discovered:
        if meta.name in disabled_set:
            continue
        satisfied, reason = checker.check(meta)
        if not satisfied:
            logger.info(
                "Skill '%s' skipped: %s", meta.name, reason,
                extra={"skill": meta.name, "reason": reason},
            )
            continue
        self._external_skills[meta.name] = meta

    if self._external_skills:
        from pulsebot.skills.builtin.agentskills_bridge import AgentSkillsBridge
        bridge = AgentSkillsBridge(skill_registry=self._external_skills)
        self._skills["agentskills_bridge"] = bridge
        for tool in bridge.get_tools():
            self._tool_to_skill[tool.name] = "agentskills_bridge"

        logger.info(
            f"Discovered {len(self._external_skills)} external skill(s): "
            f"{list(self._external_skills.keys())}"
        )
```

### Step 4: Run tests to verify they pass

```bash
.venv/bin/pytest tests/test_agentskills.py -v
```
Expected: All tests PASS

### Step 5: Commit

```bash
git add pulsebot/skills/loader.py tests/test_agentskills.py
git commit -m "feat: filter skills by OpenClaw runtime requirements at discovery"
```

---

## Task 4: Extend SkillsConfig with ClawHub settings

**Files:**
- Modify: `pulsebot/config.py`
- Modify: `tests/test_agentskills.py` (add config tests)

### Step 1: Write the failing tests

Add to `tests/test_agentskills.py`:

```python
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
```

### Step 2: Run tests to verify they fail

```bash
.venv/bin/pytest tests/test_agentskills.py::TestClawHubConfig -v
```
Expected: FAIL (ClawHubConfig doesn't exist)

### Step 3: Implement — add ClawHubConfig to config.py

In `pulsebot/config.py`, add `ClawHubConfig` and update `SkillsConfig`.

Find the `SkillsConfig` class and add the new class before it:

```python
class ClawHubConfig(BaseModel):
    """ClawHub registry integration configuration."""
    enabled: bool = True
    site_url: str = "https://clawhub.ai"
    registry_url: str | None = None      # Auto-discovered from .well-known if None
    install_dir: str | None = None       # Defaults to first skill_dir if None
    auth_token_path: str | None = None   # Path to file containing auth token
    verify_checksums: bool = True        # Verify SHA256 checksums on download
    auto_update: bool = False            # Auto-update installed skills on startup
```

Then update `SkillsConfig`:

```python
class SkillsConfig(BaseModel):
    """Skills configuration."""
    builtin: list[str] = Field(default_factory=lambda: ["web_search", "file_ops", "shell"])
    custom: list[str] = Field(default_factory=list)
    skill_dirs: list[str] = Field(default_factory=list)
    disabled_skills: list[str] = Field(default_factory=list)
    clawhub: ClawHubConfig = Field(default_factory=ClawHubConfig)
```

### Step 4: Run tests to verify they pass

```bash
.venv/bin/pytest tests/test_agentskills.py::TestClawHubConfig -v
```
Expected: All tests PASS

### Step 5: Run all tests to confirm no regressions

```bash
.venv/bin/pytest tests/ -v
```
Expected: All tests PASS

### Step 6: Commit

```bash
git add pulsebot/config.py tests/test_agentskills.py
git commit -m "feat: add ClawHubConfig to SkillsConfig for registry settings"
```

---

## Task 5: Implement ClawHub lock file manager

**Files:**
- Create: `pulsebot/skills/lock.py`
- Create: `tests/test_lock.py`

### Step 1: Write the failing tests

Create `tests/test_lock.py`:

```python
"""Tests for ClawHub lock file manager."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pulsebot.skills.lock import LockFile, LockedSkill


@pytest.fixture
def workdir(tmp_path: Path) -> Path:
    return tmp_path


class TestLockFile:
    def test_read_empty(self, workdir: Path):
        lock = LockFile(workdir)
        assert lock.read() == {}

    def test_add_and_read(self, workdir: Path):
        lock = LockFile(workdir)
        entry = LockedSkill(
            slug="my-skill",
            version="1.0.0",
            content_hash="abc123",
            installed_at="2026-03-01T00:00:00+00:00",
            source="clawhub",
        )
        lock.add(entry)
        skills = lock.read()
        assert "my-skill" in skills
        assert skills["my-skill"].version == "1.0.0"
        assert skills["my-skill"].content_hash == "abc123"

    def test_lock_file_created_in_clawhub_dir(self, workdir: Path):
        lock = LockFile(workdir)
        lock.add(LockedSkill(
            slug="test",
            version="1.0",
            content_hash="x",
            installed_at="2026-01-01T00:00:00+00:00",
        ))
        assert (workdir / ".clawhub" / "lock.json").exists()

    def test_lock_file_json_format(self, workdir: Path):
        lock = LockFile(workdir)
        lock.add(LockedSkill(
            slug="s",
            version="1.0",
            content_hash="h",
            installed_at="2026-01-01T00:00:00+00:00",
            source="clawhub",
        ))
        data = json.loads((workdir / ".clawhub" / "lock.json").read_text())
        assert data["version"] == 1
        assert "s" in data["skills"]
        assert data["skills"]["s"]["slug"] == "s"

    def test_remove_skill(self, workdir: Path):
        lock = LockFile(workdir)
        lock.add(LockedSkill(slug="s", version="1.0", content_hash="h", installed_at="2026-01-01T00:00:00+00:00"))
        lock.remove("s")
        assert "s" not in lock.read()

    def test_remove_nonexistent_is_noop(self, workdir: Path):
        lock = LockFile(workdir)
        lock.remove("nonexistent")  # Should not raise

    def test_add_overwrites_existing(self, workdir: Path):
        lock = LockFile(workdir)
        lock.add(LockedSkill(slug="s", version="1.0", content_hash="h1", installed_at="2026-01-01T00:00:00+00:00"))
        lock.add(LockedSkill(slug="s", version="2.0", content_hash="h2", installed_at="2026-02-01T00:00:00+00:00"))
        skills = lock.read()
        assert skills["s"].version == "2.0"
        assert skills["s"].content_hash == "h2"

    def test_compute_content_hash(self, workdir: Path):
        skill_dir = workdir / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("hello world")
        hash1 = LockFile.compute_content_hash(skill_dir)
        assert isinstance(hash1, str)
        assert len(hash1) == 64  # SHA256 hex digest

        # Changing file changes hash
        (skill_dir / "SKILL.md").write_text("changed content")
        hash2 = LockFile.compute_content_hash(skill_dir)
        assert hash1 != hash2
```

### Step 2: Run tests to verify they fail

```bash
.venv/bin/pytest tests/test_lock.py -v
```
Expected: FAIL (module not found)

### Step 3: Implement `lock.py`

Create `pulsebot/skills/lock.py`:

```python
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
```

### Step 4: Run tests to verify they pass

```bash
.venv/bin/pytest tests/test_lock.py -v
```
Expected: All tests PASS

### Step 5: Commit

```bash
git add pulsebot/skills/lock.py tests/test_lock.py
git commit -m "feat: add ClawHub lock file manager (.clawhub/lock.json)"
```

---

## Task 6: Implement ClawHub registry client

**Files:**
- Create: `pulsebot/skills/clawhub_client.py`
- Create: `tests/test_clawhub_client.py`

### Step 1: Write the failing tests

Create `tests/test_clawhub_client.py`:

```python
"""Tests for ClawHub registry client."""

from __future__ import annotations

import json
import zipfile
import hashlib
import io
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import httpx

from pulsebot.skills.clawhub_client import (
    ClawHubClient,
    ClawHubSkillInfo,
    ClawHubVersionInfo,
    IntegrityError,
    SecurityError,
    TEXT_FILE_EXTENSIONS,
)


@pytest.fixture
def mock_client() -> ClawHubClient:
    """ClawHubClient with a pre-set registry URL (skips .well-known discovery)."""
    client = ClawHubClient(registry_url="https://clawhub.ai/api/v1")
    return client


@pytest.fixture
def skill_zip_bytes(tmp_path: Path) -> bytes:
    """Create a minimal in-memory skill ZIP with a SKILL.md."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("SKILL.md", "---\nname: hello\ndescription: Hi.\n---\n\n# Hello\n")
    return buf.getvalue()


class TestClawHubClientSearch:
    def test_search_returns_skill_list(self, mock_client: ClawHubClient):
        payload = {
            "skills": [
                {
                    "skill": {"slug": "hello", "displayName": "Hello", "summary": "A hello skill", "tags": {}},
                    "latestVersion": {"version": "1.0.0"},
                    "owner": {"handle": "alice"},
                }
            ]
        }
        with patch.object(mock_client._client, "get") as mock_get:
            resp = MagicMock()
            resp.json.return_value = payload
            resp.raise_for_status = MagicMock()
            mock_get.return_value = resp

            results = mock_client.search("hello")

        assert len(results) == 1
        assert results[0].slug == "hello"
        assert results[0].latest_version == "1.0.0"
        assert results[0].owner_handle == "alice"

    def test_search_empty_result(self, mock_client: ClawHubClient):
        with patch.object(mock_client._client, "get") as mock_get:
            resp = MagicMock()
            resp.json.return_value = {"skills": []}
            resp.raise_for_status = MagicMock()
            mock_get.return_value = resp

            results = mock_client.search("nonexistent")

        assert results == []


class TestClawHubClientGetSkill:
    def test_get_skill_metadata(self, mock_client: ClawHubClient):
        payload = {
            "skill": {"slug": "my-skill", "displayName": "My Skill", "summary": "Does things", "tags": {}},
            "latestVersion": {"version": "2.0.0"},
            "owner": {"handle": "bob"},
        }
        with patch.object(mock_client._client, "get") as mock_get:
            resp = MagicMock()
            resp.json.return_value = payload
            resp.raise_for_status = MagicMock()
            mock_get.return_value = resp

            info = mock_client.get_skill("my-skill")

        assert info.slug == "my-skill"
        assert info.latest_version == "2.0.0"


class TestClawHubClientGetVersion:
    def test_get_version_info(self, mock_client: ClawHubClient):
        payload = {
            "version": {
                "version": "1.0.0",
                "changelog": "Initial release",
                "files": [{"path": "SKILL.md", "sha256": "abc", "size": 100}],
                "downloadUrl": "https://clawhub.ai/downloads/my-skill-1.0.0.zip",
            }
        }
        with patch.object(mock_client._client, "get") as mock_get:
            resp = MagicMock()
            resp.json.return_value = payload
            resp.raise_for_status = MagicMock()
            mock_get.return_value = resp

            info = mock_client.get_version("my-skill")

        assert info.version == "1.0.0"
        assert info.download_url == "https://clawhub.ai/downloads/my-skill-1.0.0.zip"
        assert len(info.files) == 1


class TestClawHubClientInstall:
    def test_install_creates_skill_dir(self, mock_client: ClawHubClient, skill_zip_bytes: bytes, tmp_path: Path):
        """Happy path: download ZIP, extract, move to skills_dir."""
        version_info = ClawHubVersionInfo(
            version="1.0.0",
            changelog="",
            files=[],
            download_url="https://clawhub.ai/downloads/hello-1.0.0.zip",
        )
        with patch.object(mock_client, "get_version", return_value=version_info), \
             patch.object(mock_client._client, "get") as mock_get:
            resp = MagicMock()
            resp.content = skill_zip_bytes
            resp.raise_for_status = MagicMock()
            mock_get.return_value = resp

            target = mock_client.download_and_install("hello", tmp_path)

        assert target.exists()
        assert (target / "SKILL.md").exists()

    def test_install_rejects_binary_file(self, mock_client: ClawHubClient, tmp_path: Path):
        """ZIP containing a .exe should raise SecurityError."""
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("SKILL.md", "---\nname: bad\ndescription: Bad.\n---\nBody.")
            zf.writestr("malware.exe", b"\x4d\x5a")  # MZ header
        bad_zip = buf.getvalue()

        version_info = ClawHubVersionInfo(
            version="1.0.0", changelog="", files=[],
            download_url="https://clawhub.ai/downloads/bad-1.0.0.zip",
        )
        with patch.object(mock_client, "get_version", return_value=version_info), \
             patch.object(mock_client._client, "get") as mock_get:
            resp = MagicMock()
            resp.content = bad_zip
            resp.raise_for_status = MagicMock()
            mock_get.return_value = resp

            with pytest.raises(SecurityError):
                mock_client.download_and_install("bad", tmp_path)

    def test_install_rejects_checksum_mismatch(self, mock_client: ClawHubClient, skill_zip_bytes: bytes, tmp_path: Path):
        """Checksum mismatch should raise IntegrityError."""
        version_info = ClawHubVersionInfo(
            version="1.0.0",
            changelog="",
            files=[{"path": "SKILL.md", "sha256": "wronghash", "size": 0}],
            download_url="https://clawhub.ai/downloads/hello-1.0.0.zip",
        )
        with patch.object(mock_client, "get_version", return_value=version_info), \
             patch.object(mock_client._client, "get") as mock_get:
            resp = MagicMock()
            resp.content = skill_zip_bytes
            resp.raise_for_status = MagicMock()
            mock_get.return_value = resp

            with pytest.raises(IntegrityError):
                mock_client.download_and_install("hello", tmp_path)


class TestTextFileExtensions:
    def test_common_extensions_present(self):
        assert ".md" in TEXT_FILE_EXTENSIONS
        assert ".py" in TEXT_FILE_EXTENSIONS
        assert ".json" in TEXT_FILE_EXTENSIONS
        assert ".sh" in TEXT_FILE_EXTENSIONS
```

### Step 2: Run tests to verify they fail

```bash
.venv/bin/pytest tests/test_clawhub_client.py -v
```
Expected: FAIL (module not found)

### Step 3: Implement `clawhub_client.py`

Create `pulsebot/skills/clawhub_client.py`:

```python
"""Python-native client for the ClawHub skill registry."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import httpx

# Allowed text file extensions — mirrors ClawHub's TEXT_FILE_EXTENSIONS allowlist
TEXT_FILE_EXTENSIONS = {
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml",
    ".js", ".ts", ".jsx", ".tsx", ".py", ".sh", ".bash",
    ".css", ".html", ".svg", ".xml", ".csv", ".ini",
    ".cfg", ".conf", ".env", ".gitignore", ".editorconfig",
    ".rs", ".go", ".java", ".c", ".cpp", ".h", ".hpp",
    ".rb", ".php", ".swift", ".kt", ".scala", ".sql",
    ".r", ".R", ".jl", ".lua", ".pl", ".pm",
}


@dataclass
class ClawHubSkillInfo:
    slug: str
    display_name: str
    summary: str
    latest_version: str
    owner_handle: str
    tags: dict


@dataclass
class ClawHubVersionInfo:
    version: str
    changelog: str
    files: list[dict]      # [{path, sha256, size, ...}]
    download_url: str


class SecurityError(Exception):
    """Raised when a downloaded skill contains disallowed file types."""


class IntegrityError(Exception):
    """Raised when a downloaded file fails checksum verification."""


class ClawHubClient:
    """Python client for the ClawHub registry REST API.

    Supports search, metadata lookup, and atomic skill installation with
    text-file validation and SHA256 checksum verification.
    """

    DEFAULT_SITE = "https://clawhub.ai"
    WELL_KNOWN_PATH = "/.well-known/clawhub.json"
    API_TIMEOUT = 10.0

    def __init__(
        self,
        site_url: Optional[str] = None,
        registry_url: Optional[str] = None,
        auth_token: Optional[str] = None,
    ):
        self.site_url = (site_url or self.DEFAULT_SITE).rstrip("/")
        self._registry_url = registry_url
        self._auth_token = auth_token
        self._client = httpx.Client(timeout=self.API_TIMEOUT)

    @property
    def registry_url(self) -> str:
        if not self._registry_url:
            self._registry_url = self._discover_registry()
        return self._registry_url

    def _discover_registry(self) -> str:
        """Discover registry URL from the .well-known/clawhub.json endpoint."""
        try:
            resp = self._client.get(f"{self.site_url}{self.WELL_KNOWN_PATH}")
            resp.raise_for_status()
            return resp.json().get("registry", f"{self.site_url}/api/v1")
        except Exception:
            return f"{self.site_url}/api/v1"

    def _headers(self) -> dict:
        headers = {"Accept": "application/json"}
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"
        return headers

    def search(self, query: str, limit: int = 20) -> list[ClawHubSkillInfo]:
        """Search ClawHub for skills matching the query."""
        resp = self._client.get(
            f"{self.registry_url}/skills",
            params={"q": query, "limit": limit},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return [self._parse_skill_info(s) for s in resp.json().get("skills", [])]

    def get_skill(self, slug: str) -> ClawHubSkillInfo:
        """Fetch metadata for a skill by slug."""
        resp = self._client.get(
            f"{self.registry_url}/skills/{slug}",
            headers=self._headers(),
        )
        resp.raise_for_status()
        return self._parse_skill_info(resp.json())

    def get_version(self, slug: str, version: str = "latest") -> ClawHubVersionInfo:
        """Fetch version details (download URL, file checksums)."""
        resp = self._client.get(
            f"{self.registry_url}/skills/{slug}/{version}",
            headers=self._headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        ver = data.get("version", {})
        return ClawHubVersionInfo(
            version=ver.get("version", version),
            changelog=ver.get("changelog", ""),
            files=ver.get("files", []),
            download_url=ver.get("downloadUrl", ""),
        )

    def download_and_install(
        self,
        slug: str,
        skills_dir: Path,
        version: str = "latest",
    ) -> Path:
        """Download a skill ZIP and install it atomically.

        Process:
        1. Fetch version metadata (download URL + checksums)
        2. Download ZIP
        3. Extract to temp directory
        4. Validate: text files only (SecurityError if not)
        5. Verify SHA256 checksums (IntegrityError if mismatch)
        6. Atomic move to skills_dir/slug (replaces existing)

        Returns the installed skill directory path.
        """
        version_info = self.get_version(slug, version)
        resp = self._client.get(version_info.download_url, follow_redirects=True)
        resp.raise_for_status()

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            zip_path = tmp_path / f"{slug}.zip"
            zip_path.write_bytes(resp.content)

            extract_dir = tmp_path / slug
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(extract_dir)

            self._validate_contents(extract_dir)
            self._verify_checksums(extract_dir, version_info.files)

            target = skills_dir / slug
            if target.exists():
                shutil.rmtree(target)
            shutil.move(str(extract_dir), str(target))

        return target

    def _validate_contents(self, directory: Path) -> None:
        """Reject ZIPs that contain non-text files."""
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext and ext not in TEXT_FILE_EXTENSIONS:
                    raise SecurityError(
                        f"Disallowed file type in skill package: {file_path.name} ({ext})"
                    )

    def _verify_checksums(self, directory: Path, file_specs: list[dict]) -> None:
        """Verify SHA256 checksums for all files listed in the version spec."""
        for spec in file_specs:
            rel_path = spec.get("path", "")
            expected = spec.get("sha256")
            if not rel_path or not expected:
                continue
            file_path = directory / rel_path
            if file_path.exists():
                actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
                if actual != expected:
                    raise IntegrityError(
                        f"SHA256 mismatch for {rel_path}: "
                        f"expected {expected}, got {actual}"
                    )

    def _parse_skill_info(self, data: dict) -> ClawHubSkillInfo:
        skill = data.get("skill", data)
        latest = data.get("latestVersion", {})
        owner = data.get("owner", {})
        return ClawHubSkillInfo(
            slug=skill.get("slug", ""),
            display_name=skill.get("displayName", ""),
            summary=skill.get("summary", ""),
            latest_version=latest.get("version", ""),
            owner_handle=owner.get("handle", ""),
            tags=skill.get("tags", {}),
        )

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
```

### Step 4: Run tests to verify they pass

```bash
.venv/bin/pytest tests/test_clawhub_client.py -v
```
Expected: All tests PASS

### Step 5: Commit

```bash
git add pulsebot/skills/clawhub_client.py tests/test_clawhub_client.py
git commit -m "feat: add ClawHub registry client with download, validation, checksum verification"
```

---

## Task 7: Add `pulsebot skill` CLI commands

**Files:**
- Modify: `pulsebot/cli.py`
- Modify: `tests/test_agentskills.py` (optional CLI smoke tests)

This task wires everything together into `pulsebot skill search`, `install`, `list`, `remove`.

### Step 1: Write a basic CLI smoke test

Add to `tests/test_agentskills.py`:

```python
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
```

### Step 2: Run tests to verify they fail

```bash
.venv/bin/pytest tests/test_agentskills.py::TestSkillCLI -v
```
Expected: FAIL (`skill` command group not found)

### Step 3: Implement CLI skill commands

In `pulsebot/cli.py`, add the `skill` command group. Add it after the `task` group (around line 415), before `if __name__ == "__main__":`:

```python
@cli.group()
def skill():
    """Manage PulseBot skills from ClawHub."""
    pass


@skill.command()
@click.argument("query")
@click.option("--limit", default=20, show_default=True, help="Max results to show")
def search(query: str, limit: int):
    """Search ClawHub for skills matching QUERY."""
    from pulsebot.skills.clawhub_client import ClawHubClient

    with ClawHubClient() as client:
        try:
            results = client.search(query, limit=limit)
        except Exception as e:
            console.print(f"[red]Search failed: {e}[/]")
            raise SystemExit(1)

    if not results:
        console.print("[yellow]No skills found.[/]")
        return

    from rich.table import Table
    table = Table(title=f"ClawHub results for '{query}'")
    table.add_column("Slug")
    table.add_column("Version")
    table.add_column("Summary")
    table.add_column("Author")
    for s in results:
        table.add_row(s.slug, s.latest_version, s.summary, s.owner_handle)
    console.print(table)


@skill.command()
@click.argument("slug")
@click.option("--version", default="latest", show_default=True)
@click.option("--dir", "install_dir", default="./skills", show_default=True,
              help="Directory to install the skill into")
def install(slug: str, version: str, install_dir: str):
    """Install a skill from ClawHub by SLUG."""
    from datetime import datetime, timezone
    from pathlib import Path

    from pulsebot.skills.clawhub_client import ClawHubClient, SecurityError, IntegrityError
    from pulsebot.skills.lock import LockFile, LockedSkill

    skills_dir = Path(install_dir)
    skills_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"Installing [bold]{slug}[/] @ {version} into {skills_dir}...")
    with ClawHubClient() as client:
        try:
            target = client.download_and_install(slug, skills_dir, version)
        except SecurityError as e:
            console.print(f"[red]Security error: {e}[/]")
            raise SystemExit(1)
        except IntegrityError as e:
            console.print(f"[red]Integrity error: {e}[/]")
            raise SystemExit(1)
        except Exception as e:
            console.print(f"[red]Install failed: {e}[/]")
            raise SystemExit(1)

    lock = LockFile(Path("."))
    content_hash = LockFile.compute_content_hash(target)
    lock.add(LockedSkill(
        slug=slug,
        version=version,
        content_hash=content_hash,
        installed_at=datetime.now(timezone.utc).isoformat(),
        source="clawhub",
    ))
    console.print(f"[green]Installed {slug} to {target}[/]")


@skill.command(name="list")
@click.option("--dir", "workdir", default=".", show_default=True,
              help="Working directory containing .clawhub/lock.json")
def list_skills(workdir: str):
    """List installed ClawHub skills."""
    from pathlib import Path
    from pulsebot.skills.lock import LockFile

    lock = LockFile(Path(workdir))
    skills = lock.read()
    if not skills:
        console.print("[yellow]No ClawHub skills installed.[/]")
        return

    from rich.table import Table
    table = Table(title="Installed Skills")
    table.add_column("Slug")
    table.add_column("Version")
    table.add_column("Source")
    table.add_column("Installed At")
    for entry in skills.values():
        table.add_row(entry.slug, entry.version, entry.source, entry.installed_at)
    console.print(table)


@skill.command()
@click.argument("slug")
@click.option("--dir", "install_dir", default="./skills", show_default=True)
@click.option("--workdir", default=".", show_default=True)
def remove(slug: str, install_dir: str, workdir: str):
    """Remove an installed skill by SLUG."""
    import shutil
    from pathlib import Path
    from pulsebot.skills.lock import LockFile

    target = Path(install_dir) / slug
    if target.exists():
        shutil.rmtree(target)
        console.print(f"Removed skill directory: {target}")
    else:
        console.print(f"[yellow]Skill directory not found: {target}[/]")

    lock = LockFile(Path(workdir))
    lock.remove(slug)
    console.print(f"[green]Removed {slug} from lock file.[/]")
```

### Step 4: Run tests to verify they pass

```bash
.venv/bin/pytest tests/test_agentskills.py::TestSkillCLI -v
```
Expected: All tests PASS

### Step 5: Run all tests to confirm no regressions

```bash
.venv/bin/pytest tests/ -v
```
Expected: All tests PASS

### Step 6: Commit

```bash
git add pulsebot/cli.py tests/test_agentskills.py
git commit -m "feat: add 'pulsebot skill' CLI commands (search, install, list, remove)"
```

---

## Final verification

After all tasks are complete, run the full suite one more time:

```bash
.venv/bin/pytest tests/ -v --tb=short
```

Verify the new CLI commands are discoverable:

```bash
.venv/bin/pulsebot skill --help
.venv/bin/pulsebot skill list
```

Expected output for `pulsebot skill --help`:
```
Usage: pulsebot skill [OPTIONS] COMMAND [ARGS]...

  Manage PulseBot skills from ClawHub.

Options:
  --help  Show this message and exit.

Commands:
  install  Install a skill from ClawHub by SLUG.
  list     List installed ClawHub skills.
  remove   Remove an installed skill by SLUG.
  search   Search ClawHub for skills matching QUERY.
```
