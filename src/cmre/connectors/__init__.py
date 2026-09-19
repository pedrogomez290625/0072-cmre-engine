"""Ingestion connectors.

Each connector is a swappable module that returns standardized
ArtifactCandidate objects. Connectors never write to the DB directly —
the orchestrator does that via cmre.services.knowledge_base.
"""

from .arxiv import ArxivConnector
from .base import Connector, LicenseHeuristic
from .github import GitHubConnector
from .huggingface import HuggingFaceConnector
from .semantic_scholar import SemanticScholarConnector

__all__ = [
    "Connector",
    "LicenseHeuristic",
    "HuggingFaceConnector",
    "SemanticScholarConnector",
    "ArxivConnector",
    "GitHubConnector",
    "get_connectors",
]


def get_connectors(settings=None):
    """Return enabled connectors based on settings."""
    from ..config import get_settings

    s = settings or get_settings()
    out = []
    if s.connector_huggingface_enabled:
        try:
            out.append(HuggingFaceConnector(s))
        except Exception:  # noqa: BLE001
            pass
    if s.connector_semantic_scholar_enabled:
        try:
            out.append(SemanticScholarConnector(s))
        except Exception:  # noqa: BLE001
            pass
    if s.connector_arxiv_enabled:
        try:
            out.append(ArxivConnector(s))
        except Exception:  # noqa: BLE001
            pass
    if s.connector_github_enabled:
        try:
            out.append(GitHubConnector(s))
        except Exception:  # noqa: BLE001
            pass
    return out
