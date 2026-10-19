"""Test for CMRE-121: Mitigación de UNCONSTRAINED_CANDIDATE_DECOY_OVERLOAD.

Verifies SIRIUSAbsenceAxiomOptimizer mechanism.
"""
from cmre.modules.ood import SIRIUSAbsenceAxiomOptimizer
import pytest

def test_sirius_absence_optimizer_mitigates_decoy_overload():
    optimizer = SIRIUSAbsenceAxiomOptimizer(absence_penalty_factor=0.2)

    candidates = [
        "C1=CC=CC=C1O",  # Phenol (has Oxygen)
        "C1=CC=CC=C1",   # Benzene (no Oxygen)
        "CCN",           # Ethylamine (no Oxygen)
    ]

    # Observe a neutral loss that requires Oxygen
    observed_losses = ["H2O"]

    penalties = optimizer.evaluate(candidates, observed_losses)

    assert pytest.approx(penalties[0], abs=1e-4) == 1.0, "Phenol shouldn't be penalized as it has Oxygen."
    assert pytest.approx(penalties[1], abs=1e-4) == 0.2, "Benzene should be penalized as it lacks Oxygen."
    assert pytest.approx(penalties[2], abs=1e-4) == 0.2, "Ethylamine should be penalized as it lacks Oxygen."
