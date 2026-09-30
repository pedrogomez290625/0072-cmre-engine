# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Sesión Final de Cierre y Benchmarking (30 de Septiembre 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa") & Victoria Perez

Este archivo es reescrito por el motor tras el análisis de `ACTIVE_COMPETITIONS.json` y el `data/knowledge/postmortems_failures_catalog.json`. Su objetivo es proyectar las mitigaciones a las vulnerabilidades encontradas y potenciar los solvers de las competencias activas (RSNA Knee, CASMI, ARC-AGI).

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-16: Refactor Profiling Latency Budget
- **Origen:** Postmortem `FAIL_12` y presupuesto definido en `ACTIVE_COMPETITIONS.json` (Ej: RSNA Knee 1.5s).
- **Problema:** Ensamble lento en hardware estricto.
- **Implementación:** En `src/cmre/modules/ensemble.py`, el `LatencyBudgetPruner` debe perfilar estáticamente el FLOPs de cada modelo y ejecutar un Knapsack 0/1 para maximizar la diversidad (ROC-AUC) sin superar el budget `latency_budget_per_sample_sec`.
- **Verificación:** `tests/test_latency_knapsack_pruner.py`.

### [ ] SUPER-TAREA CMRE-17: Sistema Universal de Sanitización CUDA (FP16/FP32)
- **Origen:** Postmortem `FAIL_13`.
- **Problema:** Incompatibilidad silente de `float64` (Double) proveniente de diccionarios de normalización en operaciones autocast de torch.
- **Implementación:** Implementar un hook `sanitize_tensor_dtypes` en el pipeline de `MOD_INGEST` o un decorador en las capas inferenciales para castear automáticamente buffers NumPy/Dict a `float32` antes del paso a `half()`.
- **Verificación:** `tests/test_cuda_type_sanitizer.py`.

### [ ] SUPER-TAREA CMRE-18: Filtro Biofísico Molecular (SIRIUS v2)
- **Origen:** Postmortem `FAIL_14` y `ACTIVE_COMPETITIONS.json` (Enveda CASMI).
- **Problema:** Decoys de masa exacta en la búsqueda de lotes en bases de datos moleculares.
- **Implementación:** Refinar el `NeutralLossBiophysicsFilter` para no solo usar Oxígeno/Nitrógeno, sino también verificar penalizaciones de Ring Double Bond Equivalent (RDBE) si se sospecha de aromaticidad basada en la pérdida espectral.
- **Verificación:** `tests/test_biophysics_sirius_v2.py`.

### [ ] SUPER-TAREA CMRE-19: Extractor Automático de Fugas por Identidad
- **Origen:** Postmortem `FAIL_05` (Kaggle ISIC 2024).
- **Problema:** Fuga del paciente en la validación cruzada.
- **Implementación:** Crear en `src/cmre/modules/split.py` un `PatientIsolationValidator` que arroje `StrictLeakageException` si el hash de un identificador de paciente aparece tanto en train como en validación del mismo fold.
- **Verificación:** `tests/test_patient_isolation_validator.py`.

### [ ] SUPER-TAREA CMRE-20: Reconstrucción Hanning WSI
- **Origen:** Postmortem `FAIL_03` (HuBMAP Kidney WSI).
- **Problema:** Discontinuidades en inferencia gigapíxel.
- **Implementación:** Ampliar `MOD_INGEST` con `HanningWindowTiler` que aplique filtros paso-bajo espaciales en los bordes de los patches antes de ensamblarlos.
- **Verificación:** `tests/test_hanning_wsi.py`.

### [ ] SUPER-TAREA CMRE-21: Regresor NNLS Robusto (Simplex-Bound)
- **Origen:** Postmortem `FAIL_09` (Tabular Playground).
- **Problema:** Pesos negativos en ensambles correlacionados.
- **Implementación:** Robustecer `SimpleNNLSBlender` con una API Sklearn compatible y barreras explícitas de regularización L1 para forzar dispersión en los pesos positivos.
- **Verificación:** Refactor de `tests/test_nnls_blender.py`.

### [ ] SUPER-TAREA CMRE-22: MONOCHROME1 Dicom Normalizer Estricto
- **Origen:** Postmortem `FAIL_10` (RSNA Mammography).
- **Problema:** Inversión de tejidos (tejido tumoral negro).
- **Implementación:** Obligar en la carga de DICOMs de `MOD_INGEST` la lectura e inversión si `PhotometricInterpretation == 'MONOCHROME1'`, fallando la carga si el flag no existe en la cabecera.
- **Verificación:** `tests/test_dicom_monochrome_strict.py`.

### [ ] SUPER-TAREA CMRE-23: Sistema Dinámico de Agrupación Temporal (Purged Time Series)
- **Origen:** Postmortem `FAIL_06` (IEEE-CIS Fraud Detection).
- **Problema:** Fuga de variable objetivo en target encoding sin embargo temporal adecuado.
- **Implementación:** Introducir `PurgedGroupTimeSeriesSplit` en `src/cmre/modules/split.py` que aplique periodos de cuarentena (embargo) garantizando que variables bayesianas no filtren identidad futura.
- **Verificación:** `tests/test_purged_time_split.py`.

### [ ] SUPER-TAREA CMRE-24: Auto-Sanitizador de Pérdidas por Ruido de Etiqueta (Soft-F1/Bi-Tempered)
- **Origen:** Postmortem `FAIL_08` (Cassava Leaf Disease).
- **Problema:** Memorización de etiquetas erróneas y colapso de validación mediante Cross-Entropy estándar.
- **Implementación:** Escalar `SoftF1Loss` y agregar soporte a `BiTemperedLogisticLoss` en `src/cmre/modules/loss.py` como capas canónicas PyTorch que supriman las penalizaciones exponenciales en el extremo superior.
- **Verificación:** `tests/test_bitempered_softf1_noise.py`.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa") & Victoria Perez
