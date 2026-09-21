# 📋 JULES DYNAMIC SUPER-TASKS BACKLOG
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI

---

## 🎯 PRÓXIMAS SUPER-TAREAS AUTÓNOMAS PARA LA SIGUIENTE SESIÓN:

1. **SUPER-TAREA CMRE-01: Soft-F1 Loss Autograd PyTorch Module con Gradientes Analíticos**
   - Implementar un módulo formal `torch.nn.Module` para `SoftF1Loss` con soporte de batch multidimensional y pesos de clase asimétricos.
   - Añadir tests en `tests/test_modules.py` comparando las salidas numéricas y la coherencia del backpropagation con `torch.autograd.gradcheck`.
   - Firma: `Autor: Perez, Ernesto Rafael ("Rafa")`.

2. **SUPER-TAREA CMRE-02: DICOM Batch Pipeline con Multi-threading & Float32 Rescaling**
   - Extender `src/cmre/modules/ingest.py` con una función `batch_process_dicoms` que utilice `concurrent.futures.ThreadPoolExecutor`.
   - Incorporar validación de metadatos de rescale (Slope e Intercept) para normalización lineal precisa a unidades Hounsfield/densidad mamográfica.
   - Escribir tests unitarios con arrays sintéticos asegurando tolerancia a DICOMs corruptos.

3. **SUPER-TAREA CMRE-03: Purged Group Disjoint Time-Series Cross-Validation**
   - Añadir en `src/cmre/modules/split.py` un validador que combine restricción de grupos (pacientes/sensores) con purga de ventanas temporales (gap/embargo).
   - Validar matemáticamente que ningún grupo ni timestamp solapado exista simultáneamente en fold de entrenamiento y fold de validación (zero leakage).

4. **SUPER-TAREA CMRE-04: Hierarchical Bayesian OOF Target Encoder con M-Estimate**
   - Extender `src/cmre/modules/signal.py` permitiendo codificación de objetivos en múltiples niveles jerárquicos anidados (ej: paciente -> estudio -> mama -> proyección).
   - Añadir cálculo de varianza posterior para regularización Bayesiana estricta out-of-fold.

5. **SUPER-TAREA CMRE-05: Tanimoto Popcount Kernel HPC con SIMD Fallback**
   - Enriquecer `src/cmre/modules/hpc.py` con un kernel de similitud de Tanimoto vectorizado para matrices de bitsets de alta dimensión (ej: huellas moleculares ECFP4/Morgan).
   - Medir benchmark de rendimiento y asegurar cobertura de pruebas al 100%.

6. **SUPER-TAREA CMRE-06: Evaluador Automático de Torneos y Generador de Benchmarks**
   - Crear un CLI subcommand `cmre benchmark` que ejecute el planificador sobre los 7 datasets de ejemplo (`data/examples/`) y mida la latencia de inferencia y uso de memoria de los 6 módulos canónicos.
   - Generar un reporte comparativo sintético en `reports/cmre_benchmark_summary.md`.

---
[VINCIT_OMNIA_VERITAS]
