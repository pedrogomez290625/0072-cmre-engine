# CMRE — Competitive ML Reasoning Engine

> A competition-agnostic reasoning engine for ML competitions. Today you use it
> on a tabular fraud problem; tomorrow you point it at a text, image,
> time-series or multimodal competition and the same pipeline + architecture
> applies. The skeleton's already wired.

**v0.3.0**: deterministic scoring with transparent breakdown, soft modality
filter (cross-modal transfer preserved), per-claim-type recency decay,
provenance labels, golden-case evaluation harness.

CMRE is not a catalog of winning notebooks. It is a reasoning system that
turns write-ups, papers, repos, models and failures into **Problem DNA** +
**conditional claims** + **ranked technique recommendations** + **experiment
plans**, and learns from each competition you run.

---

## Quickstart

```bash
git clone <your-org>/cmre-engine
cd cmre-engine

# 1. Bring up Postgres + pgvector
make db-up

# 2. Install
make install-dev

# 3. Configure
cp .env.example .env

# 4. Initialize DB + seed multi-modal KB
make init-db
make seed

# 5. Generate your first report (try any modality)
make report-fraud
make report-text
make report-image
make report-ts
make report-multi

# 6. Run tests
make test
```

Outputs land in `reports/*.md`. Each report contains the Problem DNA, ranked
techniques with conditions and risks, a 6-phase experiment plan, and anti-patterns to avoid.

---

## Architecture

CMRE is composed of 9 layers. The same pipeline works for any modality
because modality-specific knowledge is encoded in the DNA + claim tags,
not in code branches.

```
┌──────────────────────────────────────────────────────────────┐
│ 1. Ingestion & Provenance     Connectors (HF, S2, arXiv, GH) │
├──────────────────────────────────────────────────────────────┤
│ 2. Normalization & Extraction Notebook AST, paper parse, LLM │
├──────────────────────────────────────────────────────────────┤
│ 3. Knowledge Base             Claims, Failures, Mechanisms   │
├──────────────────────────────────────────────────────────────┤
│ 4. Problem Profiler           Build Problem DNA              │
├──────────────────────────────────────────────────────────────┤
│ 5. Reasoning Engine           Hybrid retrieval + LLM re-rank │
├──────────────────────────────────────────────────────────────┤
│ 6. Experiment Planner         6-phase plan from DNA          │
├──────────────────────────────────────────────────────────────┤
│ 7. Execution Lab              Local notebooks, MLflow/W&B    │
├──────────────────────────────────────────────────────────────┤
│ 8. Feedback Loop              Experiments + failures         │
├──────────────────────────────────────────────────────────────┤
│ 9. Governance & Evaluation    License, ToS, attribution      │
└──────────────────────────────────────────────────────────────┘
```

See [`docs/architecture.md`](docs/architecture.md) for the full data flow.

---

## Stack

| Layer | Tool | Role |
|---|---|---|
| Reasoning + KB | **Postgres + pgvector** | Persistent KB with embedding search |
| Local LLM | **Antigravity CLI** (default) | Default LLM endpoint at `http://127.0.0.1:4317` |
| Cloud LLM (optional) | **Gemini API** | Used only when explicitly enabled |
| Cloud coding agent | **Google Jules** | Async PR generator (REST `v1alpha`) |
| Planning + Drive | **Gemini Spark** | Drafts specs and exports to Google Drive |
| CI / scheduler | **GitHub Actions** | Cron-driven ingestion, extraction, sync |
| Repo / host | **GitHub** | Source of truth, Codespaces for cloud dev |

### Why this split

- **Antigravity CLI** stays running locally for fast iteration on extraction
  tasks. Free, no API keys.
- **Jules** is reserved for big coding tasks (refactors, multi-file changes,
  tests) that benefit from async review. Free tier: 15 tasks/day, 3 concurrent.
- **Gemini Spark** is *not* used for code edits. It handles: writing project
  specs, drafting research questions, exporting summaries to Drive, and
  planning. The user copies results back into the repo manually or via API.
- **Connectors** never write to the DB directly; the orchestrator handles
  persistence and license guards.

---

## Multi-modal coverage

