"""Tests for the problem profiler."""

from cmre.schemas import CompetitionInput
from cmre.services.problem_profiler import build_dna, modality_baselines, modality_validation


def _inp(**kwargs):
    base = dict(
        title="Test",
        platform="kaggle",
        task_type="binary_classification",
        modality="tabular",
        metric="roc_auc",
    )
    base.update(kwargs)
    return CompetitionInput(**base)


def test_build_dna_tabular_basic():
    dna = build_dna(_inp())
    assert dna.modality == "tabular"
    assert dna.metric_family == "auc"
    assert any("Adversarial" in s or "Stratified" in s for s in dna.validation_recommendations)


def test_build_dna_text_modality():
    dna = build_dna(_inp(modality="text", task_type="multiclass_classification", metric="f1_macro"))
    assert dna.modality == "text"
    assert dna.metric_family == "f1"
    assert dna.validation_recommendations  # text-specific validation


def test_build_dna_image_modality():
    dna = build_dna(_inp(modality="image", task_type="detection", metric="map", has_group_structure=True))
    assert dna.modality == "image"
    assert dna.metric_family == "map"
    assert dna.has_group_structure is True  # when input declares it
    assert any("identity-level" in s or "Domain-based" in s or "Stratified" in s for s in dna.validation_recommendations)


def test_build_dna_time_series_modality():
    dna = build_dna(
        _inp(
            modality="time_series",
            task_type="forecasting",
            metric="smape",
            has_temporal_component=True,
        )
    )
    assert dna.modality == "time_series"
    assert "temporal_dependency" in dna.risk_flags
    assert any("Rolling" in s or "walk-forward" in s for s in dna.validation_recommendations)


def test_build_dna_multimodal_modality():
    dna = build_dna(_inp(modality="multimodal", task_type="multiclass_classification", metric="ndcg"))
    assert dna.modality == "multimodal"
    assert dna.metric_family == "ndcg"


def test_build_dna_invalid_modality_falls_back_to_tabular():
    dna = build_dna(_inp(modality="unknown_thing"))
    assert dna.modality == "tabular"


def test_build_dna_temporal_component_flag():
    dna = build_dna(_inp(has_temporal_component=True))
    assert dna.has_temporal_component is True
    assert "temporal_dependency" in dna.risk_flags


def test_build_dna_class_imbalance_flag():
    dna = build_dna(_inp(class_imbalance="extreme"))
    assert "class_imbalance" in dna.risk_flags


def test_modality_baselines_returns_something_for_each():
    for mod in ("tabular", "text", "image", "time_series", "multimodal"):
        assert modality_baselines(mod), f"no baselines for {mod}"


def test_modality_validation_returns_something_for_each():
    for mod in ("tabular", "text", "image", "time_series", "multimodal"):
        assert modality_validation(mod), f"no validation for {mod}"


def test_dna_enrichment_with_llm_returns_valid_dna():
    from cmre.agents.base import MockLLMClient
    dna = build_dna(_inp(description="Some description"), llm=MockLLMClient())
    # Mock returns empty payload; we still get a valid DNA back
    assert dna.title == "Test"
    assert isinstance(dna.validation_recommendations, list)
