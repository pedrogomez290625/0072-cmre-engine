# 📋 TAREAS ATÓMICAS DE DESARROLLO (TASKS LATEST)
### Proyecto: `0072-cmre-engine`
**Estado Actual:** 68/68 tests aprobados (100% en verde).

---

## 🟢 TAREAS COMPLETADAS (CORE BASELINE):
- [x] **TASK-01:** Implementar modelos relacionales SQLModel con soporte para pgvector (`src/cmre/models.py`).
- [x] **TASK-02:** Implementar esquemas de validación Pydantic v2 para ProblemDNA, RankedClaim y ExperimentPlan (`src/cmre/schemas.py`).
- [x] **TASK-03:** Desarrollar conectores base para arXiv, GitHub, Hugging Face y Semantic Scholar (`src/cmre/connectors/`).
- [x] **TASK-04:** Implementar el motor de perfilado *Problem Profiler* con detección multi-modal (`src/cmre/services/problem_profiler.py`).
- [x] **TASK-05:** Implementar sistema de Scoring y función de decaimiento por recencia (`src/cmre/services/scoring.py`, `recency.py`).
- [x] **TASK-06:** Desarrollar el planificador en 6 fases *Experiment Planner* (`src/cmre/services/planner.py`).
- [x] **TASK-07:** Implementar la interfaz CLI interactiva con Typer y Rich (`src/cmre/cli.py`).
- [x] **TASK-08:** Crear suite de 68 tests unitarios alcanzando 100% de éxito (`tests/`).

---

## 🚀 TAREAS PENDIENTES PARA JULES (FASE EVOLUTIVA):
- [ ] **TASK-09 (Kaggle Discussion Connector):** Desarrollar `src/cmre/connectors/kaggle_writeups.py` para extraer hilos de soluciones ganadoras (Top 1 a 5) desde la API de Kaggle y parsear secciones de validación, features, modelos y post-procesamiento.
- [ ] **TASK-10 (Perfilado de Enveda CASMI 2026):** Crear el archivo de configuración `data/competitions/enveda_casmi_2026.json` con el ADN específico de la competencia de espectrometría de masas y validar que el motor genere el plan de 6 fases adaptado a química molecular.
- [ ] **TASK-11 (Sincronizador Google Drive Bridge):** Implementar script `scripts/sync_drive_knowledge.py` para exportar automáticamente claims y postmortems hacia `G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\knowledge_db\`.
- [ ] **TASK-12 (Anotador AST de Submódulos):** Construir `src/cmre/services/ast_extractor.py` para descomponer funciones y clases PyTorch de notebooks ganadores en los 6 bloques canónicos (`MOD_INGEST` a `MOD_ENSEMBLE`).
- [ ] **TASK-13 (Evaluación Continua y Benchmarks):** Integrar script para evaluar la calidad de los claims recomendados contra los casos reales de prueba en `data/golden_cases/`.
