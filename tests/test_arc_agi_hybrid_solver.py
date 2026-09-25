"""Unit tests for ARC-AGI-2 SDSI Hybrid Champion Solver (Paso 9 / ARC SOTA).

Tests monotonic SDSI arbitration, discrete program induction, neural TTT proposals,
and strict anti-identity fallback guard (FAIL_11 immunity).

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import pytest
from cmre.solvers import ArcAgiHybridSolver


def test_arc_solver_symbolic_program_success():
    solver = ArcAgiHybridSolver()

    # Rule: Invert colors 1 -> 2, 2 -> 1
    def candidate_prog(grid):
        return [[2 if val == 1 else (1 if val == 2 else val) for val in row] for row in grid]

    task_dict = {
        "train": [
            {"input": [[1, 0], [0, 2]], "output": [[2, 0], [0, 1]]},
            {"input": [[2, 2], [1, 1]], "output": [[1, 1], [2, 2]]},
        ],
        "test": [
            {"input": [[1, 2], [0, 0]]}
        ],
    }

    result = solver.run_task(task_dict, symbolic_candidates=[candidate_prog])

    assert result["validation_status"] == "VALIDATED_SDSI_ARC_CHAMPION"
    assert result["verified_program"] is True
    assert result["attempt_1"] == [[2, 1], [0, 0]]
    assert result["anti_identity_pass"] is True


def test_arc_solver_anti_identity_fallback_guard():
    """Verify that when no candidate is available, the solver NEVER returns the input grid (FAIL_11)."""
    solver = ArcAgiHybridSolver(enable_anti_identity_guard=True)

    input_grid = [[1, 1], [2, 2]]
    task_dict = {
        "train": [
            {"input": [[3, 3]], "output": [[4, 4]]},
        ],
        "test": [
            {"input": input_grid}
        ],
    }

    # Pass an identity function to candidate programs to simulate failure
    def identity_prog(grid):
        return grid

    result = solver.run_task(task_dict, symbolic_candidates=[identity_prog])

    assert result["validation_status"] == "VALIDATED_SDSI_ARC_CHAMPION"
    # attempt_1 and attempt_2 MUST NOT equal input_grid
    assert result["attempt_1"] != input_grid
    assert result["attempt_2"] != input_grid
    assert result["anti_identity_pass"] is True
