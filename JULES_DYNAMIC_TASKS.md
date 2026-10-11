# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Cierre de Sesión y Proyección Auto-Evolutiva (11 de October de 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 6 nuevas super-tareas agnósticas (CMRE-79 a CMRE-84) para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-79: Mitigación de EDGE_SEAM_BOUNDARY_DEGRADATION
- **Origen:** `FAIL_03` y catálogo de fallos.
- **Problema:** Modelos con Dice de 0.88 en parches aislados de 512x512 colapsaron a 0.74 al evaluar la imagen gigapíxel completa (Whole Slide Image de 50,000x50,000 px).
- **Implementación:** Corte con solapamiento del 25% y reconstrucción mediante ponderación separable con ventana 2D de Hanning.

### [ ] SUPER-TAREA CMRE-80: Mitigación de SCAFFOLD_ANALOG_MEMORIZATION_LEAK
- **Origen:** `FAIL_04` y catálogo de fallos.
- **Problema:** Top-10 accuracy de 94.5% en validación aleatoria; colapso catastrófico a 28.2% al evaluar en el conjunto ciego de prueba.
- **Implementación:** Particionado disjunto por esqueletos moleculares de Bemis-Murcko (BemisMurckoScaffoldSplit).

### [ ] SUPER-TAREA CMRE-81: Mitigación de TARGET_ENCODING_HIGH_CARDINALITY_LEAKAGE
- **Origen:** `FAIL_06` y catálogo de fallos.
- **Problema:** Target encoding directo sobre pares de tarjetas y direcciones (card1 + addr1) infló el CV a 0.985, colapsando a 0.880 en test temporal.
- **Implementación:** Codificación bayesiana OOF estricta con regularización m-estimate de Dirichlet y adición de ruido gaussiano.

### [ ] SUPER-TAREA CMRE-82: Mitigación de LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION
- **Origen:** `FAIL_08` y catálogo de fallos.
- **Problema:** Modelos complejos (EfficientNet-B5) alcanzaron 99% accuracy en train con Cross-Entropy, pero la validación se estancó en 87.5% por sobreajuste severo a etiquetas erróneas.
- **Implementación:** Uso de Label Smoothing, Bi-Tempered Loss o Soft-F1 con gradientes amortiguados para mitigar la penalización de outliers.

### [ ] SUPER-TAREA CMRE-83: Mitigación de NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE
- **Origen:** `FAIL_09` y catálogo de fallos.
- **Problema:** Regresión lineal ordinaria (OLS) sobre las predicciones de 15 modelos de Gradient Boosting asignó coeficientes fuertemente negativos (-3.8) a varios modelos colineales, generando probabilidades negativas y Log-Loss infinito en test.
- **Implementación:** Mínimos Cuadrados No Negativos (Non-Negative Least Squares / NNLS) forzando w_i >= 0 y suma(w) = 1.0.

### [ ] SUPER-TAREA CMRE-84: Mitigación de INVERSION_MONOCHROME_LUT_MISINTERPRETATION
- **Origen:** `FAIL_10` y catálogo de fallos.
- **Problema:** Pipelines basados en OpenCV/PIL estándar leyeron mamografías DICOM sin interpretar la etiqueta PhotometricInterpretation, invirtiendo la apariencia de los tejidos (grasa blanca, tejido tumoral negro) en el 30% del dataset.
- **Implementación:** Decodificador DICOM canónico con verificación obligatoria de PhotometricInterpretation y normalización a MONOCHROME2.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
