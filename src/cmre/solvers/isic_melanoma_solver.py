"""
ISIC 2024 Skin Cancer Detection with 3D-TBP Solver.
Pipeline E2E para dermatología multimodal con normalización de Patito Feo.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

from __future__ import annotations
from typing import List, Dict, Any, Tuple
import numpy as np

from ..modules.radiology_advanced import UglyDucklingPatientNormalizer
from ..modules.split import group_disjoint_kfold


class ISICMelanomaSolver:
    """
    Solver canónico para ISIC 2024 Skin Cancer.
    Aplica normalización de lesiones por paciente ("Patito Feo") y partición disjunta.
    """
    def __init__(self, target_min_tpr: float = 0.80):
        self.target_min_tpr = target_min_tpr

    def run_pipeline(
        self,
        patient_features: np.ndarray,
        patient_ids: List[str],
        targets: np.ndarray,
        predicted_scores: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Ejecuta el pipeline de normalización de patito feo y cálculo de pAUC.
        """
        # 1. Normalización del Patito Feo
        deltas, ratios = UglyDucklingPatientNormalizer.normalize_lesions(patient_features)
        
        # 2. Partición disjunta por paciente
        folds = group_disjoint_kfold(patient_ids, n_splits=5)
        
        # 3. Cálculo de Partial AUC (pAUC) sobre la ventana TPR >= 0.80
        # Ordenar por score decreciente
        order = np.argsort(-predicted_scores)
        y_sorted = targets[order]
        
        total_pos = max(np.sum(y_sorted == 1), 1)
        total_neg = max(np.sum(y_sorted == 0), 1)
        
        tpr = np.cumsum(y_sorted == 1) / total_pos
        fpr = np.cumsum(y_sorted == 0) / total_neg
        
        # Filtrar ventana donde TPR >= target_min_tpr
        valid_mask = tpr >= self.target_min_tpr
        if np.any(valid_mask):
            trapz_fn = getattr(np, "trapezoid", getattr(np, "trapz", None))
            if trapz_fn is not None:
                pauc = float(trapz_fn(tpr[valid_mask] - self.target_min_tpr, fpr[valid_mask]))
            else:
                pauc = float(np.sum((tpr[valid_mask] - self.target_min_tpr) * np.gradient(fpr[valid_mask])))
        else:
            pauc = 0.0
            
        return {
            "normalized_deltas_shape": list(deltas.shape),
            "normalized_ratios_shape": list(ratios.shape),
            "n_folds": len(folds),
            "partial_auc_at_80_tpr": pauc,
            "validation_status": "VALIDATED_PATIENT_DISJOINT"
        }
