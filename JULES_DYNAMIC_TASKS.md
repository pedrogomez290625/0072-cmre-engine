# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Sesión de Desarrollo Agnóstico (7 de Octubre 2026) - Auto-Reescritura Avanzada
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo es reescrito por el motor tras el análisis de `ACTIVE_COMPETITIONS.json` y el `data/knowledge/postmortems_failures_catalog.json`. Su objetivo es proyectar las mitigaciones a las vulnerabilidades encontradas y potenciar los solvers de las competencias activas (RSNA Knee, CASMI, ARC-AGI).

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-56: Reconstrucción de Tiling de Mosaicos con Hanning (WSI)
- **Origen:** `FAIL_03` (MED_WSI_HANNING_TILER).
- **Problema:** En imágenes médicas de ultra-alta resolución (Gigapíxeles), la recombinación ingenua de mosaicos (tiling sin solapamiento) causa pérdida de contexto espacial en fronteras, generando discontinuidades en forma de cuadrícula y degradando la métrica Dice.
- **Implementación:** Construir en `MOD_INGEST` un Tiler de ventana separable 2D de Hanning, asegurando un solapamiento del 25% y reconstrucción suavizada ponderada.

### [ ] SUPER-TAREA CMRE-57: Target Encoder OOF Bayesiano Estricto
- **Origen:** `FAIL_06` (TARGET_ENCODING_HIGH_CARDINALITY_LEAKAGE).
- **Problema:** Calcular variables objetivo codificadas (Target Encoding) sin validación cruzada estricta genera fuga (leakage) masiva en variables de alta cardinalidad, colapsando el score en inferencia.
- **Implementación:** Implementar en `MOD_SIGNAL` un `BayesianOOFTargetEncoder` que procese estrcitamente Out-Of-Fold aplicando regularización m-estimate de Dirichlet y adición de ruido gaussiano para variables categóricas.

### [ ] SUPER-TAREA CMRE-58: Normalización Intercuartílica Robusta y Delta Trick
- **Origen:** `FAIL_07` (UNSCALED_COUNT_FEATURE_LEAKAGE_AND_CONSTANT_SHIFT).
- **Problema:** Los conteos brutos o features de densidad a menudo se sobreajustan a las distribuciones de un pliegue y fallan ante un dataset desplazado.
- **Implementación:** Añadir a `MOD_SIGNAL` un generador `DeltaTrickNormalizer` que convierta conteos directos en desvíos relativos y normalización intercuartílica (IQR) respecto a medias de grupos de control robustas.

### [ ] SUPER-TAREA CMRE-59: Suavizador de Etiquetas con Cross-Entropy Ponderada (Soft-F1)
- **Origen:** `FAIL_08` (LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION).
- **Problema:** La Cross-Entropy estándar forzaba a los modelos complejos a memorizar ruido en competencias con etiquetas de campo médicas de mala calidad (Cassava), corrompiendo gradientes.
- **Implementación:** Desarrollar en `MOD_LOSS` un mecanismo diferenciable de `WeightedSoftF1` y Label Smoothing con gradientes amortiguados para inmunizar la pérdida ante falsos positivos de anotadores.

### [ ] SUPER-TAREA CMRE-60: Ensamble de Mínimos Cuadrados No Negativos (NNLS)
- **Origen:** `FAIL_09` (NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE).
- **Problema:** En el stacking con Regresión Lineal Ordinaria, la multicolinealidad severa de modelos idénticos forzó coeficientes fuertemente negativos, causando pérdida infinita.
- **Implementación:** Desarrollar un `NNLSBlender` en `MOD_ENSEMBLE` que ajuste los meta-pesos forzando `w_i >= 0` y la restricción convexa euclidiana `sum(w) = 1.0` frente a modelos hiper-colineales.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
