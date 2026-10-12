# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Cierre de Sesión y Proyección Auto-Evolutiva (12 de Octubre de 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 6 nuevas super-tareas agnósticas (CMRE-85 a CMRE-90) para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-85: Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT
- **Origen:** `FAIL_01` y catálogo de fallos.
- **Problema:** Umbrales fijos colapsan debido a la discrepancia entre BCE Loss y métricas de Kaggle (pAUC/QWK).
- **Implementación:** Implementar `NelderMeadThresholdOptimizer` dinámico.

### [ ] SUPER-TAREA CMRE-86: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS
- **Origen:** `FAIL_02` y catálogo de fallos.
- **Problema:** Fuga temporal inversa infló AUC en CV a 0.94 pero colapsó en test.
- **Implementación:** Implementar validación cruzada con `PurgedTimeSeriesSplit` y embargo estricto.

### [ ] SUPER-TAREA CMRE-87: Mitigación de PATIENT_IDENTITY_COHORT_LEAKAGE
- **Origen:** `FAIL_05` y catálogo de fallos.
- **Problema:** Múltiples metástasis del mismo paciente distribuidas en train y validación engañan al modelo para memorizar identidad genética, cayendo severamente en evaluación.
- **Implementación:** Forzar agrupación estricta por `patient_id` usando iteradores `GroupKFold` desacoplados.

### [ ] SUPER-TAREA CMRE-88: Mitigación de UNSCALED_COUNT_FEATURE_LEAKAGE_AND_CONSTANT_SHIFT
- **Origen:** `FAIL_07` y catálogo de fallos.
- **Problema:** Sobreajuste a matriz de dispersión pública usando conteo directo, colapsando en el leaderboard privado.
- **Implementación:** Integrar cálculo de desvíos relativos (Delta Trick) y normalización robusta intercuartílica (IQR).

### [ ] SUPER-TAREA CMRE-89: Mitigación de SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE
- **Origen:** `FAIL_11` y catálogo de fallos.
- **Problema:** Fallback ciego devolviendo entrada de grilla tras timeout en ARC-AGI provocando un fallo total de identidad.
- **Implementación:** Guardián anti-identidad que exige mutación cromática/topológica garantizada o Test-Time Training (TTT) D8.

### [ ] SUPER-TAREA CMRE-90: Mitigación de UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION
- **Origen:** `FAIL_12` y catálogo de fallos.
- **Problema:** Sobre-ingeniería y ensamblado ciego de >30 redes provocando timeout de latencia en Kaggle.
- **Implementación:** Desarrollar `LatencyBudgetPruner` para podado dinámico y balance latencia/AUC dentro del presupuesto de tiempo especificado en `ACTIVE_COMPETITIONS.json`.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
