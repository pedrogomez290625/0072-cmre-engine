import pytest
import numpy as np
from cmre.modules.ood import OODDetector

def test_ood_detector_in_distribution():
    np.random.seed(42)
    # Train data: Standard normal
    X_train = np.random.randn(100, 3)

    detector = OODDetector(threshold=0.5)
    detector.fit(X_train)

    # Test data: Same distribution
    X_test = np.random.randn(50, 3)

    result = detector.compute_divergence(X_test)
    assert result["is_ood"] is False
    assert result["mean_divergence"] < 0.5

def test_ood_detector_out_of_distribution():
    np.random.seed(42)
    # Train data: Standard normal
    X_train = np.random.randn(100, 3)

    detector = OODDetector(threshold=0.5)
    detector.fit(X_train)

    # Test data: Shifted mean (OOD)
    X_test = np.random.randn(50, 3) + 2.0

    result = detector.compute_divergence(X_test)
    assert result["is_ood"] is True
    assert result["mean_divergence"] > 0.5
    assert len(result["feature_divergences"]) == 3
