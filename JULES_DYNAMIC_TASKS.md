# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 6 nuevas super-tareas agnósticas (CMRE-97 a CMRE-102) para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [x] SUPER-TAREA CMRE-97: Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT
- **Origen:** `FAIL_01` (Catálogo de fallos).
- **Problema:** Métrica teórica vs métrica de negocio desalineada debido al colapso de umbrales bajo restricciones continuas.
- **Implementación:** Incorporar optimización simplex Nelder-Mead continua del umbral sobre predicciones OOF restringiendo recall mínimo.

### [x] SUPER-TAREA CMRE-98: Mitigación de PRECURSOR_MASS_AMBIGUITY
- **Origen:** Desafío `precursor_mass_ambiguity` en `0074-enveda-casmi2026`.
- **Problema:** Múltiples isómeros comparten la misma masa monoisotópica, imposibilitando la resolución analítica sin información estructural gráfica.
- **Implementación:** Desarrollar extractor Graph Isomorphism Network (GIN) de `molecular_smiles_graph` para desambiguar isómeros.

### [x] SUPER-TAREA CMRE-99: Mitigación de ZERO_SHOT_GENERALIZATION
- **Origen:** Desafío `zero_shot_generalization` en `0076-arc-prize-2026`.
- **Problema:** Falta de capacidad del motor simbólico para abstraer reglas en una única muestra sin sobreajustar o requerir entrenamiento.
- **Implementación:** Integrar módulo de Meta-Learning adaptativo evaluando Few-Shot Demonstrations previo a la síntesis del programa discreto.

### [x] SUPER-TAREA CMRE-100: Mitigación de MDL_PROGRAM_COMPLEXITY
- **Origen:** Desafío `mdl_program_complexity` en `0076-arc-prize-2026`.
- **Problema:** Explosión del espacio de búsqueda simbólico produciendo programas sintéticos demasiado complejos (sobreajuste).
- **Implementación:** Implementar regularización estructural penalizando Minimum Description Length (MDL) de programas en el motor de búsqueda.

### [x] SUPER-TAREA CMRE-101: Mitigación de SEVERE_CLASS_IMBALANCE
- **Origen:** Desafío `severe_class_imbalance` en `0075-rsna-knee-detection`.
- **Problema:** Clases minoritarias en el dataset de lesiones de rodilla sufren colapso de recall.
- **Implementación:** Implementar esquemas híbridos de Asymmetric Loss o Focal Loss acompañados de sobremuestreo dinámico.

### [x] SUPER-TAREA CMRE-102: Mitigación de TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS
- **Origen:** `FAIL_02` (Catálogo de fallos).
- **Problema:** Filtración de datos de prueba en la validación debido a ventanas temporales autocorrelacionadas sin embargo.
- **Implementación:** Integrar estrategia de división `PurgedGroupTimeSeriesSplit` con parametrización explícita de ventana de embargo temporal.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
