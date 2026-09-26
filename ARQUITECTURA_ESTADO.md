# 🏛️ ARQUITECTURA Y ESTADO VIGENTE DEL REPOSITORIO
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Versión:** 0.5.0  
**Estado:** STAGE_6_SOTA_TRIAD_AND_ANTI_COLLAPSE 🟢 (100% Tests Pasando: 135/135)
**Última Auditoría:** 26 de Septiembre de 2026
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI  

---

## 📊 1. RESUMEN DE COBERTURA Y SALUD
- **Tests Unitarios:** 135/135 pasados (100% de éxito en pytest).
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
- **`src/cmre/services/problem_profiler.py`:** Extractor de ADN de problemas competitivos.
- **`src/cmre/services/scoring.py` y `recency.py`:** Algoritmos de scoring multidimensional y decaimiento temporal.
- **`src/cmre/services/planner.py`:** Planificador en 6 fases competitivas integrando los 6 módulos canónicos.
- **`src/cmre/services/reporter.py`:** Generador de reportes de torneo exhaustivos en Markdown.
- **`src/cmre/cli.py`:** CLI interactivo con Typer y Rich (`cmre plan`, `cmre seed`, `cmre profile`).

### Los Módulos Canónicos de Ingeniería (`src/cmre/modules/`)
1. **`src/cmre/modules/ingest.py` (`MOD_INGEST`):** Ingesta física DICOM, aplicación estricta de Modality/VOI LUT, MONOCHROME1 inversion y recorte morfológico de ROI tisular.
2. **`src/cmre/modules/signal.py` (`MOD_SIGNAL`):** Agregaciones jerárquicas delta (`feature - mean_group`), Target Encoder Bayesiano out-of-fold y arbitraje híbrido SDSI.
3. **`src/cmre/modules/split.py` (`MOD_SPLIT`):** Particiones con cero fuga: K-Fold Disjunto por Grupos (`group_disjoint_kfold`), Series Temporales Purgadas con embargo (`purged_timeseries_split`) y Scaffold Molecular Bemis-Murcko (`molecular_scaffold_split`).
4. **`src/cmre/modules/loss.py` (`MOD_LOSS`):** Asymmetric Loss (`asymmetric_loss_numpy`), Soft-F1 diferenciable y módulos PyTorch `AsymmetricLoss` y `SoftF1Loss` analíticamente validados con `torch.autograd.gradcheck` para desbalance médico extremo (SUPER-TAREA CMRE-01 Completada).
5. **`src/cmre/modules/ensemble.py` (`MOD_ENSEMBLE`):** Ensamble con regresión no-negativa NNLS (`SimpleNNLSBlender`), promediado de rangos percentiles (`rank_average_predictions`), **Class-Wise Asymmetric Matrix Blending** (`ClassWiseAsymmetricBlender`) y poda greedy por presupuesto de tiempo (`LatencyBudgetPruner`).
6. **`src/cmre/modules/hpc.py` (`MOD_HPC`):** Optimización a nivel de silicio: Popcount de bitsets de alta dimensión (`BitsetFingerprint`) y Disjoint Set Union (`DisjointSetUnion`) con compresión de caminos.
7. **`src/cmre/modules/registry.py`:** Mapeo determinista entre IDs de claims (`C01`-`C36`, `FC01`-`FC14`, `HPC01`-`HPC10`) y código ejecutable.

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
- **`FAIL_11` (NUEVO):** Colapso a score 0.00 en ARC-AGI-2 por escape simbólico hacia grilla idéntica a la entrada. (Mitigación: Guardián Anti-Identidad + TTT D8).
- **`FAIL_12` (NUEVO):** Explosión de latencia en RSNA Knee (>6.5h) por ensamble upstream de 30+ modelos. (Mitigación: `LatencyBudgetPruner` a tríada quirúrgica en 1.86s).
- **`FAIL_13` (NUEVO):** Aborto en CUDA por colisión de tipos `Half vs Double` al usar constantes de normalización en FP16. (Mitigación: `sanitize_tensor_dtypes`).
- **`FAIL_14` (NUEVO):** Saturación de decoys en CASMI por búsqueda ciega en 400k moléculas sin filtro de pérdidas neutras. (Mitigación: Axioma de Ausencia SIRIUS).

---
[VINCIT_OMNIA_VERITAS]
