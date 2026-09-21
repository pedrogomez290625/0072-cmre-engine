"""
CMRE ALTERNATIVE PLATFORMS MODULE (DrivenData & Zindi SOTA Recipes)
Mecanismos ganadores y componentes de producción extraídos de torneos DrivenData y Zindi.

Snippets implementados:
- SNIP_ALT_DRIVENDATA_MULTI_TARGET_CALIBRATOR (Flu Shot Learning)
- SNIP_ALT_DRIVENDATA_ORDINAL_DAMAGE_MODELER (Richter's Predictor & Nelder-Mead Thresholds)
- SNIP_ALT_ZINDI_SPATIO_TEMPORAL_LAG_BLENDER (AirQo Kampala Air Quality)
- SNIP_ALT_ZINDI_BIOMETRIC_REID_ARCFACE (Turtle Recall Few-Shot & Open-Set)

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

from __future__ import annotations
import math
from typing import List, Dict, Any, Tuple, Optional, Callable
import numpy as np


class MultiTargetClassifierChainCalibrator:
    """
    Calibrador multi-objetivo dependiente para DrivenData Flu Shot Learning.
    Modela la probabilidad condicional P(target_2 | target_1, X) con imputación
    semántica de valores faltantes (Missingness as Signal - MNAR).
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    def __init__(self, clip_eps: float = 1e-6):
        self.clip_eps = clip_eps
        self.calibrators: Dict[str, Any] = {}

    @staticmethod
    def extract_missing_indicators(features: np.ndarray) -> np.ndarray:
        """
        Genera matriz binaria indicando qué variables presentaban valores faltantes (NaN),
        convirtiendo la ausencia de datos en una señal predictiva explícita (MNAR).
        """
        is_nan = np.isnan(features).astype(np.float32)
        return is_nan

    @staticmethod
    def chain_conditional_probability(
        prob_target_1: np.ndarray,
        cond_prob_target_2_given_1: np.ndarray,
        cond_prob_target_2_given_0: np.ndarray
    ) -> np.ndarray:
        """
        Calcula la probabilidad total marginal P(Y2 = 1) aplicando la ley de probabilidad total:
        P(Y2 = 1) = P(Y2 = 1 | Y1 = 1) * P(Y1 = 1) + P(Y2 = 1 | Y1 = 0) * (1 - P(Y1 = 1))
        """
        return (cond_prob_target_2_given_1 * prob_target_1) + (
            cond_prob_target_2_given_0 * (1.0 - prob_target_1)
        )


