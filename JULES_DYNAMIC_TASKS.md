# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Sesión Final de Cierre y Benchmarking (2 de Octubre 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa") & Victoria Perez

Este archivo es reescrito por el motor tras el análisis de `ACTIVE_COMPETITIONS.json` y el `data/knowledge/postmortems_failures_catalog.json`. Su objetivo es proyectar las mitigaciones a las vulnerabilidades encontradas y potenciar los solvers de las competencias activas (RSNA Knee, CASMI, ARC-AGI).

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-25: Sistema Avanzado de Detección OOD (Out-of-Distribution)
- **Origen:** Evaluación transversal de competiciones en `ACTIVE_COMPETITIONS.json`.
- **Problema:** Desviaciones entre los datos públicos (LB) y privados generan regresiones no anticipadas (Ej: FAIL_07).
- **Implementación:** Introducir un módulo en `src/cmre/modules/ood.py` para analizar y reportar el divergence score entre train y las distribuciones entrantes durante inferencia.
- **Verificación:** `tests/test_ood_detection.py`.

### [ ] SUPER-TAREA CMRE-26: Attention-guided Patch Extraction para WSI
- **Origen:** Postmortem `FAIL_03` (HuBMAP) y retos de visión grandes.
- **Problema:** Inferencia ingenua gigapíxel desperdicia cómputo en zonas irrelevantes.
- **Implementación:** Ampliar `MOD_INGEST` o crear `MOD_VISION` integrando una red de atención liviana (ej: Clam/Mil) que prediga la saliencia de los parches antes del crop de alta resolución, reduciendo la memoria requerida.
- **Verificación:** `tests/test_attention_wsi_crop.py`.

### [ ] SUPER-TAREA CMRE-27: Grafo Molecular Extendido y Aumentación para CASMI
- **Origen:** Enveda CASMI 2026 y Postmortem `FAIL_14`.
- **Problema:** Fragmentación y decoys difíciles de discriminar solo con Tanimoto.
- **Implementación:** Extender `EnvedaCasmiSolver` para integrar embeddings de subestructuras (Morgan / MACCS extendidos) y simular ruido instrumental en entrenamiento (aumentación espectral).
- **Verificación:** `tests/test_molecular_graph_augmentation.py`.

### [ ] SUPER-TAREA CMRE-28: Meta-Controlador de Paradas Tempranas Múltiples (Multi-Metric Early Stopping)
- **Origen:** Optimización genérica en todo el motor CMRE.
- **Problema:** El Early Stopping en un solver a menudo se basa en una sola métrica de validación, ignorando el trade-off entre precision/recall (Ej: RSNA Mammography FAIL_10 relacionado a thresholds).
- **Implementación:** Añadir `MultiMetricEarlyStopping` en `MOD_LOSS` (o módulo callback) que monitoree tanto la pérdida como métricas secundarias (pAUC, F1), deteniendo el entrenamiento solo cuando hay consenso.
- **Verificación:** `tests/test_multimetric_early_stopping.py`.

### [ ] SUPER-TAREA CMRE-29: Dynamic Time-Warping y Cross-Validation Robusta en Series Temporales
- **Origen:** Postmortem `FAIL_06` (Fuga temporal en target encoding) y Zindi AirQo.
- **Problema:** Los esquemas actuales de CV de purga asumen estacionariedad tras el embargo, fallando en regímenes dinámicos.
- **Implementación:** Mejorar `PurgedGroupTimeSeriesSplit` introduciendo particiones guiadas por alineamiento DTW (Dynamic Time Warping) en lugar de cortes de tiempo estrictos.
- **Verificación:** `tests/test_dtw_timeseries_split.py`.

### [ ] SUPER-TAREA CMRE-30: Guardián Simbólico Híbrido con Auto-Atención para ARC-AGI
- **Origen:** ARC-AGI 2026 y Postmortem `FAIL_11`.
- **Problema:** Modelos TTT o simbólicos puros colapsan frente a reglas de abstracción complejas de largo alcance.
- **Implementación:** Integrar una capa de Auto-Atención (Self-Attention) direccional en el iterador simbólico de `ArcAgiHybridSolver` para ponderar la relevancia de transformaciones geométricas previas.
- **Verificación:** `tests/test_arc_self_attention_guard.py`.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa") & Victoria Perez
