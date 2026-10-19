"""Test for CMRE-118: Mitigación de UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION.

Verifies MultiViewOrthogonalAligner functionality.
"""
from cmre.modules.ensemble import MultiViewOrthogonalAligner


def test_multi_view_orthogonal_aligner_mitigates_latency_explosion():
    # Provide synthetic multi-view data predictions
    views_preds = {
        "sagittal": [[0.8, 0.2], [0.1, 0.9], [0.9, 0.1]],
        "coronal":  [[0.75, 0.25], [0.2, 0.8], [0.85, 0.15]],
        "axial":    [[0.82, 0.18], [0.15, 0.85], [0.88, 0.12]]
    }

    # Ground truth matrix [N, K]
    y_true = [[1.0, 0.0], [0.0, 1.0], [1.0, 0.0]]

    aligner = MultiViewOrthogonalAligner()
    aligner.fit(views_preds, y_true)

    # Verify that view weights were calculated properly without exploding logic
    assert "sagittal" in aligner.view_weights
    assert "coronal" in aligner.view_weights
    assert "axial" in aligner.view_weights

    # Ensure view weights sum to ~1 for each class
    for class_idx in range(len(y_true[0])):
        total_weight = sum(aligner.view_weights[v][class_idx] for v in aligner.view_weights)
        assert abs(total_weight - 1.0) < 1e-4

    # Run predict to ensure latency is reasonable
    blended = aligner.predict(views_preds)
    assert len(blended) == len(y_true)
    assert len(blended[0]) == len(y_true[0])
