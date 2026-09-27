# 📋 JULES DYNAMIC SUPER-TASKS BACKLOG (MOTOR GENERAL AGNÓSTICO)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE v0.6.0)
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI
**Fuente de Verdad de Torneos:** [`ACTIVE_COMPETITIONS.json`](file:///C:/Users/rafae/.gemini/01_PROYECTOS/0072-cmre-engine/ACTIVE_COMPETITIONS.json)

---

## 🎯 PRÓXIMAS SUPER-TAREAS AUTÓNOMAS DE INGENIERÍA AGNÓSTICA (SESIÓN POST-CIERRE):

1. **SUPER-TAREA CMRE-10: Pipeline de Ingestión Tensional y Rescale en Float32 para `MOD_INGEST`**
   - **Contexto:** Post-mortem `FAIL_10` (MONOCHROME inversion) y `FAIL_13` (FP16 vs Double mismatch).
   - **Acción:** Extender `src/cmre/modules/ingest.py` para implementar una función `batch_process_dicoms` usando `concurrent.futures.ThreadPoolExecutor`. Debe asegurar la normalización estricta de metadatos de rescale (Slope/Intercept) convirtiendo siempre a `float32` antes de devolver el tensor, evitando los cuelgues (RuntimeError de PyTorch) observados en CUDA.

2. **SUPER-TAREA CMRE-11: Validadores Estrictos Multi-Centro con Purga Temporal en `MOD_SPLIT`**
   - **Contexto:** Post-mortem `FAIL_02` (Temporal Leakage) y `FAIL_05` (Patient Leakage).
   - **Acción:** Integrar en `src/cmre/modules/split.py` un `PurgedMultiCenterGroupSplit`. Esta función debe forzar que muestras del mismo paciente/centro se asignen siempre al mismo pliegue y garantizar que exista un "embargo temporal" estricto (cero solapamiento de ventanas en el tiempo) entre datos de entrenamiento y validación.

3. **SUPER-TAREA CMRE-12: Target Encoder Bayesiano Jerárquico en `MOD_SIGNAL`**
   - **Contexto:** Post-mortem `FAIL_06` (High Cardinality Leakage).
   - **Acción:** Mejorar `src/cmre/modules/signal.py` añadiendo un target encoder que funcione con múltiples niveles jerárquicos (ej: hospital -> escáner -> paciente) aplicando M-Estimate (Dirichlet) y garantizando que las estadísticas de grupo se extraigan de forma "out-of-fold" estricta para evitar sobreajuste.

4. **SUPER-TAREA CMRE-13: Vectorización Tanimoto y Aceleración SIMD en `MOD_HPC`**
   - **Contexto:** Reto `high_dimensional_decoys` de CASMI 2026.
   - **Acción:** Optimizar `src/cmre/modules/hpc.py` añadiendo un kernel rápido para el cálculo del coeficiente de similitud de Tanimoto sobre bitsets (ej. ECFP4 o Morgan). Implementar un fallback seguro si SIMD nativo falla, maximizando el throughput para reducir la latencia (enfocado en el presupuesto de 5.0s por muestra de CASMI).

5. **SUPER-TAREA CMRE-14: Reductores de Latencia Greedy y Poda de Ensambles en `MOD_ENSEMBLE`**
   - **Contexto:** Post-mortem `FAIL_12` (Latency Explosion, >6.5h en RSNA Knee).
   - **Acción:** Escribir en `src/cmre/modules/ensemble.py` un algoritmo de poda (Greedy Ensemble Pruning) asociado al `LatencyBudgetPruner`. Esta lógica analizará el presupuesto máximo de inferencia listado en `ACTIVE_COMPETITIONS.json` (ej: 1.5s/muestra para Knee) y cortocircuitará ramas pesadas del ensamble si se proyecta un timeout inminente.

6. **SUPER-TAREA CMRE-15: Auto-Generador de Fallbacks Anti-Identidad en AGI (`MOD_LOSS`/`MOD_ENSEMBLE`)**
   - **Contexto:** Post-mortem `FAIL_11` (Symbolic Timeout Identity Fallback en ARC).
   - **Acción:** Implementar un servicio transversal `anti_identity_guard_generator` que, en tareas de síntesis como ARC-AGI, analice los fallbacks del sistema. En lugar de devolver la matriz original ante un timeout, el sistema aplicará automáticamente transformaciones de cromatismo o topológicas seguras para evitar el 0 absoluto en evaluación.

7. **SUPER-TAREA CMRE-16: Sistema de Checkpoints Dinámicos OOM-Guard**
   - **Contexto:** Fugas y fallos crónicos de "Out of Memory" en iteraciones pesadas.
   - **Acción:** Desarrollar `src/cmre/services/oom_guard.py` que capture dinámicamente las excepciones `RuntimeError` originadas por saturación en VRAM de CUDA. Reducirá el batch-size automáticamente a la mitad, purgará la caché de PyTorch (`torch.cuda.empty_cache()`) y resumirá desde el último batch fallido sin romper el proceso global.

8. **SUPER-TAREA CMRE-17: Optimizador Universal Nelder-Mead para Asymmetric Loss**
   - **Contexto:** Post-mortem `FAIL_01` (Threshold Collapse).
   - **Acción:** Añadir en `src/cmre/services/auto_tune.py` un envoltorio para sintonización (Auto-Tune) de hiperparámetros. Usará un optimizador continuo simplex (Nelder-Mead) para calibrar el umbral óptimo de binarización basado en asimetría clínica, desplazándolo del umbral ingenuo `0.5` en problemas de extremado desbalance (<5% positivos).

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
