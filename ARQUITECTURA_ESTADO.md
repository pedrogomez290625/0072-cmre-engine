# 🏛️ ARQUITECTURA Y ESTADO VIGENTE DEL REPOSITORIO
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Versión:** 0.4.0
**Estado:** STAGE_5_CANONICAL_MODULES_AND_HPC 🟢 (100% Tests Pasando: 85/85)
**Última Auditoría:** 21 de Septiembre de 2026
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI

---

## 📊 1. RESUMEN DE COBERTURA Y SALUD
- **Tests Unitarios:** 85/85 pasados (100% de éxito en pytest).
- **Herramienta de Construcción:** `pyproject.toml` (PEP 621) + `uv.lock`.
- **Smoke Test:** Verificado (89 claims en SQLite/Postgres, 7 reportes de torneo generados con templates canónicos).
- **Base de Datos Resiliente:** `src/cmre/db.py` con fallback automático a SQLite standalone (`sqlite:///data/cmre.db`) ante desconexión de PostgreSQL.
- **Validación Cloud GPU (Google Colab):** Tesla T4 verificada (Asymmetric Loss CUDA: 5.29 ms/iteración; Mammo ROI crop: 28.73 ms; Tanimoto popcount: 107.23 ms).
- **Almacén Google Drive:** Sincronizado en `G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\`.
- **GitHub:** [https://github.com/perezernestorafael933/0072-cmre-engine](https://github.com/perezernestorafael933/0072-cmre-engine).

---

## 📂 2. INVENTARIO DE MÓDULOS ACTIVOS

### Núcleo de Razonamiento y Servicios (`src/cmre/services/`)
- **`src/cmre/models.py`:** Esquemas relacionales SQLModel con soporte para pgvector (`Mechanism`, `Technique`, `Claim`, `Failure`, `ProblemProfile`, `Experiment`).
- **`src/cmre/schemas.py`:** Modelos Pydantic v2 inmutables para tipado de entrada y salida (`CompetitionInput`, `ProblemDNA`, `RankedClaim`, `ExperimentPlan`).
- **`src/cmre/services/seeder_claims.py`:** Sembrador de 89 claims (35 canónicas + 54 forenses/HPC extraídas de Kaggle Septiembre).
- **`src/cmre/services/problem_profiler.py`:** Extractor de ADN de problemas competitivos.
- **`src/cmre/services/scoring.py` y `recency.py`:** Algoritmos de scoring multidimensional y decaimiento temporal.
- **`src/cmre/services/planner.py`:** Planificador en 6 fases competitivas integrando los 6 módulos canónicos.
- **`src/cmre/services/reporter.py`:** Generador de reportes de torneo exhaustivos en Markdown.
- **`src/cmre/cli.py`:** CLI interactivo con Typer y Rich (`cmre plan`, `cmre seed`, `cmre profile`).

### Los 6 Módulos Canónicos de Ingeniería (`src/cmre/modules/`)
1. **`src/cmre/modules/ingest.py` (`MOD_INGEST`):** Ingesta física DICOM, aplicación estricta de Modality/VOI LUT, MONOCHROME1 inversion y recorte morfológico de ROI tisular mamario.
2. **`src/cmre/modules/signal.py` (`MOD_SIGNAL`):** Agregaciones jerárquicas delta (`feature - mean_group`) y Target Encoder Bayesiano out-of-fold con regularización m-estimate.
3. **`src/cmre/modules/split.py` (`MOD_SPLIT`):** Estrategias de partición con cero fuga: K-Fold Disjunto por Grupos (`group_disjoint_kfold`), Series Temporales Purgadas (`purged_timeseries_split`) y Scaffold Molecular Bemis-Murcko (`molecular_scaffold_split`).
4. **`src/cmre/modules/loss.py` (`MOD_LOSS`):** Funciones de pérdida asimétricas optimizadas (`asymmetric_loss_numpy`, `soft_f1_score_numpy`) y módulo PyTorch `AsymmetricLoss` para desbalance extremo.
5. **`src/cmre/modules/ensemble.py` (`MOD_ENSEMBLE`):** Ensamble con regresión no-negativa NNLS (`SimpleNNLSBlender`) y promediado de rangos percentiles (`rank_average_predictions`).
6. **`src/cmre/modules/hpc.py` (`MOD_HPC`):** Optimización a nivel de silicio: Popcount de bitsets de alta dimensión (`BitsetFingerprint`) y Disjoint Set Union (`DisjointSetUnion`) con compresión de caminos.
7. **`src/cmre/modules/registry.py`:** Registro y mapeo determinista por expresiones regulares exactas entre IDs de claims (`C01`-`C35`, `FC01`-`FC14`, `HPC01`-`HPC10`) y código ejecutable.

---
[VINCIT_OMNIA_VERITAS]
