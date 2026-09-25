"""Unit tests for ClassWiseAsymmetricBlender and LatencyBudgetPruner (MOD_ENSEMBLE).

Tests multi-target simplex matrix fitting, clinical prior blending, and greedy latency pruning.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import pytest
import numpy as np

from cmre.modules.ensemble import ClassWiseAsymmetricBlender, LatencyBudgetPruner


def test_classwise_asymmetric_blender_fit_predict():
    blender = ClassWiseAsymmetricBlender(max_iter=500)

    # 3 models, 20 samples, 2 classes
    n_samples = 20
    k_classes = 2
    
    # Model 0 is expert at class 0, poor at class 1
    # Model 1 is expert at class 1, poor at class 0
    # Model 2 is average
    rng = np.random.RandomState(42)
    y_true = rng.binomial(1, 0.4, size=(n_samples, k_classes)).astype(float).tolist()

    m0 = [[y_true[i][0] * 0.9 + 0.05, 0.5] for i in range(n_samples)]
    m1 = [[0.5, y_true[i][1] * 0.9 + 0.05] for i in range(n_samples)]
    m2 = [[0.5, 0.5] for i in range(n_samples)]

    models_preds = [m0, m1, m2]

    blender.fit(models_preds, y_true)

    assert len(blender.weights_matrix) == k_classes
    # Weights for class 0: Model 0 should have higher weight than Model 1
    w_c0 = blender.weights_matrix[0]
    assert w_c0[0] > w_c0[1]

    # Weights for class 1: Model 1 should have higher weight than Model 0
    w_c1 = blender.weights_matrix[1]
    assert w_c1[1] > w_c1[0]

    preds = blender.predict(models_preds)
    assert len(preds) == n_samples
    assert len(preds[0]) == k_classes


def test_latency_budget_pruner():
    pruner = LatencyBudgetPruner(max_latency_seconds=2.0)

    candidate_models = ["ModelA", "ModelB", "ModelC", "ModelD"]
    latencies = {
        "ModelA": 0.5,
        "ModelB": 1.2,
        "ModelC": 1.8,
        "ModelD": 0.4,
    }
    scores = {
        "ModelA": 0.90,
        "ModelB": 0.92,
        "ModelC": 0.93,
        "ModelD": 0.85,
    }

    selected, tot_lat, tot_score = pruner.prune(candidate_models, latencies, scores)

    assert tot_lat <= 2.0
    assert len(selected) >= 1
    # ModelA (0.90/0.5 = 1.8) and ModelD (0.85/0.4 = 2.125) have high efficiency ratios
    assert "ModelD" in selected
