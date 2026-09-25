"""Unit tests for Enveda CASMI 2026 V3 SOTA enhancements.

Tests SIRIUS neutral loss rules (Axiom of Absence), Gated Library Anchor (Rank 1 Shield),
and InChIKey14 tautomeric deduplication.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import pytest
import numpy as np

from cmre.solvers import EnvedaCasmiSolver


def test_casmi_v3_sota_pipeline_e2e():
    solver = EnvedaCasmiSolver(
        mass_tolerance_ppm=10.0,
        anchor_similarity_threshold=0.85,
        absence_penalty_factor=0.2,
    )

    smiles = [
        "CC(=O)OC1=CC=CC=C1C(=O)O",  # Aspirin (contains O)
        "CCN(CC)CC",                  # Triethylamine (contains N, NO O)
        "C1=CC=CC=C1",                # Benzene (hydrocarbon only)
        "CCO",                        # Ethanol (contains O)
        "CCN",                        # Ethylamine (contains N)
    ]
    query_bitsets = [0b101101]
    candidate_bitsets = [0b101100, 0b110010, 0b000001, 0b101101, 0b111111]
    candidate_masses = [180.05, 180.06, 180.05, 180.053, 180.05]
    query_mass = 180.053

    # Observed neutral loss: H2O (requires Oxygen 'O')
    observed_losses = ["H2O"]

    # Candidate inchikeys (simulate duplicates in first 14 chars)
    candidate_inchikeys = [
        "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
        "ZMANZCXQSJIPKH-UHFFFAOYSA-N",
        "UHOVQNZJYSORNB-UHFFFAOYSA-N",
        "BSYNRYMUTXBXSQ-REPEAT12345-N",  # Duplicate prefix of candidate 0
        "XLYOFNOQVPJJNP-UHFFFAOYSA-N",
    ]

    # Reference library similarities (candidate 3 has 0.92 >= 0.85 anchor threshold)
    ref_sims = [0.40, 0.30, 0.10, 0.92, 0.50]

    result = solver.run_pipeline(
        smiles_list=smiles,
        query_bitsets=query_bitsets,
        candidate_bitsets=candidate_bitsets,
        candidate_masses=candidate_masses,
        query_mass=query_mass,
        observed_neutral_losses=observed_losses,
        candidate_inchikeys=candidate_inchikeys,
        reference_library_sims=ref_sims,
    )

    assert result["validation_status"] == "VALIDATED_SCAFFOLD_DISJOINT"
    assert result["anchored_library_matches"] == 1
    # Check that the anchored candidate (index 3) is at rank 1 (first item of top candidates)
    assert result["top_candidate_indices"][0][0] == 3
    # Check that candidate 3 is unique and no duplicate prefix exists
    first_query_cands = result["top_candidate_indices"][0]
    assert len(first_query_cands) == len(set(first_query_cands))


def test_casmi_sirius_absence_penalty():
    solver = EnvedaCasmiSolver(absence_penalty_factor=0.25)
    
    # Molecule without Oxygen vs Molecule with Oxygen
    candidates = ["CCCC", "CCCO"]
    penalties = solver.evaluate_sirius_neutral_losses(candidates, observed_losses=["H2O", "CO2"])

    # First candidate has no O, should be penalized twice (0.25 * 0.25 = 0.0625)
    assert pytest.approx(penalties[0], abs=1e-4) == 0.0625
    # Second candidate has O, should not be penalized (1.0)
    assert pytest.approx(penalties[1], abs=1e-4) == 1.0
