# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Sesión Post-Benchmarking (28 de Septiembre 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI

Este archivo es reescrito por el motor tras cada cierre de sesión. Las tareas de ingeniería han sido destiladas analizando el archivo `ACTIVE_COMPETITIONS.json` y el `data/knowledge/postmortems_failures_catalog.json`.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-07: Guardián Estricto Anti-Identidad ARC-AGI
- **Origen:** Postmortem `FAIL_11` (Kaggle ARC Prize 2026).
- **Problema:** Un pipeline híbrido simbólico/neuronal colapsó al agotar el tiempo, activando un fallback pasivo que devolvía la grilla de entrada sin modificar, garantizando 0 aciertos.
- **Implementación:** Desarrollar en `src/cmre/modules/ensemble.py` o `src/cmre/services/submission_validator.py` un `AntiIdentityGuard` que intercepte cualquier predicción idéntica a la entrada y conmute automáticamente a perturbaciones seguras (TTT, D8 o cambio topológico mínimo).
- **Verificación:** `tests/test_arc_anti_identity.py` (simular timeout simbólico y verificar conmutación).

### [ ] SUPER-TAREA CMRE-08: Podador de Ensamble por Presupuesto de Latencia
- **Origen:** Postmortem `FAIL_12` (RSNA Knee Abnormality 2026).
- **Problema:** Riesgo inminente de timeout en inferencia Kaggle (>6.5 horas) debido al ensamble ciego de más de 30 sub-redes masivas (ViT, DINO, CoAtNet) sobre imágenes multi-vista.
- **Implementación:** Refinar en `src/cmre/modules/ensemble.py` el componente `LatencyBudgetPruner` para que perfile en milisegundos cada modelo en inferencia y ejecute una poda greedy, limitando el tamaño del ensamble para mantenerse por debajo del `latency_budget_per_sample_sec` definido en el `ACTIVE_COMPETITIONS.json`.
- **Verificación:** `tests/test_latency_pruner.py` asegurando respeto al budget.

### [ ] SUPER-TAREA CMRE-09: Interceptor Global de Precisión (Float vs Double) para CUDA
- **Origen:** Postmortem `FAIL_13` (RSNA Knee 2026, Runtime Error).
- **Problema:** Fallas de CUDA `expected scalar type Half but found Double` inducidas por constantes de normalización ImageNet que numpy exporta como float64.
- **Implementación:** En `src/cmre/modules/ingest.py` y el motor central de tensores, inyectar un decorador o hook global `sanitize_tensor_dtypes` que escanee todos los diccionarios, arrays y tensores forzando su casting a `.float()` pre-inferencia, antes de entrar al scope `torch.autocast()`.
- **Verificación:** `tests/test_cuda_type_sanitizer.py`.

### [ ] SUPER-TAREA CMRE-10: Filtro Axiomático Biofísico (SIRIUS) en CASMI
- **Origen:** Postmortem `FAIL_14` (Enveda CASMI 2026).
- **Problema:** Saturación en Top-25 por moléculas decoy químicamente inviables; masas compatibles pero fórmulas incoherentes con pérdidas de agua (H2O) o amoníaco (NH3).
- **Implementación:** Añadir en el componente molecular (`src/cmre/modules/hpc.py` o de parseo químico) la validación estructurada `NeutralLossBiophysicsFilter`. Si el espectro acusa pérdida de H2O, se descarta todo candidato sin átomos de Oxígeno en su SMILES.
- **Verificación:** `tests/test_biophysics_sirius_filter.py`.

### [ ] SUPER-TAREA CMRE-11: Estratificación Inflexible por Identidad (Paciente/Sujeto)
- **Origen:** Postmortem `FAIL_05` (ISIC 2024).
- **Problema:** Sobreajuste y fuga de datos en Kaggle al mezclar el fondo de la piel del paciente en pliegues de entrenamiento y validación.
- **Implementación:** Robustecer el módulo `MOD_SPLIT` (`src/cmre/modules/split.py`) forzando la obligatoriedad de que la variable `group_id` (e.g., patient_id, subject_id) lance una alerta `LeakageWarning` o error estricto si se detecta entropía mayor a 0 en la distribución del mismo ID a través de los folds OOF.
- **Verificación:** `tests/test_strict_patient_isolation.py`.

### [ ] SUPER-TAREA CMRE-12: Ventanas Cosenoidales para Reconstrucción Gigapíxel
- **Origen:** Postmortem `FAIL_03` (HuBMAP Kidney WSI).
- **Problema:** Discontinuidades catastróficas en costuras de patches (tiling simple), degradando el Dice al reconstruir la imagen macro.
- **Implementación:** Implementar `HanningWindowTiler` en `src/cmre/modules/ingest.py`, generando máscaras de solapamiento suaves 2D mediante pesos separable cosenoidales para predicción sin efecto cuadrícula.
- **Verificación:** `tests/test_hanning_window_tiler.py` sobre imagen sintética WSI.

### [ ] SUPER-TAREA CMRE-13: Regresor No-Negativo (NNLS) sobre Predicciones Colineales
- **Origen:** Postmortem `FAIL_09` (Kaggle Tabular Playground).
- **Problema:** Predicciones de OLS negativas en tareas probabilísticas (Log-Loss Infinito) a causa de multicolinealidad severa entre meta-modelos OOF de Boosting.
- **Implementación:** Validar exhaustivamente y expandir los tests del `SimpleNNLSBlender` ya existente en `MOD_ENSEMBLE` para que ofrezca API compatible con scikit-learn y emita log-loss estricto acotado en el simplex positivo.
- **Verificación:** Refactor de `tests/test_nnls_blender.py`.

### [ ] SUPER-TAREA CMRE-14: Lector DICOM Universal y Seguro (MONOCHROME)
- **Origen:** Postmortem `FAIL_10` (RSNA Mammography).
- **Problema:** Inversión térmica de tejidos blancos y negros por ignorar la metadata `PhotometricInterpretation`.
- **Implementación:** Expandir el `MOD_INGEST` actual que procesa DICOMs. Añadir el manejador estricto que lea si es `MONOCHROME1` e invierta pasivamente el array `(np.max(pixel_array) - pixel_array)` normalizándolo unificadamente hacia el estándar `MONOCHROME2`.
- **Verificación:** `tests/test_dicom_monochrome_inversion.py`.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")