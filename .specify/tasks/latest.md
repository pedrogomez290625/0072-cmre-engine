# 📋 TAREAS ATÓMICAS DE DESARROLLO (TASKS LATEST) - CMRE v0.5.0
### Proyecto: `0072-cmre-engine` (Competitive ML Reasoning Engine)
**Estado Actual:** 132/132 tests aprobados (100% en verde).
**Gobernanza:** Rafael "Rafa" Pérez & Angelus AGI
**Agente Autónomo en la Nube:** Jules (Google Cloud)

---

## 🟢 TAREAS COMPLETADAS (CORE & TOURNAMENTS V0.5.0):
- [x] **TASK-01:** Implementar modelos relacionales SQLModel con soporte para pgvector (`src/cmre/models.py`).
- [x] **TASK-02:** Implementar esquemas de validación Pydantic v2 para ProblemDNA, RankedClaim y ExperimentPlan (`src/cmre/schemas.py`).
- [x] **TASK-03:** Desarrollar conectores base para arXiv, GitHub, Hugging Face y Semantic Scholar (`src/cmre/connectors/`).
- [x] **TASK-04:** Implementar el motor de perfilado *Problem Profiler* con detección multi-modal (`src/cmre/services/problem_profiler.py`).
- [x] **TASK-05:** Implementar sistema de Scoring y función de decaimiento por recencia (`src/cmre/services/scoring.py`, `recency.py`).
- [x] **TASK-06:** Desarrollar el planificador en 6 fases *Experiment Planner* (`src/cmre/services/planner.py`).
- [x] **TASK-07:** Implementar la interfaz CLI interactiva con Typer y Rich (`src/cmre/cli.py`).
- [x] **TASK-08:** Suite de tests unitarios iniciales alcanzando 100% de éxito (`tests/`).
- [x] **TASK-S01:** Implementar `RSNAKneeSolver` con soporte multi-vista 2.5D (Sagital, Coronal, Axial) y 13 columnas oficiales (`src/cmre/solvers/rsna_knee_solver.py`).
- [x] **TASK-S02:** Implementar `ARCAGIHybridSolver` con arquitectura SDSI Leg C y Anti-Identity Fallback Guard (`src/cmre/solvers/arc_agi_hybrid_solver.py`).
- [x] **TASK-S03:** Implementar `EnvedaCASMISolver` con reglas SIRIUS de pérdidas neutras, Gated Library Anchor e InChIKey14 deduplication (`src/cmre/solvers/enveda_casmi_solver.py`).
- [x] **TASK-S04:** Desarrollar `ClassWiseAsymmetricBlender` y `LatencyBudgetPruner` (<2.0s por estudio) en `src/cmre/modules/ensemble.py`.
- [x] **TASK-S05:** Implementar `SubmissionIntegrityValidator` con auditoría de schemas multilabel y JSONs de ARC-AGI-2 (`src/cmre/services/submission_validator.py`).
- [x] **TASK-S06:** Integrar base de conocimiento con 60 claims (C31-C36 añadidos) y 14 fallos postmortem (FAIL_11 a FAIL_14).

---

## 🚀 TAREAS PRIORITARIAS PARA JULES (FASE EVOLUTIVA):
- [ ] **TASK-09 (Kaggle Discussion & Solution Writeups Connector):**
  - **Objetivo:** Desarrollar `src/cmre/connectors/kaggle_writeups.py` para parsear hilos y writeups ganadores de soluciones Kaggle (Top 1 a 5).
  - **Requerimiento:** Extraer secciones de CV scheme, feature engineering, arquitectura, loss y ensemble. Retornar objetos `ScrapedResource` tipados.
  - **Test:** Crear `tests/test_kaggle_writeups.py` con mocks de respuestas HTML/JSON de Kaggle Forum.

- [ ] **TASK-10 (Catálogo Estructurado de Problem DNA para Torneos 2026):**
  - **Objetivo:** Crear archivos JSON de Problem DNA en `data/competitions/`:
    - `rsna_knee_2026.json` (Visión médica 2.5D, desbalance severo, AUC macro-promediado).
    - `enveda_casmi_2026.json` (MS/MS espectrometría, ranking MRR@25, quimioinformática).
    - `arc_prize_2026.json` (Razonamiento discreto AGI, sintesis DSL, TTT).
  - **Test:** Verificar con `test_problem_profiler.py` que el motor infiere automáticamente los 6 módulos canónicos correctos para cada torneo.

- [ ] **TASK-11 (Google Drive & Google Apps Script Continuous Bridge):**
  - **Objetivo:** Extender `scripts/gdrive_hub.py` para sincronizar automáticamente nuevos claims y postmortems generados por Jules hacia Google Sheets y Google Drive.
  - **Test:** `tests/test_gdrive_hub_mock.py` con requests mockeados al endpoint de GAS.

- [ ] **TASK-12 (Extractor AST de Módulos PyTorch):**
  - **Objetivo:** Construir `src/cmre/services/ast_extractor.py` usando el módulo `ast` de Python para descomponer notebooks y scripts ganadores en funciones/clases correspondientes a los 6 módulos canónicos (`MOD_INGEST` a `MOD_ENSEMBLE`).
  - **Test:** Crear `tests/test_ast_extractor.py` validando la extracción sobre scripts de ejemplo.

- [ ] **TASK-13 (Suite de Benchmark Sintético para Solvers):**
  - **Objetivo:** Crear `tests/test_solvers_benchmarks.py` que genere volúmenes sintéticos de resonancia y espectros de prueba, evaluando latencia, precisión y comportamiento de los solvers `RSNAKneeSolver`, `EnvedaCASMISolver` y `ARCAGIHybridSolver`.
  - **Aceptación:** 100% de tests pasando en <5 segundos.

---

## 🛑 REGLAS DE ORO PARA JULES:
1. Ninguna tarea debe romper los 132 tests existentes.
2. Toda nueva funcionalidad debe incluir su test unitario en `tests/`.
3. Prohibido eliminar código o datos existentes (Axioma de No Borrado).
4. Abrir PR con título format: `feat(jules): [TASK-ID] <descripción breve>`.
