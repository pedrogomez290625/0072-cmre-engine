"""
Unit tests for CMRE Decision Matrix & Deterministic Dispatch Engine (Paso 8).

Tests:
- Rule loading and schema validation
- Dispatch for Medical Mammography (RSNA)
- Dispatch for Cheminformatics MS/MS (Enveda CASMI 2026)
- Dispatch for Financial Microstructure (Optiver)
- Dispatch for Ordinal Tabular Damage (DrivenData Richter's Predictor)
- Dispatch for IoT Spatio-Temporal Telemetry (Zindi AirQo)
- Wall of Shame forbidden approaches enforcement

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import pytest

from cmre.services.decision_matrix import DecisionMatrixEngine, DispatchedPipelineResult
from cmre.schemas import CompetitionInput


def test_decision_matrix_loading():
    engine = DecisionMatrixEngine()
    assert len(engine.rules) >= 5
    rule_ids = [r["rule_id"] for r in engine.rules]
    assert "RULE_MED_MAMMO_EXTREME_IMBALANCE" in rule_ids
    assert "RULE_CHEM_MOLECULAR_SCAFFOLD" in rule_ids


def test_dispatch_rsna_mammography():
    engine = DecisionMatrixEngine()
    comp = {
        "title": "RSNA Screening Mammography Breast Cancer Detection",
        "modality": "image",
        "has_group_structure": True,
        "class_imbalance": "high",
        "metric": "pf1",
    }
    result = engine.dispatch(comp)
    assert result.matched_rule_id == "RULE_MED_MAMMO_EXTREME_IMBALANCE"
    assert result.confidence_score >= 0.95
    assert "ingest" in result.prescribed_pipeline
    assert "SNIP_INGEST_DICOM_FAST" in result.prescribed_pipeline["ingest"]
    assert "SNIP_MED_CROSS_VIEW_MAMMO_ATTENTION" in result.prescribed_pipeline["signal"]
    assert any("FAIL_01" in f for f in result.forbidden_approaches)


def test_dispatch_enveda_casmi_molecular():
    engine = DecisionMatrixEngine()
    comp = {
        "title": "Enveda CASMI 2026 Blind Molecular Identification Challenge",
        "modality": "tabular",
        "has_group_structure": True,
        "leak_signals": ["molecular_scaffold_leakage", "smiles_memorization"],
        "metric": "top_k_accuracy",
    }
    result = engine.dispatch(comp)
    assert result.matched_rule_id == "RULE_CHEM_MOLECULAR_SCAFFOLD"
    assert "SNIP_SPLIT_SCAFFOLD_MURCKO" in result.prescribed_pipeline["split"]
    assert "SNIP_HPC_BITSET_TANIMOTO_FAST" in result.prescribed_pipeline["signal"]
    assert any("FAIL_04" in f for f in result.forbidden_approaches)


def test_dispatch_optiver_financial_orderbook():
    engine = DecisionMatrixEngine()
    comp = {
        "title": "Optiver - Trading at the Close",
        "modality": "time_series",
        "has_temporal_component": True,
        "metric": "mae",
    }
    result = engine.dispatch(comp)
    assert result.matched_rule_id == "RULE_FIN_TIMESERIES_ORDERBOOK"
    assert "SNIP_SPLIT_PURGED_EMBARGO_TIME" in result.prescribed_pipeline["split"]
    assert any("FAIL_02" in f for f in result.forbidden_approaches)


def test_dispatch_richters_predictor_ordinal():
    engine = DecisionMatrixEngine()
    comp = {
        "title": "Richter's Predictor: Modeling Earthquake Damage",
        "modality": "tabular",
        "task_type": "ordinal_classification",
        "metric": "f1_micro",
    }
    result = engine.dispatch(comp)
    assert result.matched_rule_id == "RULE_TAB_ORDINAL_DAMAGE"
    assert "SNIP_ALT_DRIVENDATA_ORDINAL_DAMAGE_MODELER" in result.prescribed_pipeline["signal"]


def test_dispatch_zindi_airqo():
    engine = DecisionMatrixEngine()
    comp = {
        "title": "AirQo Ugandan Air Quality Forecast Challenge",
        "modality": "time_series",
        "has_temporal_component": True,
        "has_group_structure": True,
        "metric": "rmse",
    }
    result = engine.dispatch(comp)
    assert result.matched_rule_id == "RULE_ENV_SPATIO_TEMPORAL_IOT"
    assert "SNIP_ALT_ZINDI_SPATIO_TEMPORAL_LAG_BLENDER" in result.prescribed_pipeline["signal"]
