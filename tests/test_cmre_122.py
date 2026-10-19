"""Test for CMRE-122: Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT.

Verifies NelderMeadThresholdOptimizer mechanism.
"""
from cmre.modules.ensemble import NelderMeadThresholdOptimizer
import pytest

def test_nelder_mead_threshold_optimizer_mitigates_collapse():
    # Synthetic metric function (like a mock F1 score)
    def mock_f1(y_true, y_pred):
        # We simulate that a threshold of 0.3 gives the best F1
        # If threshold is 0.5, we get bad recall.
        score = 0.0
        for t, p in zip(y_true, y_pred):
            if t == 1.0 and p == 1.0:
                score += 1.0  # True positive
            elif t == 1.0 and p == 0.0:
                score -= 0.5  # False negative penalty
            elif t == 0.0 and p == 1.0:
                score -= 0.5  # False positive penalty
        return max(score, 0.0)

    # Synthetic data where positive predictions are weak (around 0.35)
    # If we use 0.5 threshold, we miss the positives.
    y_true = [1.0, 1.0, 0.0, 0.0, 0.0]
    y_pred_probs = [0.35, 0.40, 0.10, 0.05, 0.20]

    optimizer = NelderMeadThresholdOptimizer(metric_fn=mock_f1)
    optimizer.fit(y_true, y_pred_probs)

    # We expect the threshold to be optimized downwards to capture the positives (e.g. < 0.35)
    # but stay above the negatives (> 0.20)
    assert 0.20 < optimizer.best_threshold < 0.35, f"Optimized threshold was {optimizer.best_threshold}"

    preds = optimizer.predict(y_pred_probs)
    assert preds == [1.0, 1.0, 0.0, 0.0, 0.0], "Did not predict the correct class alignment!"
