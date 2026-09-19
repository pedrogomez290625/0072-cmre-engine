"""Semantic Scholar connector.

https://api.semanticscholar.org/graph/v1/paper/search
"""

from __future__ import annotations

from typing import List, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import Settings, get_settings
from ..schemas import ArtifactCandidate
from .base import LicenseHeuristic, get_logger


class SemanticScholarConnector:
    name = "semantic_scholar"

    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.log = get_logger("cmre.connector.semantic_scholar")
        self._http = httpx.Client(timeout=30.0)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _search(self, query: str, limit: int) -> dict:
        params = {
            "query": query,
            "limit": min(limit, 100),
            "fields": "title,authors,year,abstract,citationCount,externalIds,openAccessPdf,publicationDate",
        }
        r = self._http.get(self.BASE_URL, params=params)
        r.raise_for_status()
        return r.json()

    def discover(self, query: str, limit: int = 20) -> List[ArtifactCandidate]:
        try:
            payload = self._search(query, limit)
        except Exception as exc:
            self.log.warning("s2_search_failed", error=str(exc))
            return []

        out: List[ArtifactCandidate] = []
        for item in (payload.get("data") or [])[:limit]:
            try:
                title = item.get("title") or ""
                paper_id = item.get("paperId") or ""
                if not title or not paper_id:
                    continue
                url = f"https://www.semanticscholar.org/paper/{paper_id}"
                authors = item.get("authors") or []
                author = authors[0]["name"] if authors else None
                ext = item.get("externalIds") or {}
                license_text = "unknown"
                pdf = item.get("openAccessPdf") or {}
                pdf_url = pdf.get("url") if isinstance(pdf, dict) else None
                out.append(
                    ArtifactCandidate(
                        source_type="paper",
                        platform="semantic_scholar",
                        url=url,
                        title=title,
                        author=author,
                        published_at=item.get("publicationDate"),
                        license=None,
                        license_status="unknown",
                        metadata={
                            "arxiv_id": ext.get("ArXiv"),
                            "doi": ext.get("DOI"),
                            "year": item.get("year"),
                            "citations": item.get("citationCount"),
                            "abstract": (item.get("abstract") or "")[:500],
                            "open_access_pdf": pdf_url,
                        },
                    )
                )
            except Exception as exc:
                self.log.warning("s2_item_parse_failed", error=str(exc))
        return out
