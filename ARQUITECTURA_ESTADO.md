# 🏛️ ARQUITECTURA Y ESTADO VIGENTE DEL REPOSITORIO
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Versión:** 1.0.0
**Estado:** STAGE_14_AUTO_EVOLUTION_COMPLETED 🟢 (100% Tests Pasando: 170/170)
**Última Auditoría:** 4 de Octubre de 2026
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Victoria Perez

---

## 📊 1. RESUMEN DE COBERTURA Y SALUD
- **Tests Unitarios:** 170/170 pasados (100% de éxito en pytest).
- **Herramienta de Construcción:** `pyproject.toml` (PEP 621) + `uv.lock`.
- **Smoke Test:** Verificado (60 claims metodológicas, forenses y HPC, 8 reportes de torneo generados con templates canónicos).
- **Base de Datos Resiliente:** `src/cmre/db.py` con fallback automático a SQLite standalone (`sqlite:///data/cmre.db`) ante desconexión de PostgreSQL.
- **Validación Cloud GPU (Google Colab / Kaggle T4):** Tesla T4 verificada (Asymmetric Loss CUDA: 5.29 ms/iteración; Mammo ROI crop: 28.73 ms; Tanimoto popcount: 107.23 ms; Inferencia multi-vista RSNA Knee: 1.86s).
- **Almacén Google Drive:** Sincronizado en `G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\`.
- **GitHub:** [https://github.com/perezernestorafael933/0072-cmre-engine](https://github.com/perezernestorafael933/0072-cmre-engine).

---

## 📂 2. INVENTARIO DE MÓDULOS ACTIVOS

### Núcleo de Razonamiento y Servicios (`src/cmre/services/`)
- **`src/cmre/models.py`:** Esquemas relacionales SQLModel con soporte para pgvector (`Mechanism`, `Technique`, `Claim`, `Failure`, `ProblemProfile`, `Experiment`).
- **`src/cmre/schemas.py`:** Modelos Pydantic v2 inmutables para tipado de entrada y salida (`CompetitionInput`, `ProblemDNA`, `RankedClaim`, `ExperimentPlan`).
- **`src/cmre/services/seeder_claims.py`:** Sembrador de 60 claims (36 canónicas + 14 forenses + 10 HPC extraídas de torneos mundiales 2026).
- **`src/cmre/services/submission_validator.py`:** Guardián universal pre-envío con soporte CSV, multi-etiqueta (RSNA Knee 12 clases) y validación estricta de JSON ARC-AGI con detector de colapso por identidad (`anti_identity_collapse`).
- **`src/cmre/services/problem_profiler.py`:** Extractor de ADN de problemas competitivos con `load_active_competitions` dinámico (SUPER-TAREA CMRE-06 Completada).
- **`src/cmre/services/ast_extractor.py`:** Extractor y clasificador de AST para destilar soluciones competitivas en componentes CMRE.
- **`src/cmre/connectors.py`:** Conectores robustos (ej. KaggleWriteupConnector) para ingestión de discusiones de torneos.
- **`src/cmre/services/scoring.py` y `recency.py`:** Algoritmos de scoring multidimensional y decaimiento temporal.
- **`src/cmre/services/planner.py`:** Planificador en 6 fases competitivas integrando los 6 módulos canónicos.
- **`src/cmre/services/reporter.py`:** Generador de reportes de torneo exhaustivos en Markdown.
- **`src/cmre/cli.py`:** CLI interactivo con Typer y Rich (`cmre plan`, `cmre seed`, `cmre profile`).

### Los Módulos Canónicos de Ingeniería (`src/cmre/modules/`)
1. **`src/cmre/modules/ingest.py` (`MOD_INGEST`):** Ingesta física DICOM, aplicación estricta de Modality/VOI LUT, MONOCHROME1 inversion y recorte morfológico de ROI tisular.
2. **`src/cmre/modules/signal.py` (`MOD_SIGNAL`):** Agregaciones jerárquicas delta (`feature - mean_group`), Target Encoder Bayesiano out-of-fold y arbitraje híbrido SDSI.
3. **`src/cmre/modules/split.py` (`MOD_SPLIT`):** Particiones con cero fuga: K-Fold Disjunto por Grupos (`group_disjoint_kfold`), Series Temporales Purgadas con embargo (`purged_timeseries_split`), Scaffold Molecular Bemis-Murcko (`molecular_scaffold_split`), y alineamiento Dynamic Time-Warping CV (`DTWPurgedTimeSeriesSplit`, CMRE-29).
4. **`src/cmre/modules/loss.py` (`MOD_LOSS`):** Asymmetric Loss (`asymmetric_loss_numpy`), Soft-F1 diferenciable, módulos PyTorch `AsymmetricLoss` y `SoftF1Loss`, y el Meta-Controlador de Paradas Tempranas Múltiples (`MultiMetricEarlyStopping`, CMRE-28).
5. **`src/cmre/modules/ensemble.py` (`MOD_ENSEMBLE`):** Ensamble con regresión no-negativa NNLS (`SimpleNNLSBlender`), promediado de rangos percentiles (`rank_average_predictions`), **Class-Wise Asymmetric Matrix Blending** (`ClassWiseAsymmetricBlender`) y poda greedy por presupuesto de tiempo (`LatencyBudgetPruner`).
6. **`src/cmre/modules/hpc.py` (`MOD_HPC`):** Optimización a nivel de silicio: Popcount de bitsets de alta dimensión (`BitsetFingerprint`) y Disjoint Set Union (`DisjointSetUnion`) con compresión de caminos.
7. **`src/cmre/modules/ood.py` (`MOD_OOD`):** Detección Z-score based OOD (`OODDetector`) contra regresiones de distribución (implementación CMRE-25).
8. **`src/cmre/modules/registry.py`:** Mapeo determinista entre IDs de claims (`C01`-`C36`, `FC01`-`FC14`, `HPC01`-`HPC10`) y código ejecutable.

---

## 🏆 3. SUITE DE LOS 7 SOLVERS CANÓNICOS (`src/cmre/solvers/`)
1. **`RSNAKneeSolver` (`rsna_knee_solver.py`):** Inferencia multi-vista 2.5D MRI (Sagital, Coronal, Axial), Asymmetric Matrix Blending ($12 \times 4$), sanitización Float vs Double para FP16 CUDA y Macro ROC-AUC.
2. **`ArcAgiHybridSolver` (`arc_agi_hybrid_solver.py`):** Arquitectura SDSI Leg C: inducción simbólica en pares de entrenamiento (intento 1) + modelo neuronal TTT con aumentaciones $D_8$ (intento 2) con guardián anti-identidad que inmuniza contra scores 0.00.
3. **`EnvedaCasmiSolver` (`enveda_casmi_solver.py`):** Pipeline V3 SOTA: Tanimoto acelerado por Bitsets, filtro biofísico SIRIUS (Axioma de Ausencia de pérdidas neutras), Gated Library Anchor (Rank 1 Shield para cosenos $\ge 0.85$) y deduplicación tautomérica InChIKey14.
4. **`RSNAMammographySolver` (`rsna_mammography_solver.py`):** Pipeline mamográfico DICOM con ROI crop tisular y optimización simplex Nelder-Mead de umbrales pF1.
5. **`ISICMelanomaSolver` (`isic_melanoma_solver.py`):** Detección de lesiones melanocíticas con normalización delta de paciente y optimización de pAUC a 80% TPR.
6. **`RichtersPredictorSolver` (`richters_predictor_solver.py`):** Clasificación ordinal sísmica con fronteras de decisión calibradas vía Nelder-Mead.
7. **`ZindiAirQoSolver` (`zindi_airqo_solver.py`):** Regresión espacio-temporal purgada con features de retardo horario y ensamble de gradiente + KNN.

---

## 🛡️ 4. CATÁLOGO DE AUTOPSIAS (WALL OF SHAME - 14 CASOS)
- **`FAIL_01` a `FAIL_10`:** Desalineación de umbrales pF1, fuga temporal por autocorrelación, discontinuidad de bordes en WSI histopatológicas, memorización de scaffolds, multicolinealidad negativa OLS, inversión errónea MONOCHROME1.
- **`FAIL_11`:** Colapso a score 0.00 en ARC-AGI-2 por escape simbólico hacia grilla idéntica a la entrada. (Mitigación actual en pipeline: Guardián Anti-Identidad + TTT D8).
- **`FAIL_12`:** Explosión de latencia en RSNA Knee (>6.5h) por ensamble upstream de 30+ modelos. (Mitigación actual: `LatencyBudgetPruner` a tríada quirúrgica en 1.86s).
- **`FAIL_13`:** Aborto en CUDA por colisión de tipos `Half vs Double` al usar constantes de normalización en FP16. (Mitigación en radar: `sanitize_tensor_dtypes`).
- **`FAIL_14`:** Saturación de decoys en CASMI por búsqueda ciega en 400k moléculas sin filtro de pérdidas neutras. (Mitigación actual: Axioma de Ausencia SIRIUS).

## 🚀 5. CAPACIDADES DE AUTO-EVOLUCIÓN
- **Motor de Benchmarking Universal:** Pruebas unitarias extendidas (155 pruebas) cubriendo extracción AST, perfilado JSON de torneos, constructores robustos de módulos (Loss, Split, Ingest, HPC) y simulación multi-modelo. Integrado exhaustivamente para prevenir regresiones.
- **Generador Dinámico de Tareas:** El motor analiza en tiempo real `ACTIVE_COMPETITIONS.json` y postmortems históricos para autoproyectar su evolución a través de `JULES_DYNAMIC_TASKS.md`, abordando vulnerabilidades sistémicas antes de la inferencia en producción y permitiendo reescritura constante de su backlog de ingeniería.

## 🌟 6. ACTUALIZACIONES RECIENTES (v1.0.0+)
- **Módulos Avanzados (CMRE-25, CMRE-28, CMRE-29)**: Integración de `OODDetector` para validación OOD (CMRE-25), `MultiMetricEarlyStopping` para paradas tempranas seguras (CMRE-28), y `DTWPurgedTimeSeriesSplit` para robustez temporal dinámica (CMRE-29).
- **AntiIdentityGuard**: Implementado en `src/cmre/services/submission_validator.py` para prevenir colapsos a 0.00 en Kaggle ARC-AGI, forzando transformaciones geométricas (D8) y cromáticas deterministas frente a inferencias idénticas a la entrada (Postmortem FAIL_11).
- **Google Drive Continuous Bridge**: Herramienta CLI (`scripts/gdrive_hub.py`) ahora incluye comando `sync` que transfiere `claims_cmre.json` y `postmortems_failures_catalog.json` directo a la nube.
- Pruebas incrementadas garantizando cobertura en las mitigaciones (100% de tests pasando de forma aislada, un total de 170/170 pasados).

---
- **Super-Tareas Resolutivas (CMRE-41 a CMRE-45)**: Integración de `AntiIdentityGuard` y TTT D8 en `MOD_OOD`/`SubmissionValidator` (CMRE-41), `LatencyBudgetPruner` multi-flujo dinámico en `MOD_ENSEMBLE` (CMRE-42), Sanitizador Universal FP16/FP64 en `MOD_HPC` (CMRE-43), Optimizador SIRIUS unificado en `MOD_OOD` (CMRE-44) y Controlador Multi-Vista Ortogonal en `MOD_ENSEMBLE` (CMRE-45). Incremento a 170 tests unitarios cubriendo los componentes.

- **Super-Tareas Resolutivas (CMRE-36 a CMRE-40)**: Integración de `NelderMeadThresholdOptimizer` en MOD_ENSEMBLE (CMRE-36), `OOFTargetEncoder` en MOD_SIGNAL (CMRE-37), `BiTemperedLogisticLoss` en MOD_LOSS (CMRE-38), `NonNegativeLeastSquaresBlender` forzando ensamble simplex positivo en MOD_ENSEMBLE (CMRE-39) y `StrictDicomLUTDecoder` como decodificador seguro MONOCHROME2 en MOD_INGEST (CMRE-40). Incremento a 170 tests unitarios cubriendo los componentes.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa") & Victoria Perez

## 🚀 7. EVOLUCIÓN DINÁMICA FINAL Y BENCHMARKING (4 de Octubre de 2026)
- **Benchmarking Universal:** Validación del motor con suite de 170/170 tests pasando (0 regresiones).
- **Auto-Reescritura Dinámica:** Integrada la reescritura de `JULES_DYNAMIC_TASKS.md` como mecanismo nativo del motor, proyectando las nuevas super-tareas (CMRE-41 a CMRE-45) basadas en análisis cruzado de `ACTIVE_COMPETITIONS.json` y `postmortems_failures_catalog.json` para resolución de debilidades de la competencia y desafíos específicos en visión 2.5D, metabolómica y AGI (Severe Class Imbalance, Latency Budgets, Zero-Shot Generalization).

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa")
