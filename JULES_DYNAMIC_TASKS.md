# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-140: Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT
- **Origen:** `FAIL_01` (Catálogo de fallos)
- **Problema:** Modelos con ROC-AUC > 0.82 y buena convergencia en entrenamiento colapsaron a pF1 de 0.02 en validac...
- **Implementación:** Optimización simplex Nelder-Mead continua del umbral sobre predicciones OOF restringiendo recall mínimo.

### [ ] SUPER-TAREA CMRE-141: Mitigación de PATIENT_IDENTITY_COHORT_LEAKAGE
- **Origen:** `FAIL_05` (Catálogo de fallos)
- **Problema:** ROC-AUC local de 0.945; caída a 0.812 pAUC en Private LB y fallo en detección de melanomas sutiles....
- **Implementación:** StratifiedGroupKFold agrupado estrictamente por patient_id combinado con la normalización de Patito Feo.

### [ ] SUPER-TAREA CMRE-142: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS
- **Origen:** `FAIL_02` (Catálogo de fallos)
- **Problema:** Validación cruzada K-Fold aleatoria infló el score a 5.12 MAE. En la fase de test en vivo (Private L...
- **Implementación:** PurgedGroupTimeSeriesSplit con ventana de embargo de al menos 10 minutos entre pliegues de entrenamiento y test.

### [ ] SUPER-TAREA CMRE-143: Mitigación de UNSCALED_COUNT_FEATURE_LEAKAGE_AND_CONSTANT_SHIFT
- **Origen:** `FAIL_07` (Catálogo de fallos)
- **Problema:** El conteo directo de ceros por fila mejoró drásticamente el Public LB (0.52 RMSLE), pero cayó más de...
- **Implementación:** Cálculo de desvíos relativos (Delta Trick) y normalización robusta intercuartílica (IQR).

### [ ] SUPER-TAREA CMRE-144: Mitigación de CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH
- **Origen:** `FAIL_13` (Catálogo de fallos)
- **Problema:** Al ejecutar inferencia en Kaggle GPU (Tesla T4) con torch.autocast, el kernel falló con RuntimeError...
- **Implementación:** Sanitización explícita forzando tensores y buffers de normalización a .float() antes del autocast a .half().

### [ ] SUPER-TAREA CMRE-145: Mitigación de UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION
- **Origen:** `FAIL_12` (Catálogo de fallos)
- **Problema:** Pipeline multi-modelo con más de 30 sub-redes (DINO slot-attention, 5 folds A5, RadImageNet y 4 rama...
- **Implementación:** LatencyBudgetPruner podando el ensamble a una tríada quirúrgica (KneeSpecialistMONAI512 + CoAtNet + Raptor) reduciendo el tiempo de inferencia a 1.86s por estudio.

### [ ] SUPER-TAREA CMRE-146: Mitigación de UNCONSTRAINED_CANDIDATE_DECOY_OVERLOAD
- **Origen:** `FAIL_14` (Catálogo de fallos)
- **Problema:** Búsqueda ciega en bibliotecas masivas (400k LOTUS/COCONUT) saturó el Top-25 con moléculas decoy que ...
- **Implementación:** Axioma de Ausencia SIRIUS que penaliza severamente candidatos que carecen de heteroátomos (O, N) requeridos para las pérdidas neutrales observadas (H2O, CO2, NH3).

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
