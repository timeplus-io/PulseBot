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
        assert mock_which.call_count == 1

    def test_invalidate_cache(self):
        checker = RequirementChecker()
        with patch("shutil.which", return_value="/usr/bin/python3"):
            checker._check_bin("python3")
        checker.invalidate_cache()
        assert "python3" not in checker._bin_cache
