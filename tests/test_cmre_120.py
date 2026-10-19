"""Test for CMRE-120: Mitigación de SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE.

Verifies ArcAgiHybridSolver anti-identity guard mechanism.
"""
from cmre.solvers.arc_agi_hybrid_solver import ArcAgiHybridSolver


def test_hybrid_solver_mitigates_identity_collapse():
    solver = ArcAgiHybridSolver(enable_anti_identity_guard=True)

    input_grid = [[1, 2], [3, 4]]
    task_dict = {
        "train": [
            {"input": [[5, 6]], "output": [[6, 5]]}
        ],
        "test": [
            {"input": input_grid}
        ]
    }

    # We provide a dummy program that fails or returns identity to simulate symbolic failure
    def bad_program(inp):
        return inp # Identity fallback!

    result = solver.run_task(task_dict, symbolic_candidates=[bad_program], neural_proposals=[input_grid])

    # Verify attempts don't match the input
    attempt_1 = result.get("attempt_1")
    attempt_2 = result.get("attempt_2")

    assert not solver._is_identity(attempt_1, input_grid), "Anti-Identity failed! Attempt 1 is identical to input."
    assert not solver._is_identity(attempt_2, input_grid), "Anti-Identity failed! Attempt 2 is identical to input."
    assert result.get("anti_identity_pass") is True
