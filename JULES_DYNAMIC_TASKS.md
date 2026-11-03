# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-238: Mitigación de FAIL_11 (SNIP_ARC_ANTI_IDENTITY_GUARD)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_11)
- **Problema:** Pipeline híbrido V2 de búsqueda simbólica + heurísticas colapsó a un score oficial de 0.00 en Kaggle tras 17 horas de corrida.
- **Causa Raíz:** Cuando el motor simbólico alcanzó su límite de profundidad y tiempo de CPU, el bloque de escape ejecutó fallback = test_input (copia idéntica de la grilla de entrada). En ARC-AGI, la grilla objetivo jamás es idéntica a la entrada; por tanto 0/240 intentos fueron correctos.
- **Implementación:** Guardián estricto anti-identidad que prohíbe la sumisión de grillas idénticas y conmuta a Test-Time Training (TTT) con aumentaciones D8 y transformaciones cromáticas/topológicas seguras.

### [ ] SUPER-TAREA CMRE-239: Mitigación de FAIL_12 (SNIP_ENS_LATENCY_BUDGET_PRUNING)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_12)
- **Problema:** Pipeline multi-modelo con más de 30 sub-redes demoró más de 6.5 horas en el test set privado, rozando el timeout de 9 horas y arriesgando la pérdida de la sumisión.
- **Causa Raíz:** Sobre-ingeniería de ensamble sin presupuestación de latencia de inferencia. La concatenación ciega de modelos pesados sin podado greedy degrada la velocidad sin aportar ganancia marginal de AUC.
- **Implementación:** LatencyBudgetPruner podando el ensamble a una tríada quirúrgica (KneeSpecialistMONAI512 + CoAtNet + Raptor) reduciendo el tiempo de inferencia a 1.86s por estudio.

### [ ] SUPER-TAREA CMRE-240: Mitigación de FAIL_13 (SNIP_GPU_FP16_PRECISION_SANITIZER)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_13)
- **Problema:** Al ejecutar inferencia en Kaggle GPU (Tesla T4) con torch.autocast, el kernel falló con RuntimeError: expected scalar type Half but found Double.
- **Causa Raíz:** Constantes de normalización ImageNet (mean/std) importadas como float64 (Double) en NumPy o PyTorch. Al interactuar con capas Half sin conversión explícita, CUDA aborta la ejecución.
- **Implementación:** Sanitización explícita forzando tensores y buffers de normalización a .float() antes del autocast a .half().

### [ ] SUPER-TAREA CMRE-241: Mitigación de FAIL_14 (SNIP_CHEM_SIRIUS_ABSENCE_FILTER)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_14)
- **Problema:** Búsqueda ciega en bibliotecas masivas saturó el Top-25 con moléculas decoy que compartían masa similar pero presentaban fórmulas incompatibles con las pérdidas neutras espectrales.
- **Causa Raíz:** Filtrado basado exclusivamente en delta de masa monoisotópica sin validación de reglas biofísicas de fragmentación. Las moléculas con estructuras ajenas a las vías biológicas dominaban el ranking.
- **Implementación:** Axioma de Ausencia SIRIUS que penaliza severamente candidatos que carecen de heteroátomos (O, N) requeridos para las pérdidas neutrales observadas (H2O, CO2, NH3).

### [ ] SUPER-TAREA CMRE-242: Mitigación de FAIL_02 (SINGLE_VIEW_EDGE_DEGRADATION_ARTEFACT)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_02)
- **Problema:** El parcheado ciego (tiling) masivo en Whole Slide Images (WSI) sin contexto global provocó clasificaciones de alto riesgo en bordes benignos.
- **Causa Raíz:** Pérdida de topología tisular global al procesar tiles de 256x256 aislados.
- **Implementación:** Bimodal WSI Fusion con embeddings globales (DINOv2) y atención cruzada tile-to-slide.

### [ ] SUPER-TAREA CMRE-243: Mitigación de FAIL_05 (TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_05)
- **Problema:** Un modelo predictivo de series de tiempo financieras colapsó de Sharpe 2.4 OOF a Sharpe -1.2 en vivo.
- **Causa Raíz:** Fuga de autocorrelación temporal al normalizar Z-Score sobre ventanas temporales superpuestas (lookahead bias sutil).
- **Implementación:** Splitter de validación cruzada temporal estricto de series temporales (PurgedGroupTimeSeriesSplit).
