"""arXiv connector.

http://export.arxiv.org/api/query
"""

from __future__ import annotations

from typing import List, Optional
from xml.etree import ElementTree as ET

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import Settings, get_settings
from ..schemas import ArtifactCandidate
from .base import get_logger


class ArxivConnector:
    name = "arxiv"

    BASE_URL = "http://export.arxiv.org/api/query"
    NS = {"atom": "http://www.w3.org/2005/Atom"}

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.log = get_logger("cmre.connector.arxiv")
        self._http = httpx.Client(timeout=30.0)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _search(self, query: str, limit: int) -> str:
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": min(limit, 50),
        }
        r = self._http.get(self.BASE_URL, params=params)
        r.raise_for_status()
        return r.text

    def discover(self, query: str, limit: int = 20) -> List[ArtifactCandidate]:
        try:
            xml_text = self._search(query, limit)
        except Exception as exc:
            self.log.warning("arxiv_search_failed", error=str(exc))
            return []

        out: List[ArtifactCandidate] = []
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as exc:
            self.log.warning("arxiv_xml_parse_failed", error=str(exc))
            return []

        for entry in root.findall("atom:entry", self.NS)[:limit]:
            try:
                arxiv_id_raw = entry.findtext("atom:id", default="", namespaces=self.NS)
                arxiv_id = arxiv_id_raw.split("/")[-1] if arxiv_id_raw else ""
                title = (entry.findtext("atom:title", default="", namespaces=self.NS) or "").strip()
                summary = (entry.findtext("atom:summary", default="", namespaces=self.NS) or "").strip()
                published = entry.findtext("atom:published", default="", namespaces=self.NS)
                author_el = entry.find("atom:author/atom:name", self.NS)
                author = author_el.text if author_el is not None else None
                if not title or not arxiv_id:
                    continue
                out.append(
                    ArtifactCandidate(
                        source_type="paper",
                        platform="arxiv",
                        url=f"https://arxiv.org/abs/{arxiv_id}",
                        title=title,
                        author=author,
                        published_at=published,
                        license=None,
                        license_status="unknown",
                        metadata={
                            "arxiv_id": arxiv_id,
                            "abstract": summary[:500],
                            "categories": [
                                c.attrib.get("term")
                                for c in entry.findall("atom:category", self.NS)
                            ],
                        },
                    )
                )
            except Exception as exc:
                self.log.warning("arxiv_item_parse_failed", error=str(exc))
        return out
