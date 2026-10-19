# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 5 nuevas super-tareas agnósticas (CMRE-123 a CMRE-127) para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-123: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS
- **Origen:** `FAIL_02` (Catálogo de fallos)
- **Problema:** Riesgo de fuga temporal al evaluar el modelo sobre datos correlacionados en series de tiempo.
- **Implementación:** Implementación de Purged Group Time Series Split con embargo riguroso.

### [ ] SUPER-TAREA CMRE-124: Mitigación de PATIENT_IDENTITY_COHORT_LEAKAGE
- **Origen:** `FAIL_05` (Catálogo de fallos) / Desafío Activo: RSNA Knee
- **Problema:** Filtración de identidad del paciente entre particiones provocando sobreajuste al ID.
- **Implementación:** Estrategia estricta de partición GroupKFold asegurando que un paciente solo exista en un fold.

### [ ] SUPER-TAREA CMRE-125: Mitigación de TARGET_ENCODING_HIGH_CARDINALITY_LEAKAGE
- **Origen:** `FAIL_06` (Catálogo de fallos) / Desafío Activo: Tabular Metadata
- **Problema:** Codificación directa de variables categóricas provocando colapso temporal en test.
- **Implementación:** Codificación bayesiana OOF estricta con regularización Dirichlet m-estimate.

### [ ] SUPER-TAREA CMRE-126: Mitigación de LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION
- **Origen:** `FAIL_08` (Catálogo de fallos) / Desafío Activo: Medical Label Noise
- **Problema:** Memorización del ruido en etiquetas médicas con Cross-Entropy.
- **Implementación:** Integración de Bi-Tempered Logistic Loss y Weighted Soft-F1 Loss.

### [ ] SUPER-TAREA CMRE-127: Mitigación de CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH
- **Origen:** `FAIL_13` (Catálogo de fallos) / Desafío Activo: hardware kaggle
- **Problema:** Colisión de tipos al usar normalización float64 de numpy con torch.autocast.
- **Implementación:** Sanitizador FP16 para garantizar compatibilidad CUDA y prevenir fallos silenciosos.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
