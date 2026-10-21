# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-133: Mitigación de UNCONSTRAINED_CANDIDATE_DECOY_OVERLOAD
- **Origen:** `FAIL_14` (Catálogo de fallos)
- **Problema:** Búsqueda ciega en bibliotecas masivas (400k LOTUS/COCONUT) saturó el Top-25 con moléculas decoy que ...
- **Implementación:** Axioma de Ausencia SIRIUS que penaliza severamente candidatos que carecen de heteroátomos (O, N) requeridos para las pérdidas neutrales observadas (H2O, CO2, NH3).

### [ ] SUPER-TAREA CMRE-134: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS
- **Origen:** `FAIL_02` (Catálogo de fallos)
- **Problema:** Validación cruzada K-Fold aleatoria infló el score a 5.12 MAE. En la fase de test en vivo (Private L...
- **Implementación:** PurgedGroupTimeSeriesSplit con ventana de embargo de al menos 10 minutos entre pliegues de entrenamiento y test.

### [ ] SUPER-TAREA CMRE-135: Mitigación de SCAFFOLD_ANALOG_MEMORIZATION_LEAK
- **Origen:** `FAIL_04` (Catálogo de fallos)
- **Problema:** Top-10 accuracy de 94.5% en validación aleatoria; colapso catastrófico a 28.2% al evaluar en el conj...
- **Implementación:** Particionado disjunto por esqueletos moleculares de Bemis-Murcko (BemisMurckoScaffoldSplit).

### [ ] SUPER-TAREA CMRE-136: Mitigación de SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE
- **Origen:** `FAIL_11` (Catálogo de fallos)
- **Problema:** Pipeline híbrido V2 de búsqueda simbólica + heurísticas colapsó a un score oficial de 0.00 en Kaggle...
- **Implementación:** Guardián estricto anti-identidad que prohíbe la sumisión de grillas idénticas y conmuta a Test-Time Training (TTT) con aumentaciones D8 y transformaciones cromáticas/topológicas seguras.

### [ ] SUPER-TAREA CMRE-137: Mitigación de CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH
- **Origen:** `FAIL_13` (Catálogo de fallos)
- **Problema:** Al ejecutar inferencia en Kaggle GPU (Tesla T4) con torch.autocast, el kernel falló con RuntimeError...
- **Implementación:** Sanitización explícita forzando tensores y buffers de normalización a .float() antes del autocast a .half().

### [ ] SUPER-TAREA CMRE-138: Mitigación de EDGE_SEAM_BOUNDARY_DEGRADATION
- **Origen:** `FAIL_03` (Catálogo de fallos)
- **Problema:** Modelos con Dice de 0.88 en parches aislados de 512x512 colapsaron a 0.74 al evaluar la imagen gigap...
- **Implementación:** Corte con solapamiento del 25% y reconstrucción mediante ponderación separable con ventana 2D de Hanning.

### [ ] SUPER-TAREA CMRE-139: Mitigación de NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE
- **Origen:** `FAIL_09` (Catálogo de fallos)
- **Problema:** Regresión lineal ordinaria (OLS) sobre las predicciones de 15 modelos de Gradient Boosting asignó co...
- **Implementación:** Mínimos Cuadrados No Negativos (Non-Negative Least Squares / NNLS) forzando w_i >= 0 y suma(w) = 1.0.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
