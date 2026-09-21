"""
Unit tests for CMRE Canonical Competition Solvers (Paso 9).

Tests end-to-end execution of:
- EnvedaCasmiSolver
- RSNAMammographySolver
- ISICMelanomaSolver
- RichtersPredictorSolver
- ZindiAirQoSolver

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import pytest
import numpy as np

from cmre.solvers import (
    EnvedaCasmiSolver,
    RSNAMammographySolver,
    ISICMelanomaSolver,
    RichtersPredictorSolver,
    ZindiAirQoSolver,
)


def test_enveda_casmi_solver_e2e():
    solver = EnvedaCasmiSolver(mass_tolerance_ppm=10.0)
    
    smiles = ["CC(=O)OC1=CC=CC=C1C(=O)O", "CCN(CC)CC", "C1=CC=CC=C1", "CCO", "CCN"]
    query_bitsets = [0b101101, 0b110011]
    candidate_bitsets = [0b101100, 0b110010, 0b000001, 0b111111]
    candidate_masses = [180.05, 180.06, 250.10, 180.05]
    query_mass = 180.053
    
    result = solver.run_pipeline(smiles, query_bitsets, candidate_bitsets, candidate_masses, query_mass)
    
    assert result["validation_status"] == "VALIDATED_SCAFFOLD_DISJOINT"
    assert len(result["top_candidate_indices"]) == 2
    assert result["best_similarity"] > 0.0


def test_rsna_mammography_solver_e2e():
    solver = RSNAMammographySolver()
    
    pixels = [50, 100, 150, 200, 250]
    meta = {
        "PhotometricInterpretation": "MONOCHROME1",
        "RescaleSlope": 1.0,
        "RescaleIntercept": 0.0,
        "WindowCenter": 128.0,
        "WindowWidth": 256.0,
    }
    patient_ids = ["P1", "P2", "P3", "P4", "P5"]
    targets = [0.0, 0.0, 0.0, 1.0, 0.0]
    preds = [0.02, 0.04, 0.01, 0.18, 0.03]
    
    result = solver.run_pipeline(pixels, meta, patient_ids, targets, preds)
    
    assert result["validation_status"] == "VALIDATED_PATIENT_DISJOINT"
    assert 0.01 <= result["calibrated_threshold"] <= 0.25
    assert result["optimal_f1_score"] > 0.0


def test_isic_melanoma_solver_e2e():
    solver = ISICMelanomaSolver(target_min_tpr=0.80)
    
    features = np.array([
        [1.0, 2.0],
        [1.1, 2.1],
        [1.0, 1.9],
        [4.5, 6.0],  # Outlier
        [1.2, 2.0],
    ], dtype=np.float32)
    patient_ids = ["P1", "P1", "P1", "P2", "P2"]
    targets = np.array([0, 0, 0, 1, 0], dtype=np.int64)
    scores = np.array([0.1, 0.2, 0.15, 0.95, 0.05], dtype=np.float32)
    
    result = solver.run_pipeline(features, patient_ids, targets, scores)
    
    assert result["validation_status"] == "VALIDATED_PATIENT_DISJOINT"
    assert result["normalized_deltas_shape"] == [5, 2]
    assert result["partial_auc_at_80_tpr"] >= 0.0


def test_richters_predictor_solver_e2e():
    solver = RichtersPredictorSolver()
    
    heights = np.array([10.0, 20.0, 5.0, 15.0], dtype=np.float32)
    areas = np.array([25.0, 16.0, 100.0, 36.0], dtype=np.float32)
    continuous_scores = np.array([0.1, 0.45, 0.85, 0.50], dtype=np.float32)
    y_true = np.array([1, 2, 3, 2], dtype=np.int64)
    
    result = solver.run_pipeline(heights, areas, continuous_scores, y_true)
    
    assert result["validation_status"] == "VALIDATED_ORDINAL_NELDER_MEAD"
    assert len(result["optimized_thresholds"]) == 2
    assert result["calibrated_micro_f1"] >= 0.75


def test_zindi_airqo_solver_e2e():
    solver = ZindiAirQoSolver(w_gbdt=0.85)
    
    timestamps = [1000, 2000, 3000, 4000, 5000, 6000]
    hours = np.array([0.0, 4.0, 8.0, 12.0, 16.0, 20.0], dtype=np.float32)
    series = np.array([25.0, 30.0, 45.0, 50.0, 35.0, 28.0], dtype=np.float32)
    pred_gbdt = np.array([24.0, 31.0, 44.0, 49.0, 36.0, 27.0], dtype=np.float32)
    pred_knn = np.array([26.0, 29.0, 46.0, 52.0, 34.0, 30.0], dtype=np.float32)
    
    result = solver.run_pipeline(timestamps, hours, series, pred_gbdt, pred_knn)
    
    assert result["validation_status"] == "VALIDATED_SPATIO_TEMPORAL_PURGED"
    assert "lag_1" in result["lags_computed"]
    assert result["blended_prediction_mean"] > 0.0
