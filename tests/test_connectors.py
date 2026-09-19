"""Smoke tests for connectors.

Focus on LicenseHeuristic (deterministic) + connector factory behavior.
Network calls are NOT tested here — those should be integration tests.
"""

from cmre.connectors.base import LicenseHeuristic
from cmre.connectors import get_connectors


def test_license_heuristic_permissive():
    assert LicenseHeuristic.classify("MIT") == "allowed"
    assert LicenseHeuristic.classify("Apache-2.0") == "allowed"
    assert LicenseHeuristic.classify("BSD-3-Clause") == "allowed"
    assert LicenseHeuristic.classify("CC-BY-4.0") == "allowed"
    assert LicenseHeuristic.classify("CC0-1.0") == "allowed"
    assert LicenseHeuristic.classify("CC-BY-3.0") == "allowed"
    assert LicenseHeuristic.classify("Kaggle-rule") == "allowed"


def test_license_heuristic_restricted():
    assert LicenseHeuristic.classify("GPL-3.0") == "restricted"
    assert LicenseHeuristic.classify("CC-BY-NC") == "restricted"
    assert LicenseHeuristic.classify("CC-BY-NC-SA") == "restricted"
    assert LicenseHeuristic.classify("non-commercial") == "restricted"


def test_license_heuristic_forbidden():
    assert LicenseHeuristic.classify("Proprietary - all rights reserved") == "forbidden"
    assert LicenseHeuristic.classify("internal use only") == "forbidden"
    assert LicenseHeuristic.classify("confidential") == "forbidden"


def test_license_heuristic_unknown():
    assert LicenseHeuristic.classify("") == "unknown"
    assert LicenseHeuristic.classify(None) == "unknown"
    assert LicenseHeuristic.classify("Made-up License") == "unknown"


def test_connector_factory_respects_disabled_flags(monkeypatch):
    from cmre.config import get_settings

    s = get_settings()
    monkeypatch.setattr(s, "connector_huggingface_enabled", False)
    monkeypatch.setattr(s, "connector_arxiv_enabled", False)
    monkeypatch.setattr(s, "connector_github_enabled", False)
    monkeypatch.setattr(s, "connector_semantic_scholar_enabled", True)
    out = get_connectors(s)
    names = {c.name for c in out}
    assert "huggingface" not in names
    assert "arxiv" not in names
    assert "github" not in names
    assert "semantic_scholar" in names
