"""Python-native client for the ClawHub skill registry."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import httpx

# Allowed text file extensions — mirrors ClawHub's TEXT_FILE_EXTENSIONS allowlist
TEXT_FILE_EXTENSIONS = {
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml",
    ".js", ".mjs", ".cjs", ".ts", ".jsx", ".tsx", ".py", ".sh", ".bash",
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
        """Discover registry URL from the .well-known/clawhub.json endpoint.

        The well-known endpoint returns a base URL (e.g. "https://clawhub.ai")
        under the "apiBase" key. The actual REST API lives at <apiBase>/api/v1.
        """
        try:
            resp = self._client.get(f"{self.site_url}{self.WELL_KNOWN_PATH}")
            resp.raise_for_status()
            data = resp.json()
            base = data.get("apiBase") or data.get("registry") or self.site_url
            return f"{base.rstrip('/')}/api/v1"
        except Exception:
            return f"{self.site_url}/api/v1"

    def _headers(self) -> dict:
        headers = {"Accept": "application/json"}
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"
        return headers

    def search(self, query: str, limit: int = 20) -> list[ClawHubSkillInfo]:
        """Search ClawHub for skills matching the query.

        Uses the /api/v1/search endpoint which performs semantic similarity
        search via embeddings. Returns results under the "results" key.
        """
        resp = self._client.get(
            f"{self.registry_url}/search",
            params={"q": query, "limit": limit},
            headers=self._headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return [self._parse_search_result(s) for s in data.get("results", [])]

    def get_skill(self, slug: str) -> ClawHubSkillInfo:
        """Fetch metadata for a skill by slug."""
        resp = self._client.get(
            f"{self.registry_url}/skills/{slug}",
            headers=self._headers(),
        )
        resp.raise_for_status()
        return self._parse_skill_info(resp.json())

    def get_version(self, slug: str, version: str = "latest") -> ClawHubVersionInfo:
        """Fetch version details and construct the download URL.

        Calls /api/v1/skills/{slug} to resolve the latest version number,
        then constructs the download URL using /api/v1/download?slug=&version=.
        """
        resp = self._client.get(
            f"{self.registry_url}/skills/{slug}",
            headers=self._headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        latest = data.get("latestVersion", {})
        resolved_version = latest.get("version") or version
        download_url = (
            f"{self.site_url}/api/v1/download?slug={slug}&version={resolved_version}"
        )
        return ClawHubVersionInfo(
            version=resolved_version,
            changelog=latest.get("changelog", ""),
            files=latest.get("files", []),
            download_url=download_url,
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
        resp = self._get_with_retry(version_info.download_url)

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

    def _get_with_retry(self, url: str, max_retries: int = 3) -> httpx.Response:
        """GET with exponential back-off on 429 Too Many Requests."""
        for attempt in range(max_retries):
            resp = self._client.get(url, follow_redirects=True)
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", 2 ** (attempt + 1)))
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        # Final attempt — let raise_for_status surface the 429
        resp = self._client.get(url, follow_redirects=True)
        resp.raise_for_status()
        return resp

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

    def _parse_search_result(self, data: dict) -> ClawHubSkillInfo:
        """Parse a flat search result item from /api/v1/search."""
        return ClawHubSkillInfo(
            slug=data.get("slug", ""),
            display_name=data.get("displayName", ""),
            summary=data.get("summary", ""),
            latest_version=data.get("version") or "",
            owner_handle="",
            tags={},
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

    def __exit__(self, *_):
        self.close()
