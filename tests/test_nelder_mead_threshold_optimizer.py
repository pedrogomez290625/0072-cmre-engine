import pytest
from cmre.modules.ensemble import NelderMeadThresholdOptimizer

def dummy_f1_metric(y_true, y_pred):
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1.0 and yp == 1.0)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0.0 and yp == 1.0)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1.0 and yp == 0.0)
    if tp + fp + fn == 0:
        return 0.0
    return (2 * tp) / (2 * tp + fp + fn)

def test_nelder_mead_threshold_optimizer():
    y_true = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    # Prediction probabilities heavily skewed (common in extreme imbalance)
    y_pred_probs = [0.01, 0.02, 0.01, 0.03, 0.01, 0.08, 0.02, 0.01, 0.02, 0.01]

    # Static threshold of 0.5 collapses metric (F1 = 0.0)
    opt = NelderMeadThresholdOptimizer(metric_fn=dummy_f1_metric, init_threshold=0.5)

    # Fit should shift threshold to ~0.08 to capture the positive case
    opt.fit(y_true, y_pred_probs)

    # The optimal threshold should be <= 0.08 and > 0.03 to separate correctly
    assert 0.03 < opt.best_threshold <= 0.081

    preds = opt.predict(y_pred_probs)
    assert preds[5] == 1.0
    assert preds[3] == 0.0

    assert dummy_f1_metric(y_true, preds) == 1.0
