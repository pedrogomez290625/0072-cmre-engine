"""GitHub repository search connector.

Useful for finding competition-winning repos and clean implementations.
https://api.github.com/search/repositories
"""

from __future__ import annotations

from typing import List, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import Settings, get_settings
from ..schemas import ArtifactCandidate
from .base import LicenseHeuristic, get_logger


class GitHubConnector:
    name = "github"

    BASE_URL = "https://api.github.com/search/repositories"

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.log = get_logger("cmre.connector.github")
        self._http = httpx.Client(timeout=30.0)
        self._headers = {"Accept": "application/vnd.github+json"}
        if settings and settings.github_token:
            self._headers["Authorization"] = f"Bearer {settings.github_token}"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _search(self, query: str, limit: int) -> dict:
        params = {
            "q": f"{query} language:Python stars:>10",
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, 50),
        }
        r = self._http.get(self.BASE_URL, params=params, headers=self._headers)
        r.raise_for_status()
        return r.json()

    def discover(self, query: str, limit: int = 20) -> List[ArtifactCandidate]:
        try:
            payload = self._search(query, limit)
        except Exception as exc:
            self.log.warning("github_search_failed", error=str(exc))
            return []

        out: List[ArtifactCandidate] = []
        for item in (payload.get("items") or [])[:limit]:
            try:
                license_info = item.get("license") or {}
                spdx = license_info.get("spdx_id") if isinstance(license_info, dict) else None
                license_text = spdx or "unknown"
                out.append(
                    ArtifactCandidate(
                        source_type="repo",
                        platform="github",
                        url=item.get("html_url", ""),
                        title=item.get("full_name"),
                        author=item.get("owner", {}).get("login"),
                        published_at=item.get("created_at"),
                        license=spdx,
                        license_status=LicenseHeuristic.classify(spdx),
                        metadata={
                            "description": item.get("description", "")[:300],
                            "stars": item.get("stargazers_count"),
                            "language": item.get("language"),
                            "topics": item.get("topics", []),
                            "pushed_at": item.get("pushed_at"),
                        },
                    )
                )
            except Exception as exc:
                self.log.warning("github_item_parse_failed", error=str(exc))
        return out
