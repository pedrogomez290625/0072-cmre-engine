# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Cierre de Sesión y Proyección Auto-Evolutiva (13 de Octubre de 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 6 nuevas super-tareas agnósticas (CMRE-91 a CMRE-96) para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-91: Mitigación de LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION
- **Origen:** `FAIL_08` y catálogo de fallos.
- **Problema:** Modelos complejos memorizan ruido en etiquetas de campo, corrompiendo gradientes con Cross-Entropy pura.
- **Implementación:** Forzar el uso de `WeightedSoftF1Loss` y suavizado de etiquetas para mitigar memorización de ruido.

### [ ] SUPER-TAREA CMRE-92: Mitigación de NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE
- **Origen:** `FAIL_09` y catálogo de fallos.
- **Problema:** Ensamblado OLS produce pesos fuertemente negativos en predicciones colineales, llevando a probabilidades inválidas.
- **Implementación:** Implementar apilamiento mediante `NonNegativeLeastSquaresBlender` forzando ensamble simplex positivo.

### [ ] SUPER-TAREA CMRE-93: Mitigación de INVERSION_MONOCHROME_LUT_MISINTERPRETATION
- **Origen:** `FAIL_10` y catálogo de fallos.
- **Problema:** Ignorar metadato `PhotometricInterpretation` causa inversión de tejidos radiológicos (grasa blanca vs negra) en DICOM.
- **Implementación:** Desarrollar `StrictDicomLUTDecoder` con verificación obligatoria a MONOCHROME2.

### [ ] SUPER-TAREA CMRE-94: Mitigación de CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH
- **Origen:** `FAIL_13` y catálogo de fallos.
- **Problema:** Constantes FP64 chocan con FP16 en `torch.autocast`, causando aborto CUDA RuntimeError: expected scalar type Half.
- **Implementación:** Sanitización universal vía `sanitizer` explícito en buffer HPC antes del casteo `Half`.

### [ ] SUPER-TAREA CMRE-95: Mitigación de UNCONSTRAINED_CANDIDATE_DECOY_OVERLOAD
- **Origen:** `FAIL_14` y catálogo de fallos.
- **Problema:** Filtrado de biblioteca masiva ciega MS/MS satura Top-K con decoys de masas similares sin heteroátomos.
- **Implementación:** Introducir Axioma de Ausencia SIRIUS que restringe candidatos mediante validación de pérdidas neutras (ej. requiere O, N).

### [ ] SUPER-TAREA CMRE-96: Meta-Optimización Multi-Vista (Multi-View Orthogonal Alignment)
- **Origen:** Desafío `multi_view_ortho_alignment` en `0075-rsna-knee-detection`.
- **Problema:** Falta de convergencia por vistas anatómicas desalineadas (Axial, Coronal, Sagital).
- **Implementación:** Incorporar y estabilizar `MultiViewOrthogonalAligner` a nivel de `MOD_ENSEMBLE` o extracción de características.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
