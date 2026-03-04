"""Tests for ClawHub lock file manager."""

from __future__ import annotations

import json
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
