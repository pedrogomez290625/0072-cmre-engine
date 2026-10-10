# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Cierre de Sesión y Proyección Auto-Evolutiva (09 de Octubre de 2026)
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 6 nuevas super-tareas agnósticas (CMRE-73 a CMRE-78) para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-73: Generador de Aumentaciones Topológicas D8 (ARC-AGI)
- **Origen:** `FAIL_11` (`SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE`) y `anti_identity_collapse` (ARC Prize).
- **Problema:** Para prevenir colapso a score 0.00 en fallback en ARC-AGI, necesitamos divergencia garantizada si el razonamiento simbólico falla por timeout.
- **Implementación:** Desarrollar en `MOD_OOD` o `arc_agi_hybrid_solver.py` un generador que aplique sistemáticamente las 8 transformaciones diédricas (D8) para evadir la identidad absoluta de entrada-salida.

### [ ] SUPER-TAREA CMRE-74: Filtro de Ambigüedad de Masa Precursora (CASMI)
- **Origen:** `ACTIVE_COMPETITIONS.json` (`precursor_mass_ambiguity`) y `FAIL_14`.
- **Problema:** Búsquedas saturadas por decoys debido a variaciones isotópicas y ambigüedades en la ventana de aislamiento del espectrómetro de masas.
- **Implementación:** Implementar en `MOD_FEAT` un filtro que descarte candidatos moleculares cuyas masas teóricas escapen a un margen dinámico de PPM.

### [ ] SUPER-TAREA CMRE-75: Pipeline de Aumentación TTA Dinámico (Presupuesto de Latencia)
- **Origen:** `FAIL_12` (`UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION`) y `kaggle_timeout_risk` (RSNA Knee).
- **Problema:** Aplicar Test-Time Augmentation (TTA) de manera estática (e.g. 8x o 10x) en datasets grandes viola el límite de inferencia y causa Timeouts en sumisión.
- **Implementación:** Construir en `MOD_ENSEMBLE` un orquestador TTA que monitoree la latencia por muestra y reduzca el factor TTA si el presupuesto global peligra.

### [ ] SUPER-TAREA CMRE-76: Estratificación Estricta por Identidad de Paciente (PatientGroupKFold)
- **Origen:** `FAIL_05` (`PATIENT_IDENTITY_COHORT_LEAKAGE`) y dominio `medical_radiology_vision`.
- **Problema:** Los splits aleatorios o estratificados simples pueden repartir distintas tomas del mismo paciente entre train y validación, inflando métricas por memorización de biometría.
- **Implementación:** Implementar en `MOD_SIGNAL` un partidor `PatientGroupKFold` que garantice disjunción de pacientes entre pliegues.

### [ ] SUPER-TAREA CMRE-77: Alineador Nelder-Mead de Umbrales Asimétricos Multi-Clase
- **Origen:** `FAIL_01` (`THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT`) y `severe_class_imbalance`.
- **Problema:** En clasificación multi-etiqueta severamente desbalanceada, un umbral global estático de 0.5 destruye el recall de las clases raras (e.g., lesiones infrecuentes en rodilla).
- **Implementación:** Construir en `MOD_ENSEMBLE` una extensión de optimización Nelder-Mead que optimice un vector de umbrales continuos independientemente para cada clase maximizando la métrica final (Macro-ROC-AUC).

### [ ] SUPER-TAREA CMRE-78: Detector de Fugas por Autocorrelación Temporal (Time Series Leak Guard)
- **Origen:** `FAIL_02` (`TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS`).
- **Problema:** Crear features de retardo horario (lags) o medias móviles sin un gap de purga causa lookahead temporal en validación.
- **Implementación:** Desarrollar en `MOD_OOD` un utilitario `TimeSeriesLeakDetector` que alerte si se detectan superposiciones en las ventanas de agregación entre muestras de entrenamiento y de test/validación.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
