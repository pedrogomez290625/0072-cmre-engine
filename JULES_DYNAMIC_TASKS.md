# 📋 JULES DYNAMIC SUPER-TASKS BACKLOG (MOTOR GENERAL AGNÓSTICO)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE v0.6.0)
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI
**Fuente de Verdad de Torneos:** [`ACTIVE_COMPETITIONS.json`](file:///C:/Users/rafae/.gemini/01_PROYECTOS/0072-cmre-engine/ACTIVE_COMPETITIONS.json)

---

## 🎯 PRÓXIMAS SUPER-TAREAS AUTÓNOMAS DE ARQUITECTURA GENERAL:

1. **SUPER-TAREA CMRE-02: DICOM & High-Dimension Batch Pipeline con Multi-threading & Float32 Rescaling**
   - Extender `src/cmre/modules/ingest.py` con `batch_process_dicoms` y procesadores de tensores de alta dimensión utilizando `concurrent.futures.ThreadPoolExecutor`.
   - Validación de metadatos de rescale (Slope e Intercept) para normalización lineal precisa en `float32`.
   - Tests unitarios con arrays sintéticos asegurando tolerancia a archivos corruptos.

2. **SUPER-TAREA CMRE-03: Purged Group Disjoint Time-Series & Multi-Center Cross-Validation**
   - Añadir en `src/cmre/modules/split.py` un validador que combine restricción de grupos (pacientes/sensores/centros) con purga de ventanas temporales (gap/embargo).
   - Validar matemáticamente que ningún grupo ni timestamp solapado exista simultáneamente en train y val (zero leakage).

3. **SUPER-TAREA CMRE-04: Hierarchical Bayesian OOF Target Encoder con M-Estimate**
   - Extender `src/cmre/modules/signal.py` permitiendo codificación de objetivos en múltiples niveles jerárquicos anidados (ej: paciente -> estudio -> región).
   - Cálculo de varianza posterior para regularización Bayesiana estricta out-of-fold.

4. **SUPER-TAREA CMRE-05: Tanimoto Popcount Kernel HPC con SIMD Fallback**
   - Enriquecer `src/cmre/modules/hpc.py` con un kernel de similitud de Tanimoto vectorizado para matrices de bitsets de alta dimensión (ej: huellas moleculares ECFP4/Morgan o bitmasks).
   - Benchmark de rendimiento y cobertura de pruebas al 100%.

5. **SUPER-TAREA CMRE-06: Lector Dinámico de Competencias Activas (`ACTIVE_COMPETITIONS.json`)**
   - Integrar en `src/cmre/services/problem_profiler.py` una función `load_active_competitions()` que lea `ACTIVE_COMPETITIONS.json` y genere automáticamente el `ProblemDNA` y el plan de 6 fases para cualquier competencia listada en el registro.
   - Test: `tests/test_active_competitions_loader.py`.

6. **SUPER-TAREA CMRE-07: Adaptador Multimodal Cruzado para RSNA-Knee y CASMI**
   - Crear en `src/cmre/connectors/multimodal_adapter.py` un pipeline unificado que acepte tanto "image_2.5d_mri" como "msms_peak_spectra" fusionando un embedding vision-encoder con un Graph Neural Network.
   - Mitigación del timeout (visto en postmortems) empleando `LatencyBudgetPruner`.

7. **SUPER-TAREA CMRE-08: Manejo Robusto de Out-Of-Memory con Checkpoints Dinámicos**
   - Desarrollar un "OOM-Guard" en `src/cmre/services/oom_guard.py` que intercepte errores CUDA RuntimeError y conmute dinámicamente el batch-size y retome del último checkpoint.
   - Esto evita la pérdida de corridas críticas en competencias como ARC-AGI-2 y CASMI.

8. **SUPER-TAREA CMRE-09: Auto-Ajuste de Hiperparámetros Basado en Post-Mortems**
   - Integrar una fase de "Auto-Tune" que lea `data/knowledge/postmortems_failures_catalog.json` e inyecte la heurística necesaria para optimización contínua de umbrales Nelder-Mead sobre pF1 y métricas macro ROC-AUC.
   - Tests en `tests/test_autotune_heuristics.py`.

---
[VINCIT_OMNIA_VERITAS]  
Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
