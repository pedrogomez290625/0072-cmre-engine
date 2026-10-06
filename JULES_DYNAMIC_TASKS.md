# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Sesión de Desarrollo Agnóstico (6 de Octubre 2026) - Auto-Reescritura Avanzada
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo es reescrito por el motor tras el análisis de `ACTIVE_COMPETITIONS.json` y el `data/knowledge/postmortems_failures_catalog.json`. Su objetivo es proyectar las mitigaciones a las vulnerabilidades encontradas y potenciar los solvers de las competencias activas (RSNA Knee, CASMI, ARC-AGI).

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-51: Optimizador Nelder-Mead de Umbrales Multiclase (Extremo Desbalance)
- **Origen:** `ACTIVE_COMPETITIONS.json` (RSNA Knee 2026 - severe_class_imbalance) & `FAIL_01` (Threshold Collapse and Metric Disalignment).
- **Problema:** Usar un umbral de 0.5 por defecto colapsa métricas en clases raras (<5% de prevalencia). Los modelos pueden obtener AUC alto pero fallar en el private LB de Kaggle al momento de la binarización de decisión.
- **Implementación:** Construir en `MOD_ENSEMBLE` un Optimizador Nelder-Mead multiclase, que tome las predicciones out-of-fold y calibre cada clase independientemente (o macro-promediada) para optimizar el F1-score sin penalizar masivamente los falsos positivos.

### [ ] SUPER-TAREA CMRE-52: Sanitizador Universal de Precisiones (FP16/FP64)
- **Origen:** `FAIL_13` (CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH).
- **Problema:** En el paso de tensores o constantes de pre-procesamiento desde NumPy (Float64) a PyTorch con Autocast (FP16) para inferencia acelerada en Kaggle, existen fallos en tiempo de ejecución (Double vs Half) abortando CUDA silenciosamente.
- **Implementación:** Implementar un guardián de tipos y casting `PrecisionSanitizer` en `MOD_HPC` o `MOD_INGEST` que analice recursivamente cada tensor dentro del `ProblemDNA` antes de pasarlo al backbone, realizando un casting explícito a `.float()` y luego a `.half()` bajo autocast.

### [ ] SUPER-TAREA CMRE-53: Arquitectura Híbrida de Enrutamiento para Latencia Estricta (Dynamic Budget Pruner V2)
- **Origen:** `ACTIVE_COMPETITIONS.json` (RSNA Knee 2026 - kaggle_timeout_risk) & `FAIL_12` (UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION).
- **Problema:** Un pipeline ensamblado masivo (>30 sub-redes) causó colapsos por exceder 9h en RSNA. El presupuesto actual es de 1.5s por muestra.
- **Implementación:** Mejorar el `LatencyBudgetPruner` en `MOD_ENSEMBLE`. Desarrollar un sistema de enrutamiento basado en costo: usar una pequeña red convolucional que en menos de 5ms determine si un estudio es "difícil" o "fácil". Si es fácil, ejecutar la red principal; si es difícil, ejecutar un bloque pesado (KneeSpecialist + CoAtNet) deteniendo otros componentes en paralelo.

### [ ] SUPER-TAREA CMRE-54: Generador de Señal Delta Relativo a Dispersión (Delta Trick)
- **Origen:** `FAIL_07` (UNSCALED_COUNT_FEATURE_LEAKAGE).
- **Problema:** Los metadatos tabulares a menudo contienen conteos absolutos que se sobreajustan a las distribuciones del public LB.
- **Implementación:** Implementar en `MOD_SIGNAL` un calculador de desvíos relativos e intercuartílicos robustos para toda columna numérica entrante, eliminando constantes crudas como conteo de ceros no relativizado por grupo.

### [ ] SUPER-TAREA CMRE-55: Purga Temporal y Embargo para Alineamiento Multimodal
- **Origen:** `FAIL_02` (TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS).
- **Problema:** K-Fold aleatorio en datos biomédicos longitudinales del mismo paciente filtra información futura hacia el pasado.
- **Implementación:** Extender `MOD_SPLIT` con un `PurgedGroupTimeSeriesSplit` robusto a modalidades 2.5D que garantice la desconexión estricta temporal (embargo period) entre los scans de base de datos del mismo paciente sin superposición en folds.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
