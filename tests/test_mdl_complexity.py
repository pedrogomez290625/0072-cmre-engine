from cmre.modules.loss import MDLComplexityOptimizer

def test_mdl_complexity_optimizer():
    optimizer = MDLComplexityOptimizer(alpha=1.0, beta=100.0)

    cost1 = optimizer.compute_cost(num_ast_nodes=10, error_rate=0.0)
    assert cost1 == 10.0

    cost2 = optimizer.compute_cost(num_ast_nodes=5, error_rate=0.1)
    # 5 * 1.0 + 0.1 * 100.0 = 5 + 10 = 15.0
    assert cost2 == 15.0

    programs = [
        {"nodes": 100, "error_rate": 0.0}, # Overfitted spaghetti: cost 100
        {"nodes": 10, "error_rate": 0.5},  # Too simple, high error: 10 + 50 = 60
        {"nodes": 15, "error_rate": 0.1},  # Balanced: 15 + 10 = 25 -> Should win
    ]

    best_idx = optimizer.select_best_program(programs)
    assert best_idx == 2
