# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Sesión Final de Cierre y Benchmarking (4 de Octubre 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa") & Victoria Perez

Este archivo es reescrito por el motor tras el análisis de `ACTIVE_COMPETITIONS.json` y el `data/knowledge/postmortems_failures_catalog.json`. Su objetivo es proyectar las mitigaciones a las vulnerabilidades encontradas y potenciar los solvers de las competencias activas (RSNA Knee, CASMI, ARC-AGI).

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-36: Optimizador Continuo de Umbrales (Nelder-Mead Thresholding)
- **Origen:** Postmortem `FAIL_01` (RSNA Breast Cancer) y desalineamiento de métrica pF1.
- **Problema:** Evaluar con un umbral fijo estático de 0.50 en problemas con desbalance extremo (ej. prevalencia < 5%) colapsa completamente la métrica (pF1 o F1).
- **Implementación:** Agregar una clase `NelderMeadThresholdOptimizer` en `MOD_ENSEMBLE` o `MOD_LOSS` que tome predicciones de validación cruzada y encuentre el umbral asimétrico óptimo (ej. 0.05) maximizando dinámicamente la métrica sin colapsar el recall.
- **Verificación:** `tests/test_nelder_mead_threshold_optimizer.py`.

### [ ] SUPER-TAREA CMRE-37: Guardián contra Fuga en Target Encoding (Out-of-Fold TE)
- **Origen:** Postmortem `FAIL_06` (Home Credit Default Risk).
- **Problema:** Calcular variables categóricas de target encoding sin un esquema riguroso OOF provoca data leakage masivo, inflando artificialmente el ROC-AUC en validación cruzada para luego colapsar en producción.
- **Implementación:** Refactorizar o añadir `OOFTargetEncoder` en `MOD_SIGNAL` que fuerce de manera estricta la partición, aplicando regularización de Dirichlet y adición de ruido gaussiano en cada pliegue de entrenamiento antes de transformar la validación.
- **Verificación:** `tests/test_oof_target_encoder.py`.

### [ ] SUPER-TAREA CMRE-38: Módulo de Pérdida Resistente a Ruido de Etiquetas (Soft-F1 Weighted)
- **Origen:** Postmortem `FAIL_08` (Cassava Leaf Disease).
- **Problema:** En dominios médicos o biológicos con diagnósticos inexactos de campo (15-20% de ruido en etiquetas), la Cross-Entropy pura corrompe los gradientes porque fuerza a la red a memorizar el ruido.
- **Implementación:** Potenciar `MOD_LOSS` con un implementador puro de `BiTemperedLogisticLoss` o extender `SoftF1Loss` con mitigación robusta de outliers a través de Label Smoothing diferencial por clase.
- **Verificación:** `tests/test_noise_robust_loss.py`.

### [ ] SUPER-TAREA CMRE-39: Ensamble Restringido Simplex Positivo (NNLS Stacking estricto)
- **Origen:** Postmortem `FAIL_09` (Tabular Playground Series).
- **Problema:** Usar Ordinary Least Squares (OLS) sobre meta-modelos altamente colineales resulta en coeficientes negativos masivos, lo que destruye el Log-Loss (probabilidades menores que 0).
- **Implementación:** Reemplazar el backend ingenuo en `MOD_ENSEMBLE` y garantizar que la clase de ensamblaje (ej. `NonNegativeLeastSquaresBlender`) fuerce matemáticamente los pesos en el simplex $(w_i \ge 0, \sum w_i = 1)$.
- **Verificación:** `tests/test_nnls_simplex_blender.py`.

### [ ] SUPER-TAREA CMRE-40: Auto-Decodificador Universal DICOM MONOCHROME2
- **Origen:** Postmortem `FAIL_10` (RSNA Breast Cancer) con la etiqueta PhotometricInterpretation.
- **Problema:** Ignorar las tablas Modality LUT y la inversión MONOCHROME1 en DICOM causa que los modelos confundan regiones tumorales y tejido normal en el 30% del dataset.
- **Implementación:** Implementar un middleware robusto `StrictDicomLUTDecoder` dentro de `MOD_INGEST` que analice los metadatos DICOM por defecto e invierta dinámicamente las matrices de píxeles a MONOCHROME2 canónico antes del rescale.
- **Verificación:** `tests/test_strict_dicom_lut_decoder.py`.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa") & Victoria Perez