| Modality | Example input | Notes |
|---|---|---|
| Tabular (binary) | `data/examples/competition_fraud.json` | Strong baselines + class imbalance |
| Text (multiclass) | `data/examples/competition_text_classification.json` | Pretrained transformer + duplicate handling |
| Image (detection) | `data/examples/competition_image_detection.json` | Site-aware splits + domain adaptation |
| Time series | `data/examples/competition_time_series_forecast.json` | Rolling-origin validation + lag features |
| Multimodal | `data/examples/competition_multimodal.json` | Late fusion + missing-modality fallback |
| Ranking | `data/examples/competition_recommendation.json` | Cold-start + temporal leakage |

Generate all reports with:

```bash
make report-all
```

---

## CLI

```bash
cmre init-db                 # create tables in Postgres + pgvector
cmre seed                    # seed multi-modal KB (idempotent)
cmre report -i input.json    # generate a markdown report
cmre ingest --query "..."    # discover public artifacts via connectors
cmre approve-claim <id>      # approve an extracted claim
cmre reject-claim <id> --note "..."
cmre jules-sync              # dispatch tasks from .jules/tasks.yaml
cmre evaluate-golden         # run golden evaluation harness
cmre evaluate-golden --case <id>  # single case
cmre version
```

---

## Connectors

| Connector | Replaces | Status |
|---|---|---|
| HuggingFace Papers | Papers with Code (shut down 2025) | Live |
| Semantic Scholar | Citation + abstract source | Live |
| arXiv | Paper preprint source | Live |
| GitHub | Repo search (clean implementations) | Live |
| Kaggle (planned) | Public notebook source | Disabled by default |

Enable/disable via `CMRE_CONNECTOR_*_ENABLED=true|false`.

---

## Repo layout

```
cmre-engine/
├── src/cmre/                  # the package
│   ├── agents/                # LLM clients (Antigravity, Gemini, Mock) + Jules API
│   ├── connectors/            # data ingestion (HF, S2, arXiv, GitHub)
│   ├── services/              # profiler, retrieval, reasoner, planner, embedder
│   ├── schemas.py             # competition-agnostic Pydantic models
│   ├── models.py              # SQLModel ORM (Postgres + pgvector)
│   ├── db.py                  # engine + init_db
│   ├── config.py              # Settings
│   └── cli.py                 # Typer CLI
├── data/
│   ├── examples/              # 6 CompetitionInput JSONs across modalities
│   └── postmortems/           # 5 retrospective post-mortems
├── prompts/                   # prompt templates for extractors
├── db_migrations/             # raw SQL migrations
├── tests/                     # pytest
├── docker-compose.yml         # Postgres + pgvector
├── Makefile                   # one-liners for every workflow
├── pyproject.toml
├── .env.example
└── README.md
```

---

## Roadmap

- **Native vector columns** (replacing the JSON-embedding storage)
- **MLflow integration** for experiment tracking
- **Contradiction detection** between claims
- **Web review UI** (Streamlit) for approving extracted claims
- **Spark integration** (write specs directly to Drive folder)
- **Multi-user mode** (roles + shared KB)

See [`docs/architecture.md`](docs/architecture.md) and
[`docs/SCORING.md`](docs/SCORING.md) for the full design.

---

## License

MIT. Note that ingested artifacts have their own licenses; the engine never
uses forbidden-licensed artifacts in reports without explicit override.

---

## Changelog

### v0.3.0 (2026-09-19)

- **Soft modality filter**: cross-modal mechanism transfer preserved.
- **Deterministic scoring** with transparent `ScoreBreakdown`.
- **LLM rerank bounded to ±0.10**; deterministic base is the primary ranking.
- **Per-claim-type recency**: mechanism=5y, empirical_trick=1y, platform_specific=6m.
- **Provenance labels**: seeds tagged `curated_hypothesis`, validation labels surfaced in reports.
- **Golden evaluation harness**: `cmre evaluate-golden` runs against 3 shipped cases.
- 28 new tests (68 total, all passing).

### v0.2.0 (2026-09-19)

- Initial skeleton with Postgres + pgvector, multi-modal KB, hybrid retrieval,
  Antigravity + Jules adapters, 6 example competitions, 5 post-mortems.
