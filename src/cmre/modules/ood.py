"""MOD_OOD - Out-of-Distribution Detection Module.

Implements advanced OOD detection for inference distribution shift (Claim CMRE-25).
Computes divergence scores between train and test distributions to flag potential
silent regressions in LB/private sets.
"""

from __future__ import annotations

from typing import List, Dict, Any, Union
import numpy as np

class OODDetector:
    """Advanced OOD (Out-of-Distribution) Detector.

    Monitors data drift by measuring the divergence score between reference (train)
    and incoming target (test) distributions.
    """

    def __init__(self, threshold: float = 0.5):
        """
        Args:
            threshold: Divergence threshold above which data is considered OOD.
        """
        self.threshold = threshold
        self.reference_stats: Dict[str, Dict[str, float]] = {}

    def fit(self, X: np.ndarray, feature_names: List[str] = None) -> OODDetector:
        """Computes reference statistics from training data.

        Args:
            X: Training data array of shape (N_samples, N_features)
            feature_names: Optional list of feature names.
        """
        if feature_names is None:
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]

        for i, name in enumerate(feature_names):
            col = X[:, i]
            self.reference_stats[name] = {
                "mean": float(np.mean(col)),
                "std": float(np.std(col)) + 1e-8,
            }
        return self

    def compute_divergence(self, X: np.ndarray, feature_names: List[str] = None) -> Dict[str, Union[float, bool, Dict[str, float]]]:
        """Computes Z-score based divergence for the incoming data batch.

        Args:
            X: Inference data array of shape (N_samples, N_features)
            feature_names: Optional list of feature names.

        Returns:
            Dictionary containing 'is_ood', 'mean_divergence', and per-feature divergence.
        """
        if not self.reference_stats:
            raise ValueError("OODDetector is not fitted. Call fit() first.")

        if feature_names is None:
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]

        feature_divergences = {}
        total_div = 0.0

        for i, name in enumerate(feature_names):
            if name not in self.reference_stats:
                continue

            col = X[:, i]
            ref_mean = self.reference_stats[name]["mean"]
            ref_std = self.reference_stats[name]["std"]

            # Use mean of Z-scores or Wasserstein-like metric. Here we use
            # absolute difference of means scaled by reference std.
            target_mean = float(np.mean(col))
            div = abs(target_mean - ref_mean) / ref_std
            feature_divergences[name] = div
            total_div += div

        mean_div = total_div / len(feature_divergences) if feature_divergences else 0.0

        return {
            "is_ood": mean_div > self.threshold,
            "mean_divergence": mean_div,
            "feature_divergences": feature_divergences,
        }
