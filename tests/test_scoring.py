"""Tests for deterministic scoring with breakdown."""

from datetime import datetime, timezone

from cmre.models import Claim
from cmre.schemas import ProblemDNA
from cmre.services.scoring import (
    LICENSE_MULTIPLIER,
    PROVENANCE_MULTIPLIER,
    apply_llm_delta,
    compute_deterministic_score,
)


def _claim(**kwargs) -> Claim:
    base = dict(
        statement="Test claim",
        claim_type="mechanism",
        evidence_level=4,
        license_status="allowed",
        provenance_type="paper",
        validation_status="validated",
        mechanism_slug="temporal_validation",
        compatible_modalities=["tabular"],
        transferable_modalities=[],
        hard_exclude_modalities=[],
        approved=True,
    )
    base.update(kwargs)
    return Claim(**base)


def _dna(**kwargs) -> ProblemDNA:
    base = dict(
        title="Test",
        platform="kaggle",
        task_type="binary_classification",
        modality="tabular",
        metric="roc_auc",
        metric_family="auc",
        has_temporal_component=True,
        class_imbalance="high",
    )
    base.update(kwargs)
    return ProblemDNA(**base)


def test_breakdown_is_returned():
    bd = compute_deterministic_score(_claim(), _dna())
    assert bd.mechanism_fit >= 0
    assert bd.deterministic_score >= 0
    assert bd.final_score == bd.deterministic_score  # no LLM delta applied


def test_mechanism_fit_high_for_matching_mechanism():
    bd = compute_deterministic_score(
        _claim(mechanism_slug="temporal_validation"),
        _dna(has_temporal_component=True),
    )
    # Partial-word match: "temporal" hits the DNA hint. Full slug is in
    # DNA's risk_flags/validation_recommendations when the profiler ran,
    # but here we build the DNA directly, so we accept ≥0.7.
    assert bd.mechanism_fit >= 0.7


def test_mechanism_fit_low_for_unrelated_mechanism():
    bd = compute_deterministic_score(
        _claim(mechanism_slug="graph_spectral_decomposition"),
        _dna(),
    )
    assert bd.mechanism_fit < 0.7


def test_constraint_compatibility_penalizes_not_recommended_match():
    c = _claim(not_recommended_when=["has_temporal_component"])
    bd = compute_deterministic_score(c, _dna(has_temporal_component=True))
    # Should be penalized
    assert bd.constraint_compatibility < 1.0


def test_modality_soft_bonus_full_for_matching_compatible():
    c = _claim(compatible_modalities=["tabular"], claim_type="mechanism")
    bd = compute_deterministic_score(c, _dna(modality="tabular"))
    assert bd.modality_bonus == 1.0


def test_modality_soft_bonus_transferable_is_partial_not_exclusion():
    c = _claim(compatible_modalities=["image"], transferable_modalities=["text"], claim_type="mechanism")
    bd = compute_deterministic_score(c, _dna(modality="text"))
    # Soft bonus, NOT exclusion
    assert 0.7 <= bd.modality_bonus <= 0.9


def test_modality_hard_exclude_is_zero():
    c = _claim(hard_exclude_modalities=["text"], claim_type="mechanism")
    bd = compute_deterministic_score(c, _dna(modality="text"))
    assert bd.modality_bonus == 0.0


def test_provenance_multiplier_higher_for_internal_experiment():
    assert PROVENANCE_MULTIPLIER["internal_experiment"] > PROVENANCE_MULTIPLIER["paper"]
    assert PROVENANCE_MULTIPLIER["paper"] > PROVENANCE_MULTIPLIER["curated_hypothesis"]


def test_license_multiplier_forbidden_is_zero():
    assert LICENSE_MULTIPLIER["forbidden"] == 0.0


def test_contradicted_validation_status_reduces_evidence():
    c_valid = _claim(validation_status="validated")
    c_contradicted = _claim(validation_status="contradicted")
    bd_v = compute_deterministic_score(c_valid, _dna())
    bd_c = compute_deterministic_score(c_contradicted, _dna())
    assert bd_v.evidence_quality > bd_c.evidence_quality


def test_deterministic_is_pure_function():
    """Same inputs → same output, no DB, no I/O."""
    c = _claim()
    d = _dna()
    bd1 = compute_deterministic_score(c, d)
    bd2 = compute_deterministic_score(c, d)
    assert bd1.deterministic_score == bd2.deterministic_score


def test_llm_delta_bounded_to_max_0_10():
    c = _claim()
    d = _dna()
    bd = compute_deterministic_score(c, d)

    # Even with extreme LLM score (100 = very positive), delta capped at +0.10
    bd_high = apply_llm_delta(bd, llm_score_0_100=100)
    assert bd_high.llm_rerank_delta <= 0.10

    # Even with extreme negative (0 = very negative), delta floored at -0.10
    bd_low = apply_llm_delta(bd, llm_score_0_100=0)
    assert bd_low.llm_rerank_delta >= -0.10


def test_llm_delta_neutral_score_keeps_deterministic():
    bd = compute_deterministic_score(_claim(), _dna())
    bd_neutral = apply_llm_delta(bd, llm_score_0_100=50)
    assert abs(bd_neutral.llm_rerank_delta) < 0.01
    assert bd_neutral.final_score == bd.deterministic_score


def test_curated_hypothesis_warning_present():
    c = _claim(provenance_type="curated_hypothesis")
    bd = compute_deterministic_score(c, _dna())
    assert any("curated hypothesis" in w.lower() for w in bd.warnings)
