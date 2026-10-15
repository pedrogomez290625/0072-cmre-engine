# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta 5 nuevas super-tareas agnósticas (CMRE-103 a CMRE-107) para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-103: Mitigación de TARGET_ENCODING_HIGH_CARDINALITY_LEAKAGE
- **Origen:** `FAIL_06` (Catálogo de fallos).
- **Problema:** Fuga de la variable objetivo hacia medias de grupo causando colapso en test temporal en competencias como IEEE-CIS Fraud Detection.
- **Implementación:** Desarrollar Codificación bayesiana OOF estricta con regularización m-estimate de Dirichlet y adición de ruido gaussiano.

### [ ] SUPER-TAREA CMRE-104: Mitigación de UNSCALED_COUNT_FEATURE_LEAKAGE_AND_CONSTANT_SHIFT
- **Origen:** `FAIL_07` (Catálogo de fallos).
- **Problema:** Sobreajuste a conteos brutos no escalados que no generalizan al cambiar densidad de dispersión.
- **Implementación:** Implementar cálculo de desvíos relativos (Delta Trick) y normalización robusta intercuartílica (IQR).

### [ ] SUPER-TAREA CMRE-105: Mitigación de LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION
- **Origen:** `FAIL_08` (Catálogo de fallos).
- **Problema:** Cross-Entropy pura corrompiendo gradientes al forzar la red a memorizar ruido en etiquetas.
- **Implementación:** Implementar Label Smoothing, Bi-Tempered Loss o Soft-F1 con gradientes amortiguados para mitigar la penalización de outliers.

### [ ] SUPER-TAREA CMRE-106: Mitigación de NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE
- **Origen:** `FAIL_09` (Catálogo de fallos).
- **Problema:** Asignación de pesos fuertemente negativos en ensambles de modelos colineales resultando en predicciones fuera de rango.
- **Implementación:** Integrar Mínimos Cuadrados No Negativos (NNLS) forzando pesos w_i >= 0 y sum(w) = 1.0 en stacking.

### [ ] SUPER-TAREA CMRE-107: Mitigación de INVERSION_MONOCHROME_LUT_MISINTERPRETATION
- **Origen:** `FAIL_10` (Catálogo de fallos).
- **Problema:** Inversión de tejidos (blanco vs negro) por ignorar polaridad MONOCHROME en archivos radiológicos DICOM.
- **Implementación:** Implementar Decodificador DICOM canónico con verificación estricta de PhotometricInterpretation y normalización forzada a MONOCHROME2.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
