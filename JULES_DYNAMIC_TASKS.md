# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 5 nuevas super-tareas agnósticas (CMRE-108 a CMRE-112) para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-108: Mitigación de PATIENT_IDENTITY_COHORT_LEAKAGE
- **Origen:** `FAIL_05` (Catálogo de fallos).
- **Problema:** Fuga de cohortes por identidad de paciente resultando en validación OOF demasiado optimista.
- **Implementación:** Implementar StratifiedGroupKFold agrupado estrictamente por patient_id combinado con la normalización de Patito Feo.

### [ ] SUPER-TAREA CMRE-109: Mitigación de SCAFFOLD_ANALOG_MEMORIZATION_LEAK
- **Origen:** `FAIL_04` (Catálogo de fallos).
- **Problema:** Memorización de análogos de andamiaje / scaffolds moleculares en metabolómica.
- **Implementación:** Implementar particionado disjunto por esqueletos moleculares de Bemis-Murcko (BemisMurckoScaffoldSplit).

### [ ] SUPER-TAREA CMRE-110: Mitigación de SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE
- **Origen:** `FAIL_11` (Catálogo de fallos).
- **Problema:** Colapso de score a cero por devolver la entrada (identidad) intacta ante un timeout en inferencia simbólica de ARC-AGI.
- **Implementación:** Implementar Guardián estricto anti-identidad que prohíba la sumisión de grillas idénticas y conmute a Test-Time Training (TTT) con aumentaciones D8 y transformaciones cromáticas/topológicas seguras.

### [ ] SUPER-TAREA CMRE-111: Mitigación de UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION
- **Origen:** `FAIL_12` (Catálogo de fallos).
- **Problema:** Consumo total del presupuesto de latencia antes de procesar el conjunto de test completo.
- **Implementación:** Implementar LatencyBudgetPruner podando el ensamble a una tríada quirúrgica reduciendo el tiempo de inferencia a presupuestos aceptables.

### [ ] SUPER-TAREA CMRE-112: Mitigación de UNCONSTRAINED_CANDIDATE_DECOY_OVERLOAD
- **Origen:** `FAIL_14` (Catálogo de fallos).
- **Problema:** Sobrecarga de candidatos falsos no constreñidos en metabolómica.
- **Implementación:** Implementar Axioma de Ausencia SIRIUS que penaliza severamente candidatos que carecen de heteroátomos requeridos para las pérdidas neutrales observadas.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
