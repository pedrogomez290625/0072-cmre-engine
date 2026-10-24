# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-157: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS
- **Origen:** `FAIL_02` (Catálogo de fallos)
- **Problema:** Validación cruzada K-Fold aleatoria infló el score a 5.12 MAE. En la fase de test en vivo (Private L...
- **Implementación:** PurgedGroupTimeSeriesSplit con ventana de embargo de al menos 10 minutos entre pliegues de entrenamiento y test.

### [ ] SUPER-TAREA CMRE-158: Mitigación de severe_class_imbalance en RSNA
- **Origen:** `ACTIVE_COMPETITIONS.json` (Retos activos)
- **Problema:** Desafío activo no resuelto completamente que limita el performance en el torneo asociado.
- **Implementación:** Implementar focal loss calibrada con temperature scaling para clases severamente desbalanceadas en radiología.

### [ ] SUPER-TAREA CMRE-159: Mitigación de multi_view_ortho_alignment en MRI
- **Origen:** `ACTIVE_COMPETITIONS.json` (Retos activos)
- **Problema:** Desafío activo no resuelto completamente que limita el performance en el torneo asociado.
- **Implementación:** Desarrollar un alineador 3D robusto invariante a la resolución para vistas sagital y coronal en MRI.

### [ ] SUPER-TAREA CMRE-160: Optimización para kaggle_timeout_risk
- **Origen:** `ACTIVE_COMPETITIONS.json` (Retos activos)
- **Problema:** Desafío activo no resuelto completamente que limita el performance en el torneo asociado.
- **Implementación:** Integrar poda dinámica de ensambles basada en budget de latencia y metric drop tolerance (Tolerancia a la Caída de Métrica).

### [ ] SUPER-TAREA CMRE-161: Mitigación de high_dimensional_decoys en Espectrometría
- **Origen:** `ACTIVE_COMPETITIONS.json` (Retos activos)
- **Problema:** Desafío activo no resuelto completamente que limita el performance en el torneo asociado.
- **Implementación:** Refinar filtros biofísicos para descartar decoys sin presencia de fragmentos peptídicos comunes en CASMI.

### [ ] SUPER-TAREA CMRE-162: Resolución de precursor_mass_ambiguity
- **Origen:** `ACTIVE_COMPETITIONS.json` (Retos activos)
- **Problema:** Desafío activo no resuelto completamente que limita el performance en el torneo asociado.
- **Implementación:** Módulo de corrección de ventanas de aislamiento para masas precursoras ambiguas en MS/MS.

### [ ] SUPER-TAREA CMRE-163: Manejo de neutral_loss_absence
- **Origen:** `ACTIVE_COMPETITIONS.json` (Retos activos)
- **Problema:** Desafío activo no resuelto completamente que limita el performance en el torneo asociado.
- **Implementación:** Implementar validador de vías de fragmentación usando un grafo dirigido de pérdidas neutras permitidas.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
