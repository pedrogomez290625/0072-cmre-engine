"""MOD_SPLIT - Anti-Leakage Cross-Validation & Splitting Module.

Implements rigorous validation strategies:
- Group-Disjoint CV for entities/patients (Claim C01, FC03)
- Causal Walk-Forward with Purged intervals and Embargo (Claims C02, C03, FC07)
- Chemical Bemis-Murcko Scaffold Split for molecular ML (Claim FC06)
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, Generator, List, Optional, Set, Tuple


def group_disjoint_kfold(
    groups: List[Any],
    n_splits: int = 5,
    seed: int = 42,
) -> List[Tuple[List[int], List[int]]]:
    """Partitions indices into n_splits folds such that every group appears in EXACTLY one fold.
    
    Prevents patient, hospital, device, or user data leakage (Claim C01).
    """
    unique_groups = sorted(list(set(groups)), key=lambda g: hashlib.md5(str(g).encode()).hexdigest())
    
    # Hash-based deterministic assignment
    fold_assignments: Dict[Any, int] = {}
    for idx, g in enumerate(unique_groups):
        fold_assignments[g] = idx % n_splits

    folds: List[Tuple[List[int], List[int]]] = []
    all_indices = list(range(len(groups)))

    for f in range(n_splits):
        val_idx = [i for i, g in enumerate(groups) if fold_assignments[g] == f]
        train_idx = [i for i, g in enumerate(groups) if fold_assignments[g] != f]
        folds.append((train_idx, val_idx))

    return folds


def purged_timeseries_split(
    timestamps: List[int | float],
    n_splits: int = 5,
    embargo_pct: float = 0.01,
) -> List[Tuple[List[int], List[int]]]:
    """Generates causal expanding splits with purged intervals and embargo.
    
    Prevents lookahead bias and serial correlation leakage (Claims C02, C03).
    """
    sorted_indices = sorted(range(len(timestamps)), key=lambda i: timestamps[i])
    n = len(sorted_indices)
    
    folds = []
    test_size = n // (n_splits + 1)
    embargo_size = max(1, int(n * embargo_pct))

    for split in range(1, n_splits + 1):
        train_end = split * test_size
        val_start = train_end + embargo_size
        val_end = min(n, val_start + test_size)

        if val_start >= n:
            break

        train_indices = [sorted_indices[i] for i in range(0, train_end)]
        val_indices = [sorted_indices[i] for i in range(val_start, val_end)]
        
        folds.append((train_indices, val_indices))

    return folds


def molecular_scaffold_split(
    scaffolds: List[str],
    test_ratio: float = 0.2,
    seed: int = 42,
) -> Tuple[List[int], List[int]]:
    """Splits chemical compounds based on core Bemis-Murcko molecular scaffolds.
    
    Ensures Out-of-Distribution evaluation on structurally novel chemical scaffolds (Claim FC06).
    """
    scaffold_to_indices: Dict[str, List[int]] = {}
    for idx, sc in enumerate(scaffolds):
        scaffold_to_indices.setdefault(sc, []).append(idx)

    # Sort scaffolds by size descending to distribute large clusters fairly
    sorted_scaffolds = sorted(
        scaffold_to_indices.keys(),
        key=lambda s: (len(scaffold_to_indices[s]), hashlib.sha256(s.encode()).hexdigest()),
        reverse=True,
    )

    n_total = len(scaffolds)
    n_test = int(n_total * test_ratio)
    
    train_indices: List[int] = []
    test_indices: List[int] = []

    for sc in sorted_scaffolds:
        idxs = scaffold_to_indices[sc]
        if len(test_indices) + len(idxs) <= n_test:
            test_indices.extend(idxs)
        else:
            train_indices.extend(idxs)

    return train_indices, test_indices


CODE_TEMPLATE_PURGED_CV = '''# [CMRE MOD_SPLIT] Purged Group TimeSeries Split
import numpy as np

class PurgedGroupTimeSeriesSplit:
    def __init__(self, n_splits=5, embargo_samples=10):
        self.n_splits = n_splits
        self.embargo = embargo_samples

    def split(self, X, y=None, groups=None):
        n = len(X)
        fold_size = n // (self.n_splits + 1)
        for i in range(1, self.n_splits + 1):
            train_end = i * fold_size
            val_start = train_end + self.embargo
            val_end = min(n, val_start + fold_size)
            if val_start < n:
                yield np.arange(0, train_end), np.arange(val_start, val_end)
'''
