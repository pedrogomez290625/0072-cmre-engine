"""MOD_SIGNAL - Feature Engineering & Signal Extraction Module.

Implements competitive feature extraction playbooks:
- Hierarchical Group Aggregations with the "delta trick" (Claim C07)
- Out-of-Fold Bayesian Target Encoding with m-estimate smoothing (Claims C04, C05, C06)
- Categorical interactions with frequency thresholding (Claim C09)
"""

from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Tuple


def compute_group_delta_stats(
    rows: List[Dict[str, Any]],
    group_key: str,
    value_key: str,
) -> Tuple[Dict[Any, float], List[float]]:
    """Calculates group means and delta residuals (x - mean_group) for a list of records.
    
    The 'Delta Trick' breaks the common-mean trap and produces localized signal.
    """
    group_sums: Dict[Any, float] = {}
    group_counts: Dict[Any, int] = {}

    for r in rows:
        g = r.get(group_key)
        val = float(r.get(value_key, 0.0) or 0.0)
        group_sums[g] = group_sums.get(g, 0.0) + val
        group_counts[g] = group_counts.get(g, 0) + 1

    group_means = {g: group_sums[g] / max(group_counts[g], 1) for g in group_sums}
    deltas = [float(r.get(value_key, 0.0) or 0.0) - group_means.get(r.get(group_key), 0.0) for r in rows]
    return group_means, deltas


class BayesianOofTargetEncoder:
    """Out-of-Fold Bayesian Target Encoder with m-estimate smoothing.
    
    Formula (Claim C06):
        TE_c = (n_c * mean_c + m * global_mean) / (n_c + m)
    
    Strictly isolates fit to training folds to prevent target leakage (Claims C04, C05).
    """

    def __init__(self, m_smoothing: float = 20.0, noise_level: float = 0.001):
        self.m_smoothing = m_smoothing
        self.noise_level = noise_level
        self.global_mean: float = 0.0
        self.category_stats: Dict[Any, Tuple[int, float]] = {}

    def fit(self, categories: List[Any], targets: List[float]) -> BayesianOofTargetEncoder:
        n_total = len(targets)
        if n_total == 0:
            return self
        
        self.global_mean = sum(targets) / float(n_total)
        counts: Dict[Any, int] = {}
        sums: Dict[Any, float] = {}

        for cat, y in zip(categories, targets):
            counts[cat] = counts.get(cat, 0) + 1
            sums[cat] = sums.get(cat, 0.0) + float(y)

        self.category_stats = {
            cat: (counts[cat], sums[cat] / counts[cat]) for cat in counts
        }
        return self

    def transform(self, categories: List[Any]) -> List[float]:
        encoded = []
        for cat in categories:
            if cat in self.category_stats:
                n_c, mean_c = self.category_stats[cat]
                te = (n_c * mean_c + self.m_smoothing * self.global_mean) / (n_c + self.m_smoothing)
            else:
                te = self.global_mean

            if self.noise_level > 0.0:
                te += random.gauss(0.0, self.noise_level)
            encoded.append(te)
        return encoded


CODE_TEMPLATE_TARGET_ENCODER = '''# [CMRE MOD_SIGNAL] Out-of-Fold Bayesian Target Encoding
import numpy as np
import pandas as pd

def oof_bayesian_target_encode(df_train, df_test, cat_cols, target_col, cv_splits, m=20.0, noise=0.005):
    """Encodes categorical columns strictly out-of-fold with Bayesian m-estimate smoothing."""
    train_encoded = df_train.copy()
    test_encoded = df_test.copy()
    
    global_mean = df_train[target_col].mean()

    for col in cat_cols:
        train_encoded[f"{col}__te"] = np.nan
        test_col_acc = np.zeros(len(df_test))
        
        for tr_idx, va_idx in cv_splits:
            tr, va = df_train.iloc[tr_idx], df_train.iloc[va_idx]
            
            # Compute stats purely inside train fold
            stats = tr.groupby(col)[target_col].agg(["count", "mean"])
            te_map = (stats["count"] * stats["mean"] + m * global_mean) / (stats["count"] + m)
            
            # Map validation fold
            mapped_va = va[col].map(te_map).fillna(global_mean)
            if noise > 0:
                mapped_va += np.random.normal(0, noise, size=len(mapped_va))
            train_encoded.iloc[va_idx, train_encoded.columns.get_loc(f"{col}__te")] = mapped_va
            
            # Accumulate test mapping
            test_col_acc += df_test[col].map(te_map).fillna(global_mean).values / len(cv_splits)

        test_encoded[f"{col}__te"] = test_col_acc

    return train_encoded, test_encoded
'''
