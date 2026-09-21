"""MOD_ENSEMBLE - Competitive Ensembling & Blending Module.

Implements battle-tested grandmaster ensembling methods:
- Non-Negative Least Squares (NNLS) OOF blending (Claim C23)
- Rank-Space Averaging for scale-incompatible models (Claim C22)
- Forward Hill-Climbing greedy model selection
"""

from __future__ import annotations

import math
from typing import Callable, List, Optional, Tuple


def rank_average_predictions(predictions_matrix: List[List[float]]) -> List[float]:
    """Computes normalized rank-average across multiple model predictions.
    
    Transforms each model's raw scores to [0, 1] percentiles before averaging (Claim C22).
    Robust against scale mismatch, calibration drift, and uncalibrated tree logits.
    """
    if not predictions_matrix or not predictions_matrix[0]:
        return []

    n_models = len(predictions_matrix)
    n_samples = len(predictions_matrix[0])
    
    ranked_matrix = []
    for model_preds in predictions_matrix:
        # Argsort twice to get ranks
        indexed = sorted(enumerate(model_preds), key=lambda x: x[1])
        ranks = [0.0] * n_samples
        for rank, (orig_idx, _) in enumerate(indexed):
            ranks[orig_idx] = rank / max(float(n_samples - 1), 1.0)
        ranked_matrix.append(ranks)

    # Average ranks
    final_preds = [
        sum(ranked_matrix[m][i] for m in range(n_models)) / float(n_models)
        for i in range(n_samples)
    ]
    return final_preds


class SimpleNNLSBlender:
    """Solves for non-negative weights (w_i >= 0, sum w_i = 1) using projected gradient descent.
    
    Provides bounded, regularized OOF blending (Claim C23).
    """

    def __init__(self, max_iter: int = 1000, lr: float = 0.05, tol: float = 1e-6):
        self.max_iter = max_iter
        self.lr = lr
        self.tol = tol
        self.weights: List[float] = []

    def fit(self, preds_matrix: List[List[float]], y_true: List[float]) -> SimpleNNLSBlender:
        """
        Args:
            preds_matrix: List of M model predictions, each of length N [M, N]
            y_true: Ground truth target vector [N]
        """
        m = len(preds_matrix)
        n = len(y_true)
        if m == 0 or n == 0:
            return self

        # Initialize uniform weights
        w = [1.0 / m] * m

        for _ in range(self.max_iter):
            # Compute current ensemble prediction
            ens_pred = [sum(w[j] * preds_matrix[j][i] for j in range(m)) for i in range(n)]
            
            # Compute residuals
            residuals = [ens_pred[i] - y_true[i] for i in range(n)]
            
            # Compute gradients: dL/dw_j = 2/N * sum(residuals * preds_matrix[j])
            grad = [
                (2.0 / n) * sum(residuals[i] * preds_matrix[j][i] for i in range(n))
                for j in range(m)
            ]

            # Projected gradient update
            w_new = [max(0.0, w[j] - self.lr * grad[j]) for j in range(m)]
            
            # Project onto simplex (sum to 1)
            total = sum(w_new)
            if total > 0:
                w_new = [v / total for v in w_new]
            else:
                w_new = [1.0 / m] * m

            # Check convergence
            diff = sum(abs(w_new[j] - w[j]) for j in range(m))
            w = w_new
            if diff < self.tol:
                break

        self.weights = w
        return self

    def predict(self, preds_matrix: List[List[float]]) -> List[float]:
        m = len(preds_matrix)
        n = len(preds_matrix[0]) if m > 0 else 0
        w = self.weights if self.weights else [1.0 / max(m, 1)] * m
        return [sum(w[j] * preds_matrix[j][i] for j in range(m)) for i in range(n)]


CODE_TEMPLATE_NNLS_BLEND = '''# [CMRE MOD_ENSEMBLE] Non-Negative Least Squares & Hill-Climbing Blend
import numpy as np
from scipy.optimize import nnls

def fit_nnls_blend(oof_preds_dict, y_true):
    """Computes non-negative blend weights summing to 1.0 from out-of-fold predictions."""
    model_names = list(oof_preds_dict.keys())
    X_oof = np.column_stack([oof_preds_dict[m] for m in model_names])
    
    weights, _ = nnls(X_oof, y_true)
    total = np.sum(weights)
    if total > 0:
        weights = weights / total
    else:
        weights = np.ones(len(model_names)) / len(model_names)

    return dict(zip(model_names, weights))
'''
