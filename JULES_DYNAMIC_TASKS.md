# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Cierre de Sesión y Proyección Auto-Evolutiva (09 de October 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito dinámicamente tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 6 nuevas super-tareas agnósticas (CMRE-67 a CMRE-72) para abordar vulnerabilidades de memorización, colinealidad, alineación de vistas ortogonales y complejidad MDL.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-67: Decodificador Canónico MONOCHROME LUT (RSNA / DICOM)
- **Origen:** `FAIL_10` (`INVERSION_MONOCHROME_LUT_MISINTERPRETATION`) y dominio `medical_radiology_vision`.
- **Problema:** Ignorar la etiqueta `PhotometricInterpretation` en archivos DICOM invierte la polaridad de las características, arruinando inferencias de CNN en hospitales que usan MONOCHROME1 en vez de MONOCHROME2.
- **Implementación:** Desarrollar en `MOD_INGEST` o un módulo utilitario de DICOM un decodificador y normalizador estricto que garantice la estandarización universal a MONOCHROME2 antes de llegar a las CNNs.

### [ ] SUPER-TAREA CMRE-68: Optimizador de Complejidad MDL para ARC-AGI
- **Origen:** `ACTIVE_COMPETITIONS.json` (`mdl_program_complexity`) para ARC Prize 2026.
- **Problema:** Los motores de síntesis de programas suelen encontrar múltiples reglas DSL que encajan en las demostraciones (few-shot), causando sobreajuste (zero-shot generalization) si la regla elegida es innecesariamente compleja.
- **Implementación:** Construir en `MOD_MODEL` o `src/cmre/solvers/arc_agi_hybrid_solver.py` un filtro que aplique el Principio de Longitud de Descripción Mínima (Minimum Description Length - MDL) priorizando programas de menor longitud de AST / tokens sobre programas largos.

### [ ] SUPER-TAREA CMRE-69: Bi-Tempered Logistic Loss para Mitigación de Ruido en Etiquetas
- **Origen:** `FAIL_08` (`LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION`).
- **Problema:** En problemas con ruido (como medicina u observaciones de campo), la pérdida Cross-Entropy pura penaliza exponencialmente, corrompiendo gradientes al forzar a la red a memorizar ruido extremo.
- **Implementación:** Implementar en `MOD_LOSS` la función de pérdida `BiTemperedLoss` o `Soft-F1` suavizada (temperaturas t1 y t2) que otorgue robustez ante outliers asimétricos y evite el colapso del gradiente.

### [ ] SUPER-TAREA CMRE-70: Stacking Meta-Model con Non-Negative Least Squares (NNLS)
- **Origen:** `FAIL_09` (`NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE`).
- **Problema:** Ensamblar scores usando regresión ordinaria (OLS) sobre modelos multicolineales asigna pesos altamente negativos, resultando en probabilidades inválidas e infinitos Log-Loss.
- **Implementación:** Desarrollar en `MOD_ENSEMBLE` un método de stacking estricto basado en NNLS para forzar pesos positivos dentro de un simplex sumatorio $1.0$, logrando robustez ante colinealidad.

### [ ] SUPER-TAREA CMRE-71: Delta Trick y Normalización Robusta IQR para Conteos Sintéticos
- **Origen:** `FAIL_07` (`UNSCALED_COUNT_FEATURE_LEAKAGE_AND_CONSTANT_SHIFT`).
- **Problema:** Características basadas en conteos crudos de dispersión (sparsity counts) sufren cambios distributivos masivos entre sets, causando caídas de cientos de lugares en el LB Privado.
- **Implementación:** Implementar en `MOD_FEAT` un transformador que convierta características de conteo puro en "Deltas relativos" e IQR Robust Scaling, neutralizando fugas basadas en tamaño de muestra y set.

### [ ] SUPER-TAREA CMRE-72: Alineador Dinámico de Vistas Ortogonales (Multi-View Ortho-Alignment)
- **Origen:** `ACTIVE_COMPETITIONS.json` (`multi_view_ortho_alignment`) para RSNA Knee.
- **Problema:** En estudios 3D/2.5D de rodilla, los volúmenes Sagitales, Coronales y Axiales deben contextualizarse; pasarlos como slices desvinculadas impide que el modelo correlacione lesiones cruzadas.
- **Implementación:** Construir en `MOD_MODEL` o `MOD_FEAT` un módulo `OrthoAligner` que concatene encodings o aplique Cross-Attention entre los tensores de diferentes vistas antes del head clasificador multi-etiqueta.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
