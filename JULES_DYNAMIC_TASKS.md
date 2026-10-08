# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Sesión de Cierre y Planificación Agnóstica (7 de Octubre 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito dinámicamente tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 6 nuevas super-tareas agnósticas (CMRE-61 a CMRE-66) para abordar los desafíos más urgentes en AGI discreto, Visión Médica y Metabolómica.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-61: Guardián Estricto Anti-Identidad y TTT D8 (ARC-AGI)
- **Origen:** `FAIL_11` (`SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE`) & `ACTIVE_COMPETITIONS.json` (`anti_identity_collapse`).
- **Problema:** En ARC-AGI, los fallbacks simbólicos que devuelven grillas idénticas a la entrada garantizan un score de 0.00.
- **Implementación:** Construir en `src/cmre/services/submission_validator_arc.py` y `MOD_OOD` un sistema que rechace sumisiones idénticas a la entrada, forzando Test-Time Training (TTT) con aumentaciones $D_8$ (rotaciones/reflexiones) y transformaciones cromáticas seguras.

### [ ] SUPER-TAREA CMRE-62: Podador de Ensamble por Presupuesto de Latencia (RSNA)
- **Origen:** `FAIL_12` (`UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION`) & `ACTIVE_COMPETITIONS.json` (`kaggle_timeout_risk`).
- **Problema:** En competiciones con severas restricciones de inferencia, la concatenación ciega de modelos causa timeout.
- **Implementación:** Desarrollar en `MOD_ENSEMBLE` un `LatencyBudgetPruner` que pode modelos densos mediante un enfoque greedy basado en ganancia marginal de AUC vs tiempo, reduciendo el tiempo de inferencia total al presupuesto de la competencia.

### [ ] SUPER-TAREA CMRE-63: Sanitizador Universal de Precisión FP16/FP64 (CUDA)
- **Origen:** `FAIL_13` (`CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH`).
- **Problema:** Constantes Float64 heredadas en operaciones de normalización rompen los kernels de PyTorch en FP16 (`expected scalar type Half but found Double`), fallando silenciosamente.
- **Implementación:** Crear en `MOD_HPC` un decorador y utilidad `sanitize_tensor_dtypes` que garantice la conversión de buffers de NumPy a Float32 antes de entrar al autocast `.half()`.

### [ ] SUPER-TAREA CMRE-64: Axioma de Ausencia SIRIUS para Metabolómica (CASMI)
- **Origen:** `FAIL_14` (`UNCONSTRAINED_CANDIDATE_DECOY_OVERLOAD`) & `ACTIVE_COMPETITIONS.json` (`high_dimensional_decoys`).
- **Problema:** El filtrado masivo basado en masa retiene miles de candidatos "decoy" irreales que carecen de los heteroátomos mínimos (N, O) requeridos para las pérdidas neutras espectrales.
- **Implementación:** Integrar en `MOD_OOD` o en `MOD_INGEST` un filtro rígido biofísico ("Axioma de Ausencia SIRIUS") que evalúe si la estructura molecular de un candidato permite las pérdidas documentadas en el espectro MS/MS.

### [ ] SUPER-TAREA CMRE-65: Asymmetric Matrix Blending para Visión Multi-Vista
- **Origen:** Análisis de RSNA Knee y `severe_class_imbalance`.
- **Problema:** Las vistas médicas (Sagital, Coronal, Axial) no tienen el mismo poder predictivo para todas las clases; un promedio simple pierde las señales específicas de vista.
- **Implementación:** Refinar en `MOD_ENSEMBLE` una estrategia de `AsymmetricMatrixBlending` donde el ensamble aprende pesos matriciales por cada par (clase, vista) optimizando el Macro ROC-AUC.

### [ ] SUPER-TAREA CMRE-66: Meta-Optimización de Fronteras Ordinales de Nelder-Mead
- **Origen:** Postmortems históricos de clasificación ordinal sin mención en los últimos 5 pero vitales para métricas pAUC y QWK.
- **Problema:** Fronteras de decisión uniformes en predicciones continuas para targets ordinales no optimizan la distribución del dataset.
- **Implementación:** Desarrollar un ajustador estricto (`NelderMeadThresholdOptimizer`) que converja rápido calibrando puntos de corte ordinales no uniformes desde predicciones en coma flotante.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
