from cmre.modules.ensemble import LatencyBudgetPruner

def test_latency_budget_pruner_dynamic_route():
    pruner = LatencyBudgetPruner(max_latency_seconds=1.5)

    # High confidence, low complexity -> Early exit (False)
    route_heavy = pruner.dynamic_route(fast_model_confidence=0.95, sample_complexity=1.0)
    assert not route_heavy

    # Low confidence -> Route heavy (True)
    route_heavy2 = pruner.dynamic_route(fast_model_confidence=0.60, sample_complexity=1.0)
    assert route_heavy2

    # High complexity -> Route heavy (True)
    route_heavy3 = pruner.dynamic_route(fast_model_confidence=0.90, sample_complexity=2.0)
    assert route_heavy3
