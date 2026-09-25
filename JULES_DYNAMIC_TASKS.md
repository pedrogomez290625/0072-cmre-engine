# 📋 JULES DYNAMIC SUPER-TASKS BACKLOG (MOTOR GENERAL AGNÓSTICO)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE v0.5.0)
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI
**Fuente de Verdad de Torneos:** [`ACTIVE_COMPETITIONS.json`](file:///C:/Users/rafae/.gemini/01_PROYECTOS/0072-cmre-engine/ACTIVE_COMPETITIONS.json)

---

## 🎯 PRÓXIMAS SUPER-TAREAS AUTÓNOMAS DE ARQUITECTURA GENERAL:

1. **SUPER-TAREA CMRE-01: Soft-F1 / Dice Loss Autograd PyTorch Module con Gradientes Analíticos**
   - Implementar un módulo formal `torch.nn.Module` para pérdidas asimétricas diferenciables con soporte de batch multidimensional y pesos de clase dinámicos.
   - Tests en `tests/test_modules.py` comparando las salidas numéricas con `torch.autograd.gradcheck`.
   - Firma: `Autor: Perez, Ernesto Rafael ("Rafa")`.

2. **SUPER-TAREA CMRE-02: DICOM & High-Dimension Batch Pipeline con Multi-threading & Float32 Rescaling**
   - Extender `src/cmre/modules/ingest.py` con `batch_process_dicoms` y procesadores de tensores de alta dimensión utilizando `concurrent.futures.ThreadPoolExecutor`.
   - Validación de metadatos de rescale (Slope e Intercept) para normalización lineal precisa en `float32`.
   - Tests unitarios con arrays sintéticos asegurando tolerancia a archivos corruptos.

3. **SUPER-TAREA CMRE-03: Purged Group Disjoint Time-Series & Multi-Center Cross-Validation**
   - Añadir en `src/cmre/modules/split.py` un validador que combine restricción de grupos (pacientes/sensores/centros) con purga de ventanas temporales (gap/embargo).
   - Validar matemáticamente que ningún grupo ni timestamp solapado exista simultáneamente en train y val (zero leakage).

4. **SUPER-TAREA CMRE-04: Hierarchical Bayesian OOF Target Encoder con M-Estimate**
   - Extender `src/cmre/modules/signal.py` permitiendo codificación de objetivos en múltiples niveles jerárquicos anidados (ej: paciente -> estudio -> región).
   - Cálculo de varianza posterior para regularización Bayesiana estricta out-of-fold.

5. **SUPER-TAREA CMRE-05: Tanimoto Popcount Kernel HPC con SIMD Fallback**
   - Enriquecer `src/cmre/modules/hpc.py` con un kernel de similitud de Tanimoto vectorizado para matrices de bitsets de alta dimensión (ej: huellas moleculares ECFP4/Morgan o bitmasks).
   - Benchmark de rendimiento y cobertura de pruebas al 100%.

6. **SUPER-TAREA CMRE-06: Lector Dinámico de Competencias Activas (`ACTIVE_COMPETITIONS.json`)**
   - Integrar en `src/cmre/services/problem_profiler.py` una función `load_active_competitions()` que lea `ACTIVE_COMPETITIONS.json` y genere automáticamente el `ProblemDNA` y el plan de 6 fases para cualquier competencia listada en el registro.
   - Test: `tests/test_active_competitions_loader.py`.

7. **SUPER-TAREA CMRE-07: Scraper & Parser de Discusiones y Soluciones Ganadoras (Kaggle/DrivenData)**
   - Desarrollar `src/cmre/connectors/kaggle_writeups.py` para parsear hilos ganadores y registrar automáticamente Claims científicos en `data/knowledge/claims_cmre.json`.
   - Test unitario con mocks en `tests/test_kaggle_writeups.py`.

8. **SUPER-TAREA CMRE-08: Evaluador Automático de Torneos y Generador de Benchmarks**
   - Crear un CLI subcommand `cmre benchmark` que ejecute el planificador sobre los datasets y competiciones de `ACTIVE_COMPETITIONS.json` y mida latencia de inferencia y uso de memoria.
   - Generar reporte comparativo sintético en `reports/cmre_benchmark_summary.md`.

---
[VINCIT_OMNIA_VERITAS]  
Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
