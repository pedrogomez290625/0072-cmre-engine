"""HuggingFace Papers connector.

Official successor to Papers with Code after Meta shut it down in July 2025.
https://huggingface.co/api/papers
"""

from __future__ import annotations

from typing import List, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import Settings, get_settings
from ..schemas import ArtifactCandidate
from .base import LicenseHeuristic, get_logger


class HuggingFaceConnector:
    name = "huggingface"

    BASE_URL = "https://huggingface.co/api/papers"

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.log = get_logger("cmre.connector.huggingface")
        self._http = httpx.Client(timeout=30.0)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _search(self, query: str, limit: int) -> list[dict]:
        params = {"query": query, "limit": min(limit, 50)}
        r = self._http.get(self.BASE_URL, params=params)
        r.raise_for_status()
        return r.json() if isinstance(r.json(), list) else []

    def discover(self, query: str, limit: int = 20) -> List[ArtifactCandidate]:
        try:
            items = self._search(query, limit)
        except Exception as exc:
            self.log.warning("hf_search_failed", error=str(exc))
            return []

        out: List[ArtifactCandidate] = []
        for item in items[:limit]:
            try:
                title = item.get("title") or ""
                arxiv_id = item.get("id") or ""
                url = f"https://huggingface.co/papers/{arxiv_id}" if arxiv_id else ""
                if not url:
                    continue
                license_text = item.get("license") or ""
                out.append(
                    ArtifactCandidate(
                        source_type="paper",
                        platform="huggingface",
                        url=url,
                        title=title,
                        author=None,
                        published_at=item.get("publishedAt"),
                        license=license_text or None,
                        license_status=LicenseHeuristic.classify(license_text) if license_text else "unknown",
                        metadata={
                            "arxiv_id": arxiv_id,
                            "upvotes": item.get("upvotes"),
                            "summary": item.get("summary", "")[:500],
                        },
                    )
                )
            except Exception as exc:
                self.log.warning("hf_item_parse_failed", error=str(exc))
        return out