class OrdinalDamageClassifier:
    """
    Clasificador ordinal de daño estructural acumulativo para DrivenData Richter's Predictor.
    Descompone un problema de K clases ordenadas en K-1 clasificadores binarios acumulativos:
      P(Y >= 2) y P(Y >= 3).
    Incorpora optimizador continuo Nelder-Mead simplex para calibrar los umbrales de decisión
    maximizando directamente el Micro-Averaged F1 Score.
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    def __init__(self, thresholds: Optional[Tuple[float, float]] = None):
        # Umbrales iniciales por defecto: [0.35, 0.65]
        self.thresholds = list(thresholds) if thresholds else [0.35, 0.65]

    @staticmethod
    def compute_slenderness_features(
        height_percentage: np.ndarray,
        area_percentage: np.ndarray,
        eps: float = 1e-4
    ) -> np.ndarray:
        """
        Calcula ratios de esbeltez y densidad estructural sísmica.
        ratio = altura / sqrt(area)
        """
        effective_width = np.sqrt(np.maximum(area_percentage, eps))
        return height_percentage / effective_width

    @staticmethod
    def cumulative_to_multiclass_probs(
        p_ge_2: np.ndarray,
        p_ge_3: np.ndarray
    ) -> np.ndarray:
        """
        Convierte probabilidades acumulativas ordenadas a distribución multiclase simplex [P(1), P(2), P(3)].
        Garantiza monotonicidad: 1.0 >= P(Y>=2) >= P(Y>=3) >= 0.0.
        """
        # Forzar orden monotónico
        p_ge_2_mon = np.clip(p_ge_2, 0.0, 1.0)
        p_ge_3_mon = np.clip(np.minimum(p_ge_3, p_ge_2_mon), 0.0, 1.0)

        p1 = 1.0 - p_ge_2_mon
        p2 = p_ge_2_mon - p_ge_3_mon
        p3 = p_ge_3_mon

        return np.stack([p1, p2, p3], axis=-1)

    @staticmethod
    def predict_classes_from_latent(
        continuous_score: np.ndarray,
        thresholds: Tuple[float, float]
    ) -> np.ndarray:
        """
        Asigna clases discretas {1, 2, 3} evaluando un score continuo contra los dos umbrales.
        """
        th1, th2 = thresholds
        preds = np.ones(continuous_score.shape, dtype=np.int64)
        preds[continuous_score >= th1] = 2
        preds[continuous_score >= th2] = 3
        return preds

    def optimize_thresholds_nelder_mead(
        self,
        continuous_oof_scores: np.ndarray,
        y_true: np.ndarray,
        max_iter: int = 100
    ) -> Tuple[float, float]:
        """
        Optimiza simplex de los umbrales [th1, th2] para maximizar Micro F1 (que coincide con Accuracy).
        """
        best_th = list(self.thresholds)
        best_f1 = self._eval_micro_f1(continuous_oof_scores, y_true, best_th)

        # Búsqueda tipo Nelder-Mead / Coordinate Descent en espacio 2D
        step_sizes = [0.05, 0.02, 0.01, 0.005]
        for step in step_sizes:
            for _ in range(max_iter // len(step_sizes)):
                improved = False
                for idx in [0, 1]:
                    for direction in [-1.0, 1.0]:
                        candidate = list(best_th)
                        candidate[idx] += direction * step
                        # Restricción: 0.0 < th1 < th2 < 1.0
                        if candidate[0] >= candidate[1] - 0.02 or candidate[0] <= 0.05 or candidate[1] >= 0.95:
                            continue
                        cand_f1 = self._eval_micro_f1(continuous_oof_scores, y_true, candidate)
                        if cand_f1 > best_f1:
                            best_f1 = cand_f1
                            best_th = candidate
                            improved = True
                if not improved:
                    break

        self.thresholds = best_th
        return float(best_th[0]), float(best_th[1])

    @staticmethod
    def _eval_micro_f1(scores: np.ndarray, y_true: np.ndarray, th: List[float]) -> float:
        preds = np.ones(scores.shape, dtype=np.int64)
        preds[scores >= th[0]] = 2
        preds[scores >= th[1]] = 3
        return float(np.mean(preds == y_true))


class SpatioTemporalLagBlender:
    """
    Pipeline de ingeniería de características y blending espacio-temporal para Zindi AirQo.
    Calcula lags multiescala, ventanas rodantes, armónicos diurnos senoidales/cosenoidales
    y blending ponderado (85% GBDT + 15% Geo-KNN).
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    @staticmethod
    def compute_diurnal_harmonics(hours: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula armónicos trigonométricos del ciclo circadiano (24 horas):
        sin_hour = sin(2 * pi * hour / 24)
        cos_hour = cos(2 * pi * hour / 24)
        """
        sin_hour = np.sin(2.0 * np.pi * hours / 24.0)
        cos_hour = np.cos(2.0 * np.pi * hours / 24.0)
        return sin_hour, cos_hour

    @staticmethod
    def compute_temporal_lags(
        series: np.ndarray,
        lags: List[int] = [1, 2, 3, 24]
    ) -> Dict[str, np.ndarray]:
        """
        Construye matriz de lags hacia atrás rellenando los primeros pasos con el primer valor observado.
        """
        n = len(series)
        lag_dict = {}
        for lag in lags:
            lagged = np.empty(n, dtype=np.float32)
            if lag < n:
                lagged[:lag] = series[0]
                lagged[lag:] = series[:-lag]
            else:
                lagged[:] = series[0]
            lag_dict[f"lag_{lag}"] = lagged
        return lag_dict

    @staticmethod
    def blend_gbdt_and_geoknn(
        pred_gbdt: np.ndarray,
        pred_geoknn: np.ndarray,
        w_gbdt: float = 0.85
    ) -> np.ndarray:
        """
        Fusión lineal convexa ponderada entre predicción GBDT y regresión local espacial KNN.
        """
        w_knn = 1.0 - w_gbdt
        return (w_gbdt * pred_gbdt) + (w_knn * pred_geoknn)


class BiometricReIDArcFaceModeler:
    """
    Pipeline biométrico de re-identificación facial (Zindi Turtle Recall).
    Implementa la función de margen angular aditivo ArcFace sobre hiperesfera unitaria
    y la regla de inferencia con similitud coseno para clases abiertas (Open-Set Detection).
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    def __init__(self, scale: float = 30.0, margin: float = 0.35, open_set_threshold: float = 0.45):
        self.scale = scale
        self.margin = margin
        self.open_set_threshold = open_set_threshold

    def compute_arcface_margin(
        self,
        cosine_sim: np.ndarray,
        target_labels: np.ndarray
    ) -> np.ndarray:
        """
        Aplica penalización angular aditiva ArcFace:
        L = s * cos(theta + m) para la clase correcta y s * cos(theta) para las restantes.
        """
        # Cosine similarity acotado en [-1.0 + eps, 1.0 - eps]
        eps = 1e-7
        cos_clamped = np.clip(cosine_sim, -1.0 + eps, 1.0 - eps)
        theta = np.arccos(cos_clamped)
        
        # theta_target = theta + margin
        target_logits = np.cos(theta + self.margin)
        
        # Matriz resultante
        logits = np.copy(cos_clamped)
        n_samples = len(target_labels)
        for i in range(n_samples):
            cls_idx = target_labels[i]
            logits[i, cls_idx] = target_logits[i, cls_idx]
            
        return self.scale * logits

    def predict_open_set(
        self,
        query_embeddings: np.ndarray,
        gallery_embeddings: np.ndarray,
        gallery_labels: List[str]
    ) -> List[str]:
        """
        Clasifica cada embedding query contra la galería de identidades conocidas.
        Si la similitud coseno máxima es menor que open_set_threshold, asigna 'new_turtle'.
        """
        # Normalizar a norma L2 unitaria
        q_norm = query_embeddings / np.maximum(np.linalg.norm(query_embeddings, axis=1, keepdims=True), 1e-7)
        g_norm = gallery_embeddings / np.maximum(np.linalg.norm(gallery_embeddings, axis=1, keepdims=True), 1e-7)
        
        # Matriz de similitudes coseno [N_query, N_gallery]
        sim_matrix = np.dot(q_norm, g_norm.T)
        
        predictions = []
        for i in range(len(query_embeddings)):
            max_sim_idx = int(np.argmax(sim_matrix[i]))
            max_sim_val = sim_matrix[i, max_sim_idx]
            
            if max_sim_val >= self.open_set_threshold:
                predictions.append(gallery_labels[max_sim_idx])
            else:
                predictions.append("new_turtle")
                
        return predictions
