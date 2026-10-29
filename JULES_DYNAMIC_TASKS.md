# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-207: Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT (FAIL_01)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_01)
- **Problema:** Modelos con ROC-AUC > 0.82 y buena convergencia en entrenamiento colapsaron a pF1 de 0.02 en validación y test por evaluar con un umbral fijo estándar (0.50). Caída de más de 600 puestos en el Private Leaderboard para equipos que no optimizaron el umbral.
- **Causa Raíz:** La métrica pF1 sobre una prevalencia mamográfica extrema (~2.1% positiva) es hipersensible al umbral de binarización. Con umbral 0.50, la precisión y recall colapsan por inhibición de predicciones positivas. El umbral óptimo residía entre [0.03, 0.08].
- **Implementación:** Optimización simplex Nelder-Mead continua del umbral sobre predicciones OOF restringiendo recall mínimo.

### [ ] SUPER-TAREA CMRE-208: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS (FAIL_02)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_02)
- **Problema:** Validación cruzada K-Fold aleatoria infló el score a 5.12 MAE. En la fase de test en vivo (Private LB) el score se degradó a 5.89 MAE, provocando caídas de más de 800 puestos.
- **Causa Raíz:** Autocorrelación intradiaria de alta frecuencia en el libro de órdenes (order book). Muestras contiguas en el tiempo compartían micro-tendencias y volatilidad. Un split aleatorio filtró información del futuro inmediato hacia el pasado.
- **Implementación:** PurgedGroupTimeSeriesSplit con ventana de embargo de al menos 10 minutos entre pliegues de entrenamiento y test.

### [ ] SUPER-TAREA CMRE-209: Mitigación de PATIENT_IDENTITY_COHORT_LEAKAGE (FAIL_05)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_05)
- **Problema:** ROC-AUC local de 0.945; caída a 0.812 pAUC en Private LB y fallo en detección de melanomas sutiles.
- **Causa Raíz:** Los pacientes tenían múltiples lesiones cutáneas. Al no aislar el paciente en un único pliegue, las redes aprendieron a reconocer el tipo de piel y fondo del paciente en lugar de la atipia celular de la lesión.
- **Implementación:** StratifiedGroupKFold agrupado estrictamente por patient_id combinado con la normalización de Patito Feo.

### [ ] SUPER-TAREA CMRE-210: Mitigación de LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION (FAIL_08)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_08)
- **Problema:** Modelos complejos (EfficientNet-B5) alcanzaron 99% accuracy en train con Cross-Entropy, pero la validación se estancó en 87.5% por sobreajuste severo a etiquetas erróneas.
- **Causa Raíz:** El dataset contenía entre 15% y 20% de ruido en las etiquetas debido a diagnósticos de campo en hojas de yuca sin confirmación de laboratorio. Cross-Entropy penaliza exponencialmente las discrepancias, forzando a la red a memorizar el ruido.
- **Implementación:** Uso de Label Smoothing, Bi-Tempered Loss o Soft-F1 con gradientes amortiguados para mitigar la penalización de outliers.

### [ ] SUPER-TAREA CMRE-211: Mitigación de NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE (FAIL_09)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_09)
- **Problema:** Regresión lineal ordinaria (OLS) sobre las predicciones de 15 modelos de Gradient Boosting asignó coeficientes fuertemente negativos (-3.8) a varios modelos colineales, generando probabilidades negativas y Log-Loss infinito en test.
- **Causa Raíz:** Multicolinealidad severa entre modelos casi idénticos (LightGBM vs XGBoost con semillas distintas). OLS busca balancear diferencias infinitesimales asignando pesos gigantescos de signos opuestos.
- **Implementación:** Mínimos Cuadrados No Negativos (Non-Negative Least Squares / NNLS) forzando w_i >= 0 y suma(w) = 1.0.

### [ ] SUPER-TAREA CMRE-212: Mitigación de CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH (FAIL_13)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_13)
- **Problema:** Al ejecutar inferencia en Kaggle GPU (Tesla T4) con torch.autocast, el kernel falló con RuntimeError: expected scalar type Half but found Double.
- **Causa Raíz:** Constantes de normalización ImageNet (mean/std) importadas como float64 (Double) en NumPy o PyTorch. Al interactuar con capas Half sin conversión explícita, CUDA aborta la ejecución.
- **Implementación:** Sanitización explícita forzando tensores y buffers de normalización a .float() antes del autocast a .half().

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
