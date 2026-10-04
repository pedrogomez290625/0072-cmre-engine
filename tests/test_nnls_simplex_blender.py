import pytest
from cmre.modules.ensemble import NonNegativeLeastSquaresBlender

def test_nnls_simplex_blender():
    # Ground truth
    y_true = [1.0, 0.0, 1.0, 0.0, 1.0]

    # Model 1 is perfect
    preds1 = [1.0, 0.0, 1.0, 0.0, 1.0]

    # Model 2 is inverse
    preds2 = [0.0, 1.0, 0.0, 1.0, 0.0]

    # Model 3 is random
    preds3 = [0.5, 0.5, 0.5, 0.5, 0.5]

    blender = NonNegativeLeastSquaresBlender()
    blender.fit([preds1, preds2, preds3], y_true)

    weights = blender.weights
    assert len(weights) == 3

    # Check simplex constraints
    assert all(w >= -1e-6 for w in weights)
    assert abs(sum(weights) - 1.0) < 1e-6

    # Model 1 should have weight very close to 1.0
    assert weights[0] > 0.99

    # Predict
    preds = blender.predict([preds1, preds2, preds3])
    assert len(preds) == 5
    assert abs(preds[0] - 1.0) < 1e-4
