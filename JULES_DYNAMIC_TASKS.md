# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Sesión Final de Cierre y Benchmarking (4 de Octubre 2026) - Auto-Reescritura
**Autor:** Perez, Ernesto Rafael ("Rafa") & Victoria Perez

Este archivo es reescrito por el motor tras el análisis de `ACTIVE_COMPETITIONS.json` y el `data/knowledge/postmortems_failures_catalog.json`. Su objetivo es proyectar las mitigaciones a las vulnerabilidades encontradas y potenciar los solvers de las competencias activas (RSNA Knee, CASMI, ARC-AGI).

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [x] SUPER-TAREA CMRE-41: Guardián Anti-Identidad con Test-Time Training (TTT) Expandido
- **Origen:** Postmortem `FAIL_11` (ARC Prize 2026 - Colapso Simbólico de Identidad).
- **Problema:** En ARC-AGI, los motores simbólicos pueden agotar el tiempo y conmutar a un fallback que devuelve la entrada sin modificar, lo cual garantiza un 0 de precisión ya que la salida nunca es igual a la entrada.
- **Implementación:** Refinar el guardián anti-identidad en `src/cmre/services/submission_validator.py` o `MOD_OOD`. Implementar un módulo unificado de transformaciones (aumentaciones $D_8$ completas y variaciones topológicas) asegurando divergencia cromática y geométrica ante cualquier fallback que intente colapsar a identidad pura.

### [x] SUPER-TAREA CMRE-42: Limitador de Presupuesto de Latencia Multi-Flujo
- **Origen:** Postmortem `FAIL_12` (RSNA Knee 2026 - Explosión de Latencia de Ensamble).
- **Problema:** Ensambles complejos upstream con 30+ modelos violan los límites de Kaggle de 9 horas, causando fallas en el envío privado.
- **Implementación:** Ampliar `LatencyBudgetPruner` en `MOD_ENSEMBLE` para actuar como un controlador de latencia que pueda abortar dinámicamente o aplicar poda *greedy* sobre rutas de cómputo en `RSNAKneeSolver` y otras arquitecturas densas en caso de superar el presupuesto seguro por muestra.

### [x] SUPER-TAREA CMRE-43: Sanitizador Universal de Tipos Mixtos CUDA (FP16/FP64)
- **Origen:** Postmortem `FAIL_13` (RSNA Knee 2026 - Discordancia de Doble Precisión FP16/FP64).
- **Problema:** Constantes de normalización originadas en NumPy (`float64`) crashean CUDA al interactuar sin sanitizar con operaciones `torch.autocast` (`half`/`float16`).
- **Implementación:** Agregar una utilidad general de sanitización en `MOD_HPC` o `MOD_INGEST` que inspeccione automáticamente el Dtype de todos los tensores y diccionarios de buffers cruzando la frontera NumPy/PyTorch hacia PyTorch/CUDA FP16, asegurando que las constantes estén forzadas a `float32` antes del auto-casteo de precisión mixta.

### [x] SUPER-TAREA CMRE-44: Optimizador Universal del Axioma de Ausencia SIRIUS (Filtro Neutro Biofísico)
- **Origen:** Postmortem `FAIL_14` (Enveda CASMI 2026 - Sobrecarga de Decoys y Falsa Identidad).
- **Problema:** Buscar coincidencias de espectros masivos filtrando solo por la delta de masa permite que decoys moleculares sin sentido biológico monopolicen el Top-K MRR@25.
- **Implementación:** Generalizar el filtro SIRIUS del Axioma de Ausencia en `MOD_OOD` o un nuevo espacio quimio-biológico que penalice severamente compuestos que, dadas ciertas pérdidas neutras obligatorias en MS/MS (ej. H2O o CO2), no contengan los átomos fundamentales esperados (ej. Oxígeno).

### [x] SUPER-TAREA CMRE-45: Controlador Multi-Vista Ortogonal Robusto (Multi-View Alignment)
- **Origen:** `ACTIVE_COMPETITIONS.json` (RSNA Knee 2026 - Desafíos de Alineamiento Ortogonal y Desbalance Severo).
- **Problema:** En estudios médicos con múltiples vistas (Sagital, Coronal, Axial), los modelos pueden sobreajustarse o fracasar si no se unifican las predicciones ponderadas por la calidad y relevancia de cada vista.
- **Implementación:** Diseñar un pipeline agnóstico en `MOD_ENSEMBLE` que combine e intercale matrices de atención para entradas multi-vista estructuradas, combinándose opcionalmente con el ya implementado `NelderMeadThresholdOptimizer` para mitigar el desbalance extremo multietiqueta.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa") & Victoria Perez
