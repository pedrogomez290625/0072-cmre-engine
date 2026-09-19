"""Tests for the reasoner (v0.3.0: deterministic base + soft modality)."""

from datetime import datetime, timezone, timedelta
from cmre.models import Claim
from cmre.schemas import ProblemDNA
from cmre.services.reasoner import _passes_hard_filters, rank_claims


def _dna(**kwargs) -> ProblemDNA:
    base = dict(
        title="Test",
        platform="kaggle",
        task_type="binary_classification",
        modality="tabular",
        metric="roc_auc",
        metric_family="auc",
    )
    base.update(kwargs)
    return ProblemDNA(**base)


def _claim(**kwargs) -> Claim:
    base = dict(
        statement="Test",
        evidence_level=4,
        license_status="allowed",
        approved=True,
    )
    base.update(kwargs)
    return Claim(**base)


def test_hard_filter_drops_forbidden_license():
    c = _claim(license_status="forbidden")
    assert _passes_hard_filters(c, allow_unknown_license=False) is False


def test_hard_filter_drops_unknown_license_by_default():
    c = _claim(license_status="unknown")
    assert _passes_hard_filters(c, allow_unknown_license=False) is False
    assert _passes_hard_filters(c, allow_unknown_license=True) is True


def test_hard_filter_drops_unapproved():
    c = _claim(approved=False)
    assert _passes_hard_filters(c, allow_unknown_license=False) is False


def test_hard_filter_allows_approved_allowed():
    c = _claim(license_status="allowed", approved=True)
    assert _passes_hard_filters(c, allow_unknown_license=False) is True


def test_rank_claims_is_pure_function():
    """rank_claims should not touch the DB."""
    claims = [
        _claim(mechanism_slug="tree_baseline", compatible_modalities=["tabular"]),
        _claim(mechanism_slug="temporal_validation", compatible_modalities=["tabular"]),
        _claim(mechanism_slug="augmentation_strategy", compatible_modalities=["image"]),
    ]
    dna = _dna(modality="tabular", has_temporal_component=True)
    ranked = rank_claims(claims, dna)
    assert len(ranked) == 3
    # All have a score
    assert all(r.score >= 0 for r in ranked)


def test_rank_claims_sorts_by_score():
    claims = [
        _claim(mechanism_slug="tree_baseline", evidence_level=2, compatible_modalities=["tabular"]),
        _claim(mechanism_slug="tree_baseline", evidence_level=6, compatible_modalities=["tabular"]),
    ]
    dna = _dna(modality="tabular")
    ranked = rank_claims(claims, dna)
    # Higher evidence should rank higher
    assert ranked[0].score >= ranked[1].score
