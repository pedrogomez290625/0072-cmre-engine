# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Sesión Final de Cierre y Benchmarking (2 de Octubre 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa") & Victoria Perez

Este archivo es reescrito por el motor tras el análisis de `ACTIVE_COMPETITIONS.json` y el `data/knowledge/postmortems_failures_catalog.json`. Su objetivo es proyectar las mitigaciones a las vulnerabilidades encontradas y potenciar los solvers de las competencias activas (RSNA Knee, CASMI, ARC-AGI).

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-31: Optimizador de Latencia Adaptativa Multimodelo (Adaptive Latency Pruner)
- **Origen:** Postmortem `FAIL_12` y competencia `0075-rsna-knee-detection` con presupuestos estrictos de latencia de inferencia (1.5s / muestra).
- **Problema:** Ensamble multimodelo ciego explota los límites de tiempo de inferencia (timeout risks) en test, sin lograr maximizar la ganancia marginal del ROC-AUC.
- **Implementación:** Mejorar `LatencyBudgetPruner` en `MOD_ENSEMBLE` usando un optimizador greedy que seleccione los pesos del ensamblaje iterativamente penalizando marginalmente la latencia para ajustarse a los 1.5s indicados en el perfil de competencia, integrando fallback para un único modelo especialista en caso de que un fold tarde demasiado.
- **Verificación:** `tests/test_adaptive_latency_pruner.py`.

### [ ] SUPER-TAREA CMRE-32: Filtro Biofísico Mejorado para Decoys CASMI (Neutral Loss Checker)
- **Origen:** Postmortem `FAIL_14` y competencia `0074-enveda-casmi2026`.
- **Problema:** La búsqueda exhaustiva de moléculas introduce excesivos decoys. La validación con Tanimoto aislada no es suficiente porque ignora principios de fragmentación biofísica.
- **Implementación:** Ampliar `EnvedaCasmiSolver` o introducir en `MOD_SIGNAL` un "Neutral Loss Checker" que descarte o penalice severamente predicciones que no satisfagan los axiomas de presencia de heterotómos requeridos en la fragmentación observada (e.g. presencia obligatoria de N si se reporta pérdida neutra de NH3).
- **Verificación:** `tests/test_neutral_loss_checker.py`.

### [ ] SUPER-TAREA CMRE-33: Arquitectura Híbrida TTT D8 + Self-Attention para ARC-AGI
- **Origen:** Competencia `0076-arc-prize-2026` y Postmortem `FAIL_11`.
- **Problema:** La generalización zero-shot en ARC falla en patrones relacionales remotos.
- **Implementación:** Añadir `SelfAttentionGridTransformer` a la búsqueda simbólica de `ArcAgiHybridSolver`. Enlazar este Transformer tras la fase TTT con aumentaciones D8 para construir secuencias con pesos sobre sub-parches de 3x3 de la grilla 2D.
- **Verificación:** `tests/test_arc_self_attention_guard.py`.

### [ ] SUPER-TAREA CMRE-34: Sanitizador de Precisión Numérica Inter-Modulo (FP16/FP64)
- **Origen:** Postmortem `FAIL_13` (Error de `Half vs Double` en T4).
- **Problema:** Errores de RuntimeError al usar constantes calculadas en Float64 con Numpy pasadas inadvertidamente a tensores de red en Half (FP16).
- **Implementación:** Implementar un middleware robusto `FP16PrecisionSanitizer` en `MOD_INGEST` y el núcleo `schemas.py` que envuelva y baje de precisión los valores de metadata normalizada justo antes de que entren al autocast de CUDA en los solvers radiológicos.
- **Verificación:** `tests/test_fp16_precision_sanitizer.py`.

### [ ] SUPER-TAREA CMRE-35: Ventana Cosenoidal (Hanning) WSI con Atención (Attention WSI Crop)
- **Origen:** Postmortem `FAIL_03` (Artefactos en el borde de mosaico de WSI).
- **Problema:** Recorte sin overlap ni suavizado afecta la métrica Dice Global en inferencia sobre parches gigantes de alta resolución.
- **Implementación:** Enlazar en `MOD_INGEST` un Tiler de mosaicos con una función de suavizado cosenoidal de Hanning para superposiciones, minimizando discontinuidades de bordes en el parcheado para `RSNAKneeSolver` y problemas morfológicos análogos.
- **Verificación:** `tests/test_attention_wsi_crop.py`.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa") & Victoria Perez
