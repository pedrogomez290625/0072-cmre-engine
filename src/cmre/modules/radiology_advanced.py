"""
CMRE ADVANCED RADIOLOGY & MEDICAL VISION MODULE
Pipelines y arquitecturas de visión médica de élite para RSNA Screening Mammography, HuBMAP e ISIC Melanoma.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

from __future__ import annotations
import math
from typing import List, Tuple, Dict, Any, Optional
import numpy as np

try:
    import torch
    import torch.nn as nn
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    class DummyModule:
        pass
    class MockNN:
        Module = DummyModule
    nn = MockNN()


class CrossViewMammographyAttention(nn.Module):
    """
    Bloque de atención cruzada bidireccional CC <-> MLO sobre representaciones espaciales del mismo seno.
    Inspirado en las soluciones campeonas de RSNA Screening Mammography (1st dangnh0611 / 5th analokmaus).
    Resuelve la superposición de tejido glandular contrastando la masa en ambas proyecciones ortogonales.
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    def __init__(self, in_features: int = 512, num_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.in_features = in_features
        if HAS_TORCH:
            self.mha_cc_to_mlo = nn.MultiheadAttention(embed_dim=in_features, num_heads=num_heads, dropout=dropout, batch_first=True)
            self.mha_mlo_to_cc = nn.MultiheadAttention(embed_dim=in_features, num_heads=num_heads, dropout=dropout, batch_first=True)
            self.norm_cc = nn.LayerNorm(in_features)
            self.norm_mlo = nn.LayerNorm(in_features)
            self.fc_fusion = nn.Sequential(
                nn.Linear(in_features * 2, in_features),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(in_features, 1) # Logit de malignidad
            )

    def forward(self, feat_cc: Any, feat_mlo: Any) -> Tuple[Any, Any]:
        """
        feat_cc: [Batch, SeqLen, in_features] o [Batch, in_features]
        feat_mlo: [Batch, SeqLen, in_features] o [Batch, in_features]
        Devuelve: (logit_pred, fused_representation)
        """
        if not HAS_TORCH:
            raise ImportError("PyTorch es requerido para CrossViewMammographyAttention")
            
        if feat_cc.dim() == 2:
            feat_cc = feat_cc.unsqueeze(1)
        if feat_mlo.dim() == 2:
            feat_mlo = feat_mlo.unsqueeze(1)
            
        # CC atiende a MLO como clave y valor
        attn_cc, _ = self.mha_cc_to_mlo(query=feat_cc, key=feat_mlo, value=feat_mlo)
        out_cc = self.norm_cc(feat_cc + attn_cc)
        
        # MLO atiende a CC como clave y valor
        attn_mlo, _ = self.mha_mlo_to_cc(query=feat_mlo, key=feat_cc, value=feat_cc)
        out_mlo = self.norm_mlo(feat_mlo + attn_mlo)
        
        # Pool global promedio si seqlen > 1
        pool_cc = out_cc.mean(dim=1)
        pool_mlo = out_mlo.mean(dim=1)
        
        # Fusión concatenada
        fused = torch.cat([pool_cc, pool_mlo], dim=-1)
        logit = self.fc_fusion(fused)
        return logit, fused


class HanningWindowTiler:
    """
    Pipeline de corte en mosaicos (tiling) con solapamiento y reconstrucción ponderada mediante
    ventana 2D de Hanning para gigapíxeles histopatológicos (HuBMAP) y mamografía de alta resolución.
    Elimina artefactos y costuras en los bordes de recombinación.
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    def __init__(self, tile_size: int = 512, stride: int = 384):
        self.tile_size = tile_size
        self.stride = stride
        self.overlap = tile_size - stride
        self.window = self._create_2d_hanning_window(tile_size, tile_size)

    def _create_2d_hanning_window(self, h: int, w: int) -> np.ndarray:
        win_h = np.hanning(h)
        win_w = np.hanning(w)
        window = np.outer(win_h, win_w)
        # Evitar ceros exactos en esquinas
        return np.maximum(window, 1e-4)

    def extract_tiles(self, image: np.ndarray) -> List[Tuple[int, int, np.ndarray]]:
        """
        Corta una imagen 2D o 3D (H, W, C) en mosaicos con su coordenada (y, x).
        """
        h, w = image.shape[:2]
        tiles = []
        
        y = 0
        while y < h:
            y_end = min(y + self.tile_size, h)
            y_start = max(0, y_end - self.tile_size)
            
            x = 0
            while x < w:
                x_end = min(x + self.tile_size, w)
                x_start = max(0, x_end - self.tile_size)
                
                tile = image[y_start:y_end, x_start:x_end]
                tiles.append((y_start, x_start, tile))
                
                if x_end == w:
                    break
                x += self.stride
                
            if y_end == h:
                break
            y += self.stride
            
        return tiles

    def reconstruct_from_tiles(
        self,
        tiles: List[Tuple[int, int, np.ndarray]],
        target_shape: Tuple[int, ...]
    ) -> np.ndarray:
        """
        Reconstruye la predicción continua aplicando ponderación por ventana de Hanning.
        """
        canvas = np.zeros(target_shape, dtype=np.float32)
        weight_sum = np.zeros(target_shape[:2], dtype=np.float32)
        
        is_multichannel = len(target_shape) > 2
        
        for y, x, tile in tiles:
            h, w = tile.shape[:2]
            win = self.window[:h, :w]
            
            if is_multichannel:
                expanded_win = np.expand_dims(win, axis=-1)
                canvas[y:y+h, x:x+w] += tile * expanded_win
            else:
                canvas[y:y+h, x:x+w] += tile * win
                
            weight_sum[y:y+h, x:x+w] += win
            
        # Normalizar por suma de pesos
        weight_sum = np.maximum(weight_sum, 1e-7)
        if is_multichannel:
            weight_sum = np.expand_dims(weight_sum, axis=-1)
            
        return canvas / weight_sum


class UglyDucklingPatientNormalizer:
    """
    Normalización dermatológica basada en la heurística del 'Patito Feo' (ISIC Melanoma).
    Contrasta las características de una lesión sospechosa contra el perfil basal de la piel del paciente.
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    @staticmethod
    def normalize_lesions(
        patient_features: np.ndarray,
        eps: float = 1e-6
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        patient_features: Matriz [N_lesiones, N_features] para un paciente específico.
        Devuelve:
          (delta_matrix, ratio_matrix)
          delta_matrix: x_i - median_patient
          ratio_matrix: x_i / (median_patient + eps)
        """
        median_vec = np.median(patient_features, axis=0)
        q75 = np.percentile(patient_features, 75, axis=0)
        q25 = np.percentile(patient_features, 25, axis=0)
        iqr = np.maximum(q75 - q25, eps)
        
        delta = (patient_features - median_vec) / iqr
        ratio = patient_features / np.maximum(median_vec, eps)
        return delta, ratio
