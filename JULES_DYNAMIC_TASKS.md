# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-147: Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT
- **Origen:** `FAIL_01` (Catálogo de fallos)
- **Problema:** Modelos con ROC-AUC > 0.82 y buena convergencia en entrenamiento colapsaron a pF1 de 0.02 en validac...
- **Implementación:** Optimización simplex Nelder-Mead continua del umbral sobre predicciones OOF restringiendo recall mínimo.

### [ ] SUPER-TAREA CMRE-148: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS
- **Origen:** `FAIL_02` (Catálogo de fallos)
- **Problema:** Validación cruzada K-Fold aleatoria infló el score a 5.12 MAE. En la fase de test en vivo (Private L...
- **Implementación:** PurgedGroupTimeSeriesSplit con ventana de embargo de al menos 10 minutos entre pliegues de entrenamiento y test.

### [ ] SUPER-TAREA CMRE-149: Mitigación de EDGE_SEAM_BOUNDARY_DEGRADATION
- **Origen:** `FAIL_03` (Catálogo de fallos)
- **Problema:** Modelos con Dice de 0.88 en parches aislados de 512x512 colapsaron a 0.74 al evaluar la imagen gigap...
- **Implementación:** Corte con solapamiento del 25% y reconstrucción mediante ponderación separable con ventana 2D de Hanning.

### [ ] SUPER-TAREA CMRE-150: Mitigación de SCAFFOLD_ANALOG_MEMORIZATION_LEAK
- **Origen:** `FAIL_04` (Catálogo de fallos)
- **Problema:** Top-10 accuracy de 94.5% en validación aleatoria; colapso catastrófico a 28.2% al evaluar en el conj...
- **Implementación:** Particionado disjunto por esqueletos moleculares de Bemis-Murcko (BemisMurckoScaffoldSplit).

### [ ] SUPER-TAREA CMRE-151: Mitigación de PATIENT_IDENTITY_COHORT_LEAKAGE
- **Origen:** `FAIL_05` (Catálogo de fallos)
- **Problema:** ROC-AUC local de 0.945; caída a 0.812 pAUC en Private LB y fallo en detección de melanomas sutiles....
- **Implementación:** StratifiedGroupKFold agrupado estrictamente por patient_id combinado con la normalización de Patito Feo.

### [ ] SUPER-TAREA CMRE-152: Mitigación de TARGET_ENCODING_HIGH_CARDINALITY_LEAKAGE
- **Origen:** `FAIL_06` (Catálogo de fallos)
- **Problema:** Target encoding directo sobre pares de tarjetas y direcciones (card1 + addr1) infló el CV a 0.985, c...
- **Implementación:** Codificación bayesiana OOF estricta con regularización m-estimate de Dirichlet y adición de ruido gaussiano.

### [ ] SUPER-TAREA CMRE-153: Mitigación de UNSCALED_COUNT_FEATURE_LEAKAGE_AND_CONSTANT_SHIFT
- **Origen:** `FAIL_07` (Catálogo de fallos)
- **Problema:** El conteo directo de ceros por fila mejoró drásticamente el Public LB (0.52 RMSLE), pero cayó más de...
- **Implementación:** Cálculo de desvíos relativos (Delta Trick) y normalización robusta intercuartílica (IQR).

### [ ] SUPER-TAREA CMRE-154: Mitigación de LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION
- **Origen:** `FAIL_08` (Catálogo de fallos)
- **Problema:** Modelos complejos (EfficientNet-B5) alcanzaron 99% accuracy en train con Cross-Entropy, pero la vali...
- **Implementación:** Uso de Label Smoothing, Bi-Tempered Loss o Soft-F1 con gradientes amortiguados para mitigar la penalización de outliers.

### [ ] SUPER-TAREA CMRE-155: Mitigación de NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE
- **Origen:** `FAIL_09` (Catálogo de fallos)
- **Problema:** Regresión lineal ordinaria (OLS) sobre las predicciones de 15 modelos de Gradient Boosting asignó co...
- **Implementación:** Mínimos Cuadrados No Negativos (Non-Negative Least Squares / NNLS) forzando w_i >= 0 y suma(w) = 1.0.

### [ ] SUPER-TAREA CMRE-156: Mitigación de INVERSION_MONOCHROME_LUT_MISINTERPRETATION
- **Origen:** `FAIL_10` (Catálogo de fallos)
- **Problema:** Pipelines basados en OpenCV/PIL estándar leyeron mamografías DICOM sin interpretar la etiqueta Photo...
- **Implementación:** Decodificador DICOM canónico con verificación obligatoria de PhotometricInterpretation y normalización a MONOCHROME2.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
