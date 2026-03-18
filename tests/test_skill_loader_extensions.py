"""Tests for SkillLoader extensions needed by multi-agent system."""

import pytest

from pulsebot.skills.loader import SkillLoader


@pytest.fixture
def loader_with_two_skills():
    loader = SkillLoader()
    loader.load_builtin("file_ops")
    loader.load_builtin("shell")
    return loader


def test_get_loaded_skills_returns_all_skills(loader_with_two_skills):
    skills = loader_with_two_skills.get_loaded_skills()
    names = {s.name for s in skills}
    assert "file_ops" in names
    assert "shell" in names


def test_get_loaded_skills_empty_loader():
    loader = SkillLoader()
    assert loader.get_loaded_skills() == []


def test_create_subset_returns_only_named_skills(loader_with_two_skills):
    subset = loader_with_two_skills.create_subset(["file_ops"])
    skills = subset.get_loaded_skills()
    names = {s.name for s in skills}
    assert names == {"file_ops"}


def test_create_subset_excludes_unknown_names(loader_with_two_skills):
    # Unknown names are silently skipped
    subset = loader_with_two_skills.create_subset(["file_ops", "nonexistent"])
    skills = subset.get_loaded_skills()
    names = {s.name for s in skills}
    assert names == {"file_ops"}


def test_create_subset_preserves_tool_routing(loader_with_two_skills):
    subset = loader_with_two_skills.create_subset(["shell"])
    # Shell tools should be routable
    skill = subset.get_skill_for_tool("run_command")
    assert skill is not None
    assert skill.name == "shell"


def test_create_subset_empty_list(loader_with_two_skills):
    subset = loader_with_two_skills.create_subset([])
    assert subset.get_loaded_skills() == []
