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

# Principales pérdidas neutrales comunes en espectrometría de masas (Da)
COMMON_NEUTRAL_LOSSES = {
    "H2O": (18.0106, ["O"]),
    "NH3": (17.0265, ["N"]),
    "CO": (27.9949, ["O", "C"]),
    "CO2": (43.9898, ["O"]),
    "HCOOH": (46.0055, ["O"]),
    "CH3COOH": (60.0211, ["O"]),
}

class SIRIUSAbsenceAxiomOptimizer:
    """Universal SIRIUS Absence Axiom Optimizer (Filtro Neutro Biofísico) (Claim CMRE-44).

    Aplica una penalización severa a moléculas (decoys) que, dados ciertos picos de
    pérdida neutral detectados en el espectro MS/MS, no contienen los elementos químicos
    fundamentales esperados.
    """

    def __init__(self, absence_penalty_factor: float = 0.35):
        self.absence_penalty_factor = absence_penalty_factor

    def evaluate(self, candidate_smiles: List[str], observed_losses: List[str]) -> np.ndarray:
        """Calculates penalty weights for candidates based on absence of required elements."""
        penalties = np.ones(len(candidate_smiles), dtype=np.float32)
        if not observed_losses:
            return penalties

        for i, smi in enumerate(candidate_smiles):
            for loss_name in observed_losses:
                if loss_name in COMMON_NEUTRAL_LOSSES:
                    required_elements = COMMON_NEUTRAL_LOSSES[loss_name][1]
                    for elem in required_elements:
                        if elem not in smi:
                            penalties[i] *= self.absence_penalty_factor
                            break
        return penalties


class GNNPlausibilityValidator:
    """Detector de Decoys Basado en Grafos Moleculares (Claim CMRE-47).

    Estimador heurístico para evaluar estructuralmente si un "SMILES_graph"
    propuesto como decoy es energéticamente estable o biofísicamente probable
    dentro del dominio metabolómico.
    """

    def __init__(self, plausibility_threshold_percentile: float = 5.0, penalty_factor: float = 0.1):
        self.threshold = plausibility_threshold_percentile
        self.penalty_factor = penalty_factor
        self.reference_distribution: List[float] = []

    def fit(self, training_smiles: List[str]) -> GNNPlausibilityValidator:
        """Mock fitting of the plausibility score distribution based on training data."""
        import numpy as np
        self.reference_distribution = [self._calculate_raw_score(s) for s in training_smiles]
        if not self.reference_distribution:
            self.reference_distribution = [50.0] # Default center
        return self

    def _calculate_raw_score(self, smiles: str) -> float:
        """
        Mocks a GNN GraphSAGE score. Real impl would parse networkx graph from SMILES
        and run a forward pass of a lightweight GNN.
        Here we use a dummy heuristic: Length and ring presence (C1=CC=CC=C1 etc).
        """
        length_score = min(len(smiles) / 50.0, 1.0) * 50.0
        ring_bonus = 20.0 if "1" in smiles or "2" in smiles else 0.0
        hetero_penalty = -10.0 if smiles.count("X") > 0 else 0.0 # Unknown elements
        return max(0.0, min(100.0, length_score + ring_bonus + hetero_penalty))

    def evaluate(self, candidate_smiles: List[str], current_scores: List[float]) -> List[float]:
        """
        Penaliza candidatos cuyo score estructural cae en percentiles inferiores.
        """
        import numpy as np
        if not candidate_smiles or not self.reference_distribution:
            return current_scores

        threshold_val = np.percentile(self.reference_distribution, self.threshold)

        penalized_scores = list(current_scores)
        for i, smi in enumerate(candidate_smiles):
            plausibility = self._calculate_raw_score(smi)
            if plausibility < threshold_val:
                penalized_scores[i] *= self.penalty_factor

        return penalized_scores
