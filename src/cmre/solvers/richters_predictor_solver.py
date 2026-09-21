"""
DrivenData Richter's Predictor Solver.
Pipeline E2E para predicción ordinal de daño estructural por terremoto.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

from __future__ import annotations
from typing import List, Dict, Any, Tuple
import numpy as np

from ..modules.alternative_platforms import OrdinalDamageClassifier


class RichtersPredictorSolver:
    """
    Solver canónico para DrivenData Richter's Predictor.
    Aplica ratios de esbeltez estructural y calibración simplex Nelder-Mead de umbrales para Micro-F1.
    """
    def __init__(self):
        self.classifier = OrdinalDamageClassifier()

    def run_pipeline(
        self,
        heights: np.ndarray,
        areas: np.ndarray,
        continuous_oof_scores: np.ndarray,
        y_true: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Ejecuta el pipeline de features de ingeniería sísmica y optimización de umbrales.
        """
        # 1. Ratios estructurales de esbeltez
        slenderness = self.classifier.compute_slenderness_features(heights, areas)
        
        # 2. Optimización simplex Nelder-Mead de umbrales en OOF
        th1, th2 = self.classifier.optimize_thresholds_nelder_mead(continuous_oof_scores, y_true)
        
        # 3. Predicción de clases discretas {1, 2, 3}
        final_preds = self.classifier.predict_classes_from_latent(continuous_oof_scores, (th1, th2))
        micro_f1 = float(np.mean(final_preds == y_true))
        
        return {
            "slenderness_mean": float(np.mean(slenderness)),
            "optimized_thresholds": [th1, th2],
            "calibrated_micro_f1": micro_f1,
            "validation_status": "VALIDATED_ORDINAL_NELDER_MEAD"
        }
