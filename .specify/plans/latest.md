# 📐 PLAN TÉCNICO DE ARQUITECTURA (PLAN LATEST)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Objetivo:** Guía de implementación técnica para agentes (Jules, Nova, Kimi, Angelus).

---

## 🏗️ 1. MAPA DE COMPONENTES DEL SISTEMA (`src/cmre/`)

```
src/cmre/
├── models.py              # Esquemas relacionales SQLModel (Claim, Mechanism, Failure, ProblemProfile, Experiment)
├── schemas.py             # Modelos de validación Pydantic v2 (CompetitionInput, ProblemDNA, RankedClaim, ExperimentPlan)
├── config.py              # Configuración Pydantic Settings (.env, paths de Drive, APIs)
├── db.py                  # Conexión DB (Postgres/pgvector o SQLite local para tests)
├── cli.py                 # Interfaz de línea de comandos Typer + Rich
├── connectors/
│   ├── base.py            # Protocolo abstracto BaseConnector
│   ├── arxiv.py           # Conector arXiv API
│   ├── github.py          # Conector GitHub API
│   ├── huggingface.py     # Conector HF Hub API
│   └── semantic_scholar.py# Conector Semantic Scholar
├── services/
│   ├── problem_profiler.py# Extractor de ProblemDNA
│   ├── retrieval.py       # Motor de búsqueda híbrida vectorial + filtros
│   ├── scoring.py         # Algoritmos de scoring, penalización y afinidad
│   ├── recency.py         # Función de decaimiento temporal
│   ├── reasoner.py        # Orquestador del razonamiento condicional
│   ├── planner.py         # Generador de ExperimentPlan en 6 fases
│   ├── reporter.py        # Renderizador de reportes en Markdown profesional
│   ├── embedder.py        # Generador de embeddings (MiniLM o mock determinista)
│   └── knowledge_base.py  # Operaciones CRUD sobre la base de conocimiento
└── agents/
    ├── base.py            # Interfaces para agentes
    ├── jules_api.py       # Cliente para API de Jules Cloud
    ├── jules_outbox.py    # Cola de tareas exportables para Jules
    └── antigravity_client.py # Cliente para Antigravity IDE
```

---

## 🧪 2. ESTRATEGIA DE VERIFICACIÓN DETERMINISTA
- Suite completa en `tests/`:
  - `test_profiler.py`: Verifica que cada modalidad y métrica produzca el ADN esperado.
  - `test_scoring.py`: Verifica penalizaciones por desbalance, costo computacional y recencia.
  - `test_recency.py`: Valida el decaimiento exponencial a 30, 90, 365 días.
  - `test_reasoner.py`: Valida ranqueo y generación de explicaciones condicionales.
  - `test_connectors.py`: Valida llamadas seguras con fallbacks.
  - `test_golden_cases.py`: Casos de prueba canónicos (fraude, NLP, series de tiempo).

---

## 🚀 3. HOJA DE RUTA DE EVOLUCIÓN
1. Conector especializado de Kaggle Write-ups (`kaggle_discussions.py`).
2. Módulo de perfilado para química / espectrometría de masas (`Enveda CASMI 2026`).
3. Sincronizador de base de conocimiento hacia Google Drive (`0072-cmre-engine/knowledge_db/`).
