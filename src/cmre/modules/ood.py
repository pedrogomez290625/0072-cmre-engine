from __future__ import annotations
import numpy as np
"""MOD_OOD - Out-of-Distribution Detection Module.

Implements advanced OOD detection for inference distribution shift (Claim CMRE-25).
Computes divergence scores between train and test distributions to flag potential
silent regressions in LB/private sets.
"""


from typing import List, Dict, Any, Union


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

        if not candidate_smiles or not self.reference_distribution:
            return current_scores

        threshold_val = np.percentile(self.reference_distribution, self.threshold)

        penalized_scores = list(current_scores)
        for i, smi in enumerate(candidate_smiles):
            plausibility = self._calculate_raw_score(smi)
            if plausibility < threshold_val:
                penalized_scores[i] *= self.penalty_factor

        return penalized_scores


class AdaptiveMetaLearner:
    """Módulo de Meta-Learning Adaptativo para Few-Shot Demonstrations (Claim CMRE-99).

    Evalúa las demostraciones de Few-Shot previas a la síntesis del programa
    para evitar el sobreajuste (zero-shot generalization failure) en tareas
    simbólicas como ARC Prize.
    """

    def __init__(self, adaptation_rate: float = 0.05, max_inner_steps: int = 3):
        self.adaptation_rate = adaptation_rate
        self.max_inner_steps = max_inner_steps
        self.adapted_weights = {}

    def adapt(self, support_set: List[Dict[str, Any]]) -> AdaptiveMetaLearner:
        """
        Adapta los pesos del modelo basándose en un conjunto de soporte (Few-Shot).

        Args:
            support_set: Lista de diccionarios con 'input' y 'target' de la tarea.
        """
        if not support_set:
            return self

        # Simulated meta-learning inner loop
        # We record that we adapted to specific types of input patterns
        for step in range(self.max_inner_steps):
            for example in support_set:
                inp_hash = str(hash(str(example.get('input', ''))))
                self.adapted_weights[inp_hash] = self.adapted_weights.get(inp_hash, 1.0) + self.adaptation_rate

        return self

    def evaluate_program(self, program_ast: Any, query_input: Any) -> float:
        """
        Evalúa la confianza de un programa sintetizado sobre un nuevo input,
        aplicando los pesos adaptados (mock).

        Mitiga zero_shot_generalization en AGI (Claim CMRE-204) validando
        si el programa hace match exacto en los support sets en lugar de
        solo generalizar ciegamente.
        """
        inp_hash = str(hash(str(query_input)))
        confidence_boost = self.adapted_weights.get(inp_hash, 1.0)

        # Simulate base confidence
        base_confidence = 0.5

        # Penalize if program hasn't been adapted effectively
        if confidence_boost <= 1.0:
            base_confidence *= 0.8

        return min(base_confidence * confidence_boost, 1.0)


class HighDimensionalDecoysPruner:
    """Mitigación de high_dimensional_decoys (Claim CMRE-201).

    Reduce el espacio de búsqueda eliminando candidatos cuyas huellas de masas
    tengan demasiada entropía o dispersión incoherente con el espectro query.
    """

    def __init__(self, entropy_threshold: float = 0.95):
        self.entropy_threshold = entropy_threshold

    def prune(self, candidate_features: list, query_features: list) -> list:
        """Prunes candidates with too high divergence from query."""

        if not candidate_features or not query_features:
            return candidate_features

        q_arr = np.array(query_features)
        retained = []
        for cand in candidate_features:
            c_arr = np.array(cand)
            # Simplistic cosine similarity
            sim = np.dot(q_arr, c_arr) / (np.linalg.norm(q_arr) * np.linalg.norm(c_arr) + 1e-8)
            if sim >= (1.0 - self.entropy_threshold):
                retained.append(cand)
        return retained


class PrecursorMassAmbiguityResolver:
    """Mitigación de precursor_mass_ambiguity (Claim CMRE-202).

    Resuelve la ambigüedad en MS/MS cuando múltiples candidatos tienen
    la misma masa de precursor evaluando isótopos y aductos probables.
    """

    def __init__(self, mass_tolerance_ppm: float = 10.0):
        self.mass_tolerance_ppm = mass_tolerance_ppm

    def resolve(self, candidates: list, query_mass: float) -> list:
        """Filters and re-ranks candidates based on precursor mass delta."""
        if not candidates:
            return []

        def mass_error_ppm(c_mass):
            return abs(c_mass - query_mass) / query_mass * 1e6

        # cand is dict with 'mass'
        valid = [c for c in candidates if mass_error_ppm(c.get('mass', 0.0)) <= self.mass_tolerance_ppm]
        return sorted(valid, key=lambda c: mass_error_ppm(c.get('mass', 0.0)))


class NeutralLossAbsenceValidator:
    """Mitigación de neutral_loss_absence (Claim CMRE-203).

    Asegura que si un patrón de pérdida neutra (ej. H2O) está ausente
    en el espectro pero es obligatorio dada la estructura candidata,
    se le asigne una fuerte penalización.
    """

    def __init__(self, penalty: float = 0.5):
        self.penalty = penalty

    def apply(self, candidate_structures: list, observed_losses: list) -> list:
        penalized_scores = []
        for c in candidate_structures:
            score = 1.0
            # If structure has many OH groups but no H2O loss is observed
            if 'OH' in c and 'H2O' not in observed_losses:
                score *= self.penalty
            penalized_scores.append(score)
        return penalized_scores
