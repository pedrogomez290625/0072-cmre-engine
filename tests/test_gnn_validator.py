from cmre.modules.ood import GNNPlausibilityValidator

def test_gnn_plausibility_validator():
    validator = GNNPlausibilityValidator(plausibility_threshold_percentile=10.0, penalty_factor=0.1)

    # Fit with some normal looking SMILES
    training = ["C1=CC=CC=C1", "CC(=O)OC1=CC=CC=C1C(=O)O", "CCO"]
    validator.fit(training)

    candidates = [
        "C1=CC=CC=C1", # Normal, ring
        "C",           # Too short, no ring -> low score
        "XXXXXXXXXX"   # Hetero penalty -> low score
    ]
    initial_scores = [1.0, 1.0, 1.0]

    penalized = validator.evaluate(candidates, initial_scores)

    assert len(penalized) == 3
    # First one should be untouched
    assert penalized[0] == 1.0
    # The others should be heavily penalized
    assert penalized[1] == 0.1
    assert penalized[2] == 0.1
