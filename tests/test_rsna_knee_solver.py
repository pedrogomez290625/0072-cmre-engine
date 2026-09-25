"""Unit tests for RSNA Knee 2026 Canonical Solver (Paso 9 / RSNA 2026 SOTA).

Tests multi-view MRI pipeline, Asymmetric Matrix Blending, Float64 safety guard,
and Macro ROC-AUC computation across 12 pathologies.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import pytest
import numpy as np

from cmre.solvers import RSNAKneeSolver


def test_rsna_knee_solver_e2e():
    solver = RSNAKneeSolver()
    
    n_samples = 20
    n_classes = 12
    n_models = 3

    # Generate synthetic binary ground truth
    rng = np.random.RandomState(42)
    y_true = rng.binomial(1, 0.25, size=(n_samples, n_classes)).astype(np.float32)
    # Ensure at least 1 positive and 1 negative per class
    for c in range(n_classes):
        if np.sum(y_true[:, c] == 1) == 0:
            y_true[0, c] = 1.0
        if np.sum(y_true[:, c] == 0) == 0:
            y_true[1, c] = 0.0

    # Model 0: Specialist (high precision on meniscus [idx 2, 3] and fracture [idx 11])
    p0 = np.clip(y_true * 0.8 + rng.uniform(0.01, 0.2, size=(n_samples, n_classes)), 0.01, 0.99)
    # Model 1: CoAtNet (high precision on ligaments [idx 0, 1] and effusion [idx 7])
    p1 = np.clip(y_true * 0.75 + rng.uniform(0.01, 0.25, size=(n_samples, n_classes)), 0.01, 0.99)
    # Model 2: Raptor (high precision on OA [idx 4, 5, 6])
    p2 = np.clip(y_true * 0.70 + rng.uniform(0.01, 0.3, size=(n_samples, n_classes)), 0.01, 0.99)

    # Ingest views
    study_views = {
        "sagittal": rng.randn(n_samples, 32, 32),
        "coronal": rng.randn(n_samples, 32, 32),
        "axial": rng.randn(n_samples, 32, 32),
    }

    result = solver.run_pipeline(
        study_views_dict=study_views,
        models_preds_list=[p0, p1, p2],
        y_true=y_true,
    )

    assert result["validation_status"] == "VALIDATED_RSNA_KNEE_SOTA"
    assert result["n_classes"] == 12
    assert result["n_samples"] == n_samples
    assert result["macro_roc_auc"] >= 0.75
    assert len(result["auc_breakdown"]) == 12
    assert len(result["weights_matrix"]) == 12
    # Check that weights sum to approximately 1.0 per class
    for row in result["weights_matrix"]:
        assert pytest.approx(sum(row), abs=1e-2) == 1.0
    assert result["latency_per_study_sec"] < 1.0


def test_rsna_knee_solver_fp16_guard():
    solver = RSNAKneeSolver(enable_fp16_guard=True)
    # Test with double precision (float64) inputs to verify auto-sanitization (FAIL_13)
    double_array = np.array([[0.5, 0.2]], dtype=np.float64)
    sanitized = solver.sanitize_tensor_dtypes(double_array)
    assert sanitized.dtype == np.float32
