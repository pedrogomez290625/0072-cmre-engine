"""Tests that soft modality filter preserves cross-modal transfer."""

from cmre.models import Claim
from cmre.schemas import ProblemDNA
from cmre.services.scoring import compute_deterministic_score


def _dna(modality: str = "tabular", **kwargs) -> ProblemDNA:
    base = dict(
        title="Test",
        platform="kaggle",
        task_type="binary_classification",
        modality=modality,
        metric="roc_auc",
        metric_family="auc",
    )
    base.update(kwargs)
    return ProblemDNA(**base)


def test_cross_modal_mechanism_still_scores_high():
    """A mechanism claim from image that applies to tabular should NOT be filtered out."""
    c = Claim(
        statement="Use calibration (Platt/isotonic) for probability outputs.",
        claim_type="mechanism",
        mechanism_slug="metric_alignment",
        compatible_modalities=["image"],
        transferable_modalities=["tabular", "text", "time_series"],
        evidence_level=5,
        license_status="allowed",
        provenance_type="paper",
        validation_status="validated",
        approved=True,
    )
    bd = compute_deterministic_score(c, _dna(modality="tabular"))
    # Should score well — soft bonus, not exclusion
    assert bd.modality_bonus >= 0.7
    assert bd.deterministic_score > 0.4


def test_modality_filter_is_not_hard_exclusion():
    """A claim with modality_tags=['image'] should still score on a tabular DNA."""
    c = Claim(
        statement="Mixup/CutMix improves classification generalization.",
        claim_type="empirical_trick",
        mechanism_slug="augmentation_strategy",
        modality_tags=["image"],
        compatible_modalities=["image"],
        evidence_level=4,
        license_status="allowed",
        provenance_type="paper",
        validation_status="partially_validated",
        approved=True,
    )
    bd = compute_deterministic_score(c, _dna(modality="tabular"))
    # Should still rank above 0 (soft penalty only)
    assert bd.deterministic_score > 0.0
    assert bd.modality_bonus < 1.0  # penalized but not zero


def test_exact_modality_match_keeps_full_bonus():
    c = Claim(
        statement="Tabular baseline.",
        claim_type="empirical_trick",
        mechanism_slug="tree_baseline",
        compatible_modalities=["tabular"],
        evidence_level=5,
        license_status="allowed",
        provenance_type="paper",
        validation_status="validated",
        approved=True,
    )
    bd = compute_deterministic_score(c, _dna(modality="tabular"))
    assert bd.modality_bonus == 1.0
