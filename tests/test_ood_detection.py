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

def test_sirius_absence_axiom_optimizer():
    from cmre.modules.ood import SIRIUSAbsenceAxiomOptimizer
    import numpy as np

    optimizer = SIRIUSAbsenceAxiomOptimizer(absence_penalty_factor=0.35)

    candidates = [
        "CC(=O)OC1=CC=CC=C1C(=O)O", # Aspirin (Has C, O)
        "c1ccccc1",                 # Benzene (No O)
        "C1=CC=CC=C1N",             # Aniline (No O, has N)
    ]

    # Observe H2O (requires O)
    penalties = optimizer.evaluate(candidates, ["H2O"])
    assert penalties[0] == 1.0 # Aspirin has O
    assert penalties[1] == 0.35 # Benzene lacks O
    assert penalties[2] == 0.35 # Aniline lacks O

    # Observe NH3 (requires N)
    penalties_nh3 = optimizer.evaluate(candidates, ["NH3"])
    assert penalties_nh3[0] == 0.35 # Aspirin lacks N
    assert penalties_nh3[1] == 0.35 # Benzene lacks N
    assert penalties_nh3[2] == 1.0  # Aniline has N
