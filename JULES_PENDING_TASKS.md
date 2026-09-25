# 📜 JULES PENDING TASKS (MEMORIA CONTINUA Y EVOLUTIVA) - CMRE v0.5.0
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Investigador Principal:** Rafael "Rafa" Pérez & Angelus AGI
**Estado Actual:** 132/132 tests aprobados (100% en verde)
**Cuenta GitHub Oficial:** `pedrogomez290625` (https://github.com/pedrogomez290625/0072-cmre-engine)

---

## 📌 ESTADO DE TAREAS INCREMENTALES Y EVOLUTIVAS PARA JULES

Jules DEBE consultar `ARQUITECTURA_ESTADO.md` y `.specify/tasks/latest.md` al iniciar cada sesión para conocer qué módulos ya están creados y enfocar su trabajo en expandir, refactorizar y verificar el código sin duplicaciones.

### 🟢 TAREAS COMPLETADAS EN FASES 1 Y 2 (CORE & SOLVERS V0.5.0):
- [x] **INICIALIZACIÓN DEL MOTOR:** Modelos SQLModel, schemas Pydantic v2, CLI y suite core (`src/cmre/`).
- [x] **SOLVERS CANÓNICOS ACTIVOS:**
  - `RSNAKneeSolver`: Multi-vista 2.5D, 13 columnas oficiales, `ClassWiseAsymmetricBlender` 12x4, `LatencyBudgetPruner`.
  - `ARCAGIHybridSolver`: SDSI Leg C (simbólico DSL + TTT neural), Anti-Identity Fallback Guard.
  - `EnvedaCASMISolver`: V3 SOTA, reglas SIRIUS de pérdidas neutras, Gated Library Anchor, InChIKey14 deduplication.
- [x] **VALIDADOR DETERMINISTA:** `SubmissionIntegrityValidator` con auditoría de schemas multilabel y JSONs de ARC.
- [x] **SUITE DE PRUEBAS:** 132 tests unitarios pasando al 100% en verde.
- [x] **ALMACÉN EN GOOGLE DRIVE & APPS SCRIPT:** `scripts/gdrive_hub.py` y sincronización a Drive activa.
- [x] **CI/CD GITHUB ACTIONS:** Configurado en `pedrogomez290625/0072-cmre-engine` con test suite automática y auto-merge.

---

### 🚀 TAREAS PRIORITARIAS PARA JULES (FASE 3 & EVOLUCIÓN AUTÓNOMA):

- [ ] **TASK-09 (Kaggle Discussion & Solution Writeups Connector):**
  - Implementar conector `src/cmre/connectors/kaggle_writeups.py` para ingestar automáticamente las discusiones ganadoras de competencias concluidas y extraer secciones de validación, CV y arquitectura.
  - Test unitario: `tests/test_kaggle_writeups.py`.

- [ ] **TASK-10 (Problem DNA Competitions Catalog):**
  - Crear archivos JSON de Problem DNA en `data/competitions/`:
    - `rsna_knee_2026.json` (Visión médica 2.5D, desbalance severo, AUC macro-promediado).
    - `enveda_casmi_2026.json` (MS/MS espectrometría, ranking MRR@25, quimioinformática).
    - `arc_prize_2026.json` (Razonamiento discreto AGI, síntesis DSL, TTT).
  - Test: verificar inferencia de los 6 módulos canónicos correctos para cada torneo.

- [ ] **TASK-11 (Puente Continuo Google Drive & Apps Script):**
  - Extender `scripts/gdrive_hub.py` para sincronizar automáticamente nuevos claims y postmortems generados por Jules hacia Google Sheets y Google Drive.
  - Test unitario mockeado en `tests/test_gdrive_hub_mock.py`.

- [ ] **TASK-12 (Extractor AST de Módulos PyTorch):**
  - Construir `src/cmre/services/ast_extractor.py` usando el módulo `ast` de Python para descomponer notebooks y scripts ganadores en funciones/clases correspondientes a los 6 módulos canónicos (`MOD_INGEST` a `MOD_ENSEMBLE`).
  - Test unitario en `tests/test_ast_extractor.py`.

- [ ] **TASK-13 (Suite de Benchmark Sintético para Solvers):**
  - Crear `tests/test_solvers_benchmarks.py` que genere volúmenes sintéticos de resonancia y espectros de prueba, evaluando latencia, precisión y comportamiento de los solvers `RSNAKneeSolver`, `EnvedaCASMISolver` y `ARCAGIHybridSolver`.
  - Aceptación: 100% de tests pasando en <5 segundos.

---

## 🛑 REGLAS INVIOLABLES DE OPERACIÓN:
1. No romper los 132 tests existentes (100% verde obligatorio).
2. Toda nueva funcionalidad debe incluir su test unitario en `tests/`.
3. Prohibido eliminar código o datos existentes (Axioma de No Borrado).
4. Abrir PR con título formato: `feat(jules): [TASK-ID] <descripción breve>`.

---
[VINCIT_OMNIA_VERITAS]
Autor: Rafael "Rafa" Pérez & Angelus AGI
