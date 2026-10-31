# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-218: Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT (FAIL_01)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_01)
- **Problema:** Modelos con ROC-AUC > 0.82 y buena convergencia en entrenamiento colapsaron a pF1 de 0.02 en validación y test por evaluar con un umbral fijo estándar (0.50). Caída de más de 600 puestos en el Private Leaderboard para equipos que no optimizaron el umbral.
- **Causa Raíz:** La métrica pF1 sobre una prevalencia mamográfica extrema (~2.1% positiva) es hipersensible al umbral de binarización. Con umbral 0.50, la precisión y recall colapsan por inhibición de predicciones positivas. El umbral óptimo residía entre [0.03, 0.08].
- **Implementación:** Optimización simplex Nelder-Mead continua del umbral sobre predicciones OOF restringiendo recall mínimo.

### [ ] SUPER-TAREA CMRE-219: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS (FAIL_02)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_02)
- **Problema:** Validación cruzada K-Fold aleatoria infló el score a 5.12 MAE. En la fase de test en vivo (Private LB) el score se degradó a 5.89 MAE, provocando caídas de más de 800 puestos.
- **Causa Raíz:** Autocorrelación intradiaria de alta frecuencia en el libro de órdenes (order book). Muestras contiguas en el tiempo compartían micro-tendencias y volatilidad. Un split aleatorio filtró información del futuro inmediato hacia el pasado.
- **Implementación:** PurgedGroupTimeSeriesSplit con ventana de embargo de al menos 10 minutos entre pliegues de entrenamiento y test.

### [ ] SUPER-TAREA CMRE-220: Mitigación de SCAFFOLD_ANALOG_MEMORIZATION_LEAK (FAIL_04)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_04)
- **Problema:** Top-10 accuracy de 94.5% en validación aleatoria; colapso catastrófico a 28.2% al evaluar en el conjunto ciego de prueba.
- **Causa Raíz:** Memorización de subestructuras moleculares homólogas. La validación aleatoria colocó análogos químicos estrechos en train y test. El modelo memorizó huellas de fragmentos específicos en lugar de aprender los principios de fragmentación espectral MS/MS.
- **Implementación:** Particionado disjunto por esqueletos moleculares de Bemis-Murcko (BemisMurckoScaffoldSplit).

### [ ] SUPER-TAREA CMRE-221: Mitigación de PATIENT_IDENTITY_COHORT_LEAKAGE (FAIL_05)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_05)
- **Problema:** ROC-AUC local de 0.945; caída a 0.812 pAUC en Private LB y fallo en detección de melanomas sutiles.
- **Causa Raíz:** Los pacientes tenían múltiples lesiones cutáneas. Al no aislar el paciente en un único pliegue, las redes aprendieron a reconocer el tipo de piel y fondo del paciente en lugar de la atipia celular de la lesión.
- **Implementación:** StratifiedGroupKFold agrupado estrictamente por patient_id combinado con la normalización de Patito Feo.

### [ ] SUPER-TAREA CMRE-222: Mitigación de LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION (FAIL_08)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_08)
- **Problema:** Modelos complejos (EfficientNet-B5) alcanzaron 99% accuracy en train con Cross-Entropy, pero la validación se estancó en 87.5% por sobreajuste severo a etiquetas erróneas.
- **Causa Raíz:** El dataset contenía entre 15% y 20% de ruido en las etiquetas debido a diagnósticos de campo en hojas de yuca sin confirmación de laboratorio. Cross-Entropy penaliza exponencialmente las discrepancias, forzando a la red a memorizar el ruido.
- **Implementación:** Uso de Label Smoothing, Bi-Tempered Loss o Soft-F1 con gradientes amortiguados para mitigar la penalización de outliers.

### [ ] SUPER-TAREA CMRE-223: Mitigación de SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE (FAIL_11)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_11)
- **Problema:** Pipeline híbrido V2 de búsqueda simbólica + heurísticas colapsó a un score oficial de 0.00 en Kaggle tras 17 horas de corrida.
- **Causa Raíz:** Cuando el motor simbólico alcanzó su límite de profundidad y tiempo de CPU, el bloque de escape ejecutó fallback = test_input (copia idéntica de la grilla de entrada). En ARC-AGI, la grilla objetivo jamás es idéntica a la entrada; por tanto 0/240 intentos fueron correctos.
- **Implementación:** Guardián estricto anti-identidad que prohíbe la sumisión de grillas idénticas y conmuta a Test-Time Training (TTT) con aumentaciones D8 y transformaciones cromáticas/topológicas seguras.

### [ ] SUPER-TAREA CMRE-224: Mitigación de CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH (FAIL_13)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_13)
- **Problema:** Al ejecutar inferencia en Kaggle GPU (Tesla T4) con torch.autocast, el kernel falló con RuntimeError: expected scalar type Half but found Double.
- **Causa Raíz:** Constantes de normalización ImageNet (mean/std) importadas como float64 (Double) en NumPy o PyTorch. Al interactuar con capas Half sin conversión explícita, CUDA aborta la ejecución.
- **Implementación:** Sanitización explícita forzando tensores y buffers de normalización a .float() antes del autocast a .half().

### [ ] SUPER-TAREA CMRE-225: Mitigación de UNCONSTRAINED_CANDIDATE_DECOY_OVERLOAD (FAIL_14)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_14)
- **Problema:** Búsqueda ciega en bibliotecas masivas (400k LOTUS/COCONUT) saturó el Top-25 con moléculas decoy que compartían masa similar pero presentaban fórmulas incompatibles con las pérdidas neutras espectrales.
- **Causa Raíz:** Filtrado basado exclusivamente en delta de masa monoisotópica sin validación de reglas biofísicas de fragmentación. Las moléculas con estructuras ajenas a las vías biológicas dominaban el ranking.
- **Implementación:** Axioma de Ausencia SIRIUS que penaliza severamente candidatos que carecen de heteroátomos (O, N) requeridos para las pérdidas neutrales observadas (H2O, CO2, NH3).

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
