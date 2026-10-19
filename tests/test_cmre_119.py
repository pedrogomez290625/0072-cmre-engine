"""Test for CMRE-119: Mitigación de SCAFFOLD_ANALOG_MEMORIZATION_LEAK.

Verifies molecular_scaffold_split function.
"""
from cmre.modules.split import molecular_scaffold_split


def test_scaffold_split_mitigates_analog_leak():
    # Simple scaffolds
    scaffolds = [
        "scaffold_A", "scaffold_B", "scaffold_A", "scaffold_C",
        "scaffold_B", "scaffold_A", "scaffold_D", "scaffold_C"
    ]

    train_idx, val_idx = molecular_scaffold_split(scaffolds, test_ratio=0.25)

    # Check disjunction: NO scaffold from train should be in val
    train_scaffolds = {scaffolds[i] for i in train_idx}
    val_scaffolds = {scaffolds[i] for i in val_idx}

    assert train_scaffolds.isdisjoint(val_scaffolds), "Memorization Leak! Scaffolds leaked between splits."

    # Check that all indices are accounted for
    assert set(train_idx).union(set(val_idx)) == set(range(len(scaffolds)))
