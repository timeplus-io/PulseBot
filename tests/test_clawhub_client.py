"""Tests for ClawHub registry client."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pulsebot.skills.clawhub_client import (
    ClawHubClient,
    ClawHubVersionInfo,
    IntegrityError,
    SecurityError,
    TEXT_FILE_EXTENSIONS,
)


@pytest.fixture
def mock_client() -> ClawHubClient:
    """ClawHubClient with a pre-set registry URL (skips .well-known discovery)."""
    return ClawHubClient(registry_url="https://clawhub.ai/api/v1")


@pytest.fixture
def skill_zip_bytes() -> bytes:
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
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("SKILL.md", "---\nname: bad\ndescription: Bad.\n---\nBody.")
            zf.writestr("malware.exe", b"\x4d\x5a")
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
