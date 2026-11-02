# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-232: Mitigación de LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION (FAIL_08)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_08)
- **Problema:** Modelos complejos alcanzaron 99% accuracy en train con Cross-Entropy, pero la validación se estancó por sobreajuste severo a etiquetas erróneas.
- **Causa Raíz:** Cross-Entropy pura penaliza exponencialmente las discrepancias, forzando a la red a memorizar el ruido.
- **Implementación:** Uso de Label Smoothing, Bi-Tempered Loss o Soft-F1 con gradientes amortiguados para mitigar la penalización de outliers.

### [ ] SUPER-TAREA CMRE-233: Mitigación de NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE (FAIL_09)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_09)
- **Problema:** Regresión lineal ordinaria sobre predicciones asignó coeficientes fuertemente negativos, generando Log-Loss infinito en test.
- **Causa Raíz:** Multicolinealidad severa entre modelos casi idénticos. OLS busca balancear diferencias asignando pesos gigantescos de signos opuestos.
- **Implementación:** Mínimos Cuadrados No Negativos (Non-Negative Least Squares / NNLS) forzando w_i >= 0 y suma(w) = 1.0.

### [ ] SUPER-TAREA CMRE-234: Mitigación de INVERSION_MONOCHROME_LUT_MISINTERPRETATION (FAIL_10)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_10)
- **Problema:** Pipelines leyeron mamografías DICOM sin interpretar PhotometricInterpretation, invirtiendo la apariencia de los tejidos.
- **Causa Raíz:** Al ignorar la metadata, las convoluciones aprendieron características con polaridad invertida en diferentes centros hospitalarios.
- **Implementación:** Decodificador DICOM canónico con verificación obligatoria de PhotometricInterpretation y normalización a MONOCHROME2.

### [ ] SUPER-TAREA CMRE-235: Mitigación de UNSCALED_COUNT_FEATURE_LEAKAGE_AND_CONSTANT_SHIFT (FAIL_07)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_07)
- **Problema:** El conteo directo de ceros mejoró el Public LB, pero cayó en Private LB al cambiar la densidad de dispersión.
- **Causa Raíz:** Sobreajuste a la matriz de dispersión sintética generada por el banco en el subconjunto público.
- **Implementación:** Cálculo de desvíos relativos (Delta Trick) y normalización robusta intercuartílica (IQR).

### [ ] SUPER-TAREA CMRE-236: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS (FAIL_05)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_05)
- **Problema:** Un modelo predictivo de series de tiempo financieras colapsó de Sharpe 2.4 OOF a Sharpe -1.2 en vivo.
- **Causa Raíz:** Fuga de autocorrelación temporal al normalizar Z-Score sobre ventanas temporales superpuestas (lookahead bias sutil).
- **Implementación:** Splitter de validación cruzada temporal estricto de series temporales (PurgedGroupTimeSeriesSplit).

### [ ] SUPER-TAREA CMRE-237: Mitigación de SINGLE_VIEW_EDGE_DEGRADATION_ARTEFACT (FAIL_02)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_02)
- **Problema:** El parcheado ciego (tiling) masivo en Whole Slide Images (WSI) sin contexto global provocó clasificaciones de alto riesgo en bordes benignos.
- **Causa Raíz:** Pérdida de topología tisular global al procesar tiles de 256x256 aislados.
- **Implementación:** Bimodal WSI Fusion con embeddings globales (DINOv2) y atención cruzada tile-to-slide.
