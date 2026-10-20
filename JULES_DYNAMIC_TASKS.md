# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 5 nuevas super-tareas agnósticas (CMRE-128 a CMRE-132) para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-128: Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT
- **Origen:** `FAIL_01` (Catálogo de fallos)
- **Problema:** Modelos con ROC-AUC > 0
- **Implementación:** Optimización simplex Nelder-Mead continua del umbral sobre predicciones OOF restringiendo recall mínimo.

### [ ] SUPER-TAREA CMRE-129: Mitigación de EDGE_SEAM_BOUNDARY_DEGRADATION
- **Origen:** `FAIL_03` (Catálogo de fallos)
- **Problema:** Modelos con Dice de 0
- **Implementación:** Corte con solapamiento del 25% y reconstrucción mediante ponderación separable con ventana 2D de Hanning.

### [ ] SUPER-TAREA CMRE-130: Mitigación de SCAFFOLD_ANALOG_MEMORIZATION_LEAK
- **Origen:** `FAIL_04` (Catálogo de fallos)
- **Problema:** Top-10 accuracy de 94
- **Implementación:** Particionado disjunto por esqueletos moleculares de Bemis-Murcko (BemisMurckoScaffoldSplit).

### [ ] SUPER-TAREA CMRE-131: Mitigación de SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE
- **Origen:** `FAIL_11` (Catálogo de fallos)
- **Problema:** Pipeline híbrido V2 de búsqueda simbólica + heurísticas colapsó a un score oficial de 0
- **Implementación:** Guardián estricto anti-identidad que prohíbe la sumisión de grillas idénticas y conmuta a Test-Time Training (TTT) con aumentaciones D8 y transformaciones cromáticas/topológicas seguras.

### [ ] SUPER-TAREA CMRE-132: Mitigación de UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION
- **Origen:** `FAIL_12` (Catálogo de fallos)
- **Problema:** Pipeline multi-modelo con más de 30 sub-redes (DINO slot-attention, 5 folds A5, RadImageNet y 4 ramas CoAtNet) demoró más de 6
- **Implementación:** LatencyBudgetPruner podando el ensamble a una tríada quirúrgica (KneeSpecialistMONAI512 + CoAtNet + Raptor) reduciendo el tiempo de inferencia a 1.86s por estudio.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
