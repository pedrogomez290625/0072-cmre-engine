"""Connector base classes and license heuristic."""

from __future__ import annotations

from typing import List, Optional, Protocol

import structlog

from ..schemas import ArtifactCandidate


class Connector(Protocol):
    name: str

    def discover(self, query: str, limit: int = 20) -> List[ArtifactCandidate]: ...


# Conservative allowlist. Any unknown license is treated as unknown.
_PERMISSIVE_LICENSES = {
    "mit",
    "apache-2.0",
    "apache 2.0",
    "bsd-2-clause",
    "bsd-3-clause",
    "isc",
    "cc-by-4.0",
    "cc-by-3.0",
    "cc0-1.0",
    "public domain",
    "unlicense",
    "wtfpl",
    "lgpl-2.1",
    "lgpl-3.0",
    "mpl-2.0",
    "kaggle-rule",  # Kaggle's default for public notebooks
}

_RESTRICTED_LICENSES = {
    "gpl-3.0",
    "gpl-2.0",
    "agpl-3.0",
    "cc-by-nc",
    "cc-by-nc-sa",
    "cc-by-nc-nd",
    "cc-by-sa-nc",
    "non-commercial",
    "research-only",
    "academic-use-only",
}

_FORBIDDEN_PATTERNS = (
    "proprietary",
    "all rights reserved",
    "no redistribution",
    "confidential",
    "internal use only",
    "paid",
)


class LicenseHeuristic:
    """Conservative license classifier.

    Be safe by default: when in doubt, return "unknown".
    """

    @staticmethod
    def classify(license_text: Optional[str]) -> str:
        if not license_text:
            return "unknown"
        norm = license_text.strip().lower()
        if not norm:
            return "unknown"
        if any(p in norm for p in _FORBIDDEN_PATTERNS):
            return "forbidden"
        if norm in _PERMISSIVE_LICENSES:
            return "allowed"
        if norm in _RESTRICTED_LICENSES:
            return "restricted"
        # Substring matches for permissive
        for ok in _PERMISSIVE_LICENSES:
            if ok in norm:
                return "allowed"
        for bad in _RESTRICTED_LICENSES:
            if bad in norm:
                return "restricted"
        return "unknown"


def get_logger(name: str):
    return structlog.get_logger(name)
