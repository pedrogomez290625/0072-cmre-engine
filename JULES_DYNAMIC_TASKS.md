# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 5 nuevas super-tareas agnósticas (CMRE-113 a CMRE-117) para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-113: Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT
- **Origen:** `FAIL_01` (Catálogo de fallos).
- **Problema:** Desalineación de métricas de negocio con Cross-Entropy resultando en un Recall deficiente debido a umbrales de decisión no óptimos (0.50).
- **Implementación:** Implementar `NelderMeadThresholdOptimizer` en `MOD_ENSEMBLE` para realizar optimización continua del umbral sobre predicciones OOF, restringiendo o maximizando la métrica de forma dinámica.

### [ ] SUPER-TAREA CMRE-114: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS
- **Origen:** `FAIL_02` (Catálogo de fallos).
- **Problema:** Sesgo de auto-correlación (lookahead) cuando variables futuras se filtran en particiones temporales cercanas.
- **Implementación:** Implementar `PurgedGroupTimeSeriesSplit` con ventana de embargo para garantizar una separación de al menos 10 minutos (o unidades correspondientes) entre pliegues de entrenamiento y test temporal.

### [ ] SUPER-TAREA CMRE-115: Mitigación de EDGE_SEAM_BOUNDARY_DEGRADATION
- **Origen:** `FAIL_03` (Catálogo de fallos).
- **Problema:** Degradación severa en los bordes de predicción debido a costuras visibles en mosaicos de imágenes de alta resolución (WSI).
- **Implementación:** Implementar `HanningWindowTiler2D` en `MOD_INGEST`, realizando corte con solapamiento del 25% y reconstrucción mediante ponderación separable con ventana 2D de Hanning.

### [ ] SUPER-TAREA CMRE-116: Mitigación de CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH
- **Origen:** `FAIL_13` (Catálogo de fallos).
- **Problema:** Abortos en tiempo de ejecución (CUDA RuntimeError) causados por interacciones implícitas entre `torch.autocast` (Half) y matrices/tensores provenientes de numpy originados como Double (float64).
- **Implementación:** Implementar `FP16PrecisionSanitizer` que fuerce de manera explícita la conversión a `.float()` de todas las variables de normalización y buffers, antes de cualquier cast a `.half()`.

### [ ] SUPER-TAREA CMRE-117: Mitigación de NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE
- **Origen:** `FAIL_09` (Catálogo de fallos).
- **Problema:** Regresión lineal ordinaria (OLS) sobre las predicciones de modelos de Gradient Boosting asignó coeficientes fuertemente negativos a modelos colineales, generando probabilidades negativas y Log-Loss infinito en test.
- **Implementación:** Implementar `NonNegativeLeastSquaresBlender` en `MOD_ENSEMBLE` forzando mínimos cuadrados no negativos (NNLS) de manera que w_i >= 0 y suma(w) = 1.0.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
