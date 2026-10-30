# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-213: Mitigación de EDGE_SEAM_BOUNDARY_DEGRADATION (FAIL_03)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_03)
- **Problema:** En WSI (Whole Slide Imaging), el tilling estándar genera artefactos de borde (seams) que degradan el Dice score local de los vasos sanguíneos cerca del margen de la ventana.
- **Causa Raíz:** Falta de fusión superpuesta y ponderación gaussiana en la reconstrucción (Hanning Window Tiling).
- **Implementación:** Desarrollar `HanningWindowTiler2D` y `GaussianOverlapBlender` en MOD_VISION.

### [ ] SUPER-TAREA CMRE-214: Mitigación de TARGET_ENCODING_HIGH_CARDINALITY_LEAKAGE (FAIL_06)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_06)
- **Problema:** Target encoding directo sobre pares de tarjetas y direcciones (card1 + addr1) infló el CV a 0.985, colapsando a 0.880 en test temporal.
- **Causa Raíz:** Fuga de la variable objetivo hacia las medias de grupo sin validación cruzada interna (in-fold) ni regularización bayesiana m-estimate.
- **Implementación:** Codificación bayesiana OOF estricta con regularización m-estimate de Dirichlet y adición de ruido gaussiano (`OOFTargetEncoder` robusto).

### [ ] SUPER-TAREA CMRE-215: Mitigación de UNSCALED_COUNT_FEATURE_LEAKAGE_AND_CONSTANT_SHIFT (FAIL_07)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_07)
- **Problema:** El conteo directo de ceros por fila mejoró drásticamente el Public LB, pero cayó más de 400 puestos en Private LB al cambiar la densidad de dispersión.
- **Causa Raíz:** Sobreajuste a la matriz de dispersión sintética generada por el banco en el subconjunto público.
- **Implementación:** Cálculo de desvíos relativos (Delta Trick) y normalización robusta intercuartílica (IQR) mediante `DeltaTrickNormalizer`.

### [ ] SUPER-TAREA CMRE-216: Mitigación de INVERSION_MONOCHROME_LUT_MISINTERPRETATION (FAIL_10)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_10)
- **Problema:** Pipelines basados en OpenCV/PIL estándar leyeron mamografías DICOM sin interpretar la etiqueta PhotometricInterpretation, invirtiendo la apariencia de los tejidos en el 30% del dataset.
- **Causa Raíz:** DICOM soporta MONOCHROME1 y MONOCHROME2. Al ignorar esta metadata, las convoluciones aprendieron características con polaridad invertida.
- **Implementación:** Decodificador DICOM canónico con verificación obligatoria de PhotometricInterpretation y normalización a MONOCHROME2 (`StrictDicomLUTDecoder`).

### [ ] SUPER-TAREA CMRE-217: Mitigación de UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION (FAIL_12)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_12)
- **Problema:** Pipeline multi-modelo demoró más de 6.5 horas en el test set privado, rozando el timeout de 9 horas.
- **Causa Raíz:** Sobre-ingeniería de ensamble sin presupuestación de latencia de inferencia. La concatenación ciega de modelos pesados degrada la velocidad.
- **Implementación:** `LatencyBudgetPruner` podando el ensamble basado en presupuesto estricto manteniendo el desempeño marginal AUC.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
