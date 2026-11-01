# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-226: Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT (FAIL_01)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_01)
- **Problema:** Modelos con ROC-AUC > 0.82 y buena convergencia en entrenamiento colapsaron a pF1 de 0.02 en validación y test por evaluar con un umbral fijo estándar (0.50). Caída de más de 600 puestos en el Private Leaderboard para equipos que no optimizaron el umbral.
- **Causa Raíz:** La métrica pF1 sobre una prevalencia mamográfica extrema (~2.1% positiva) es hipersensible al umbral de binarización. Con umbral 0.50, la precisión y recall colapsan por inhibición de predicciones positivas. El umbral óptimo residía entre [0.03, 0.08].
- **Implementación:** Optimización simplex Nelder-Mead continua del umbral sobre predicciones OOF restringiendo recall mínimo.

### [ ] SUPER-TAREA CMRE-227: Mitigación de SCAFFOLD_ANALOG_MEMORIZATION_LEAK (FAIL_04)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_04)
- **Problema:** Top-10 accuracy de 94.5% en validación aleatoria; colapso catastrófico a 28.2% al evaluar en el conjunto ciego de prueba.
- **Causa Raíz:** Memorización de subestructuras moleculares homólogas. La validación aleatoria colocó análogos químicos estrechos en train y test. El modelo memorizó huellas de fragmentos específicos en lugar de aprender los principios de fragmentación espectral MS/MS.
- **Implementación:** Particionado disjunto por esqueletos moleculares de Bemis-Murcko (BemisMurckoScaffoldSplit).

### [ ] SUPER-TAREA CMRE-228: Mitigación de SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE (FAIL_11)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_11)
- **Problema:** Pipeline híbrido V2 de búsqueda simbólica + heurísticas colapsó a un score oficial de 0.00 en Kaggle tras 17 horas de corrida.
- **Causa Raíz:** Cuando el motor simbólico alcanzó su límite de profundidad y tiempo de CPU, el bloque de escape ejecutó fallback = test_input (copia idéntica de la grilla de entrada). En ARC-AGI, la grilla objetivo jamás es idéntica a la entrada; por tanto 0/240 intentos fueron correctos.
- **Implementación:** Guardián estricto anti-identidad que prohíbe la sumisión de grillas idénticas y conmuta a Test-Time Training (TTT) con aumentaciones D8 y transformaciones cromáticas/topológicas seguras.

### [ ] SUPER-TAREA CMRE-229: Mitigación de UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION (FAIL_12)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_12)
- **Problema:** Pipeline multi-modelo con más de 30 sub-redes (DINO slot-attention, 5 folds A5, RadImageNet y 4 ramas CoAtNet) demoró más de 6.5 horas en el test set privado, rozando el timeout de 9 horas y arriesgando la pérdida de la sumisión.
- **Causa Raíz:** Sobre-ingeniería de ensamble sin presupuestación de latencia de inferencia. La concatenación ciega de modelos pesados sin podado greedy degrada la velocidad sin aportar ganancia marginal de AUC.
- **Implementación:** LatencyBudgetPruner podando el ensamble a una tríada quirúrgica (KneeSpecialistMONAI512 + CoAtNet + Raptor) reduciendo el tiempo de inferencia a 1.86s por estudio.

### [ ] SUPER-TAREA CMRE-230: Mitigación de CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH (FAIL_13)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_13)
- **Problema:** Al ejecutar inferencia en Kaggle GPU (Tesla T4) con torch.autocast, el kernel falló con RuntimeError: expected scalar type Half but found Double.
- **Causa Raíz:** Constantes de normalización ImageNet (mean/std) importadas como float64 (Double) en NumPy o PyTorch. Al interactuar con capas Half sin conversión explícita, CUDA aborta la ejecución.
- **Implementación:** Sanitización explícita forzando tensores y buffers de normalización a .float() antes del autocast a .half().

### [ ] SUPER-TAREA CMRE-231: Mitigación de UNCONSTRAINED_CANDIDATE_DECOY_OVERLOAD (FAIL_14)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_14)
- **Problema:** Búsqueda ciega en bibliotecas masivas (400k LOTUS/COCONUT) saturó el Top-25 con moléculas decoy que compartían masa similar pero presentaban fórmulas incompatibles con las pérdidas neutras espectrales.
- **Causa Raíz:** Filtrado basado exclusivamente en delta de masa monoisotópica sin validación de reglas biofísicas de fragmentación. Las moléculas con estructuras ajenas a las vías biológicas dominaban el ranking.
- **Implementación:** Axioma de Ausencia SIRIUS que penaliza severamente candidatos que carecen de heteroátomos (O, N) requeridos para las pérdidas neutrales observadas (H2O, CO2, NH3).

