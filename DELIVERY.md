# CMRE Engine v0.3.0 — Delivery summary

> Built and tested on 2026-09-19. Adds deterministic scoring, soft modality
> filter, per-type recency decay, provenance labels, and a golden-case
> evaluation harness on top of the v0.2.0 skeleton.

## What changed from v0.2.0 → v0.3.0

### Code changes (the 4 P0 fixes)

| # | Problem | Fix | Files |
|---|---|---|---|
| 1 | Hard modality filter contradicted transfer thesis | Soft bonus; modality is multiplicative, not a filter | `services/scoring.py`, `services/reasoner.py` |
| 2 | LLM at 60% of score was a black box | Deterministic base + bounded ±0.10 LLM delta | `services/scoring.py`, `services/retrieval.py` |
| 3 | 365-day recency killed foundational methods | Per-claim-type half-life: mechanism=5y, trick=1y, platform=6m | `services/recency.py` |
| 4 | Seeds were indistinguishable from validated evidence | `provenance_type`, `validation_status` fields; multiplier table | `models.py`, `schemas.py`, `services/scoring.py`, `seeder_multimodal.py` |

### New modules

- `src/cmre/services/scoring.py` — pure deterministic scoring with breakdown.
- `src/cmre/services/recency.py` — per-type decay.
- `scripts/evaluate_golden.py` — runs the golden-case harness.
- `data/golden_cases/` — 3 generic competitions with known outcomes.
- `tests/test_scoring.py`, `tests/test_recency.py`, `tests/test_soft_modality.py`, `tests/test_golden_cases.py`.

### Schema additions

`Claim` gained:
- `claim_type` (mechanism / empirical_trick / platform_specific)
- `compatible_modalities`, `transferable_modalities`, `hard_exclude_modalities`
- `provenance_type`, `validation_status`, `last_validated_at`, `validation_count`, `reproducibility_score`
- `supports_claim_ids`, `contradicts_claim_ids`

`RankedClaim` gained:
- `claim_type`, `provenance_type`, `validation_status`
- `score_breakdown` (ScoreBreakdown with 7 components + bounded LLM delta)
- `sources` (list of SourceRef)
- `review_status`

## Verified

- **68/68 tests passing** (up from 40 in v0.2.0).
- **Smoke test runs end-to-end**: 35 claims seeded, 6 example competitions
  parsed, 8 ranked claims each, full markdown reports generated.
- **Golden evaluation runs**: detects all 4 expected DNA flags in fraud
  case, all 3 expected mechanisms in top-10, zero forbidden hits.

## Golden-case baseline metrics

```
case: fraud_temporal_leak_001
  risk_flag_recall:      1.00   ✓
  validation_recall:     0.50
  anti_pattern_recall:   0.00
  mechanism_p@10:        1.00   ✓
  forbidden_hits:        0      ✓

case: text_classification_dedup_002
  risk_flag_recall:      1.00   ✓
  validation_recall:     0.00
  anti_pattern_recall:   0.00
  mechanism_p@10:        1.00   ✓
  forbidden_hits:        0      ✓

case: timeseries_forecast_grouped_003
  risk_flag_recall:      1.00   ✓
  validation_recall:     0.67
  anti_pattern_recall:   0.50
  mechanism_p@10:        1.00   ✓
  forbidden_hits:        0      ✓
```

Areas to improve next: validation_recall and anti_pattern_recall are
still partial. The profiler's modality-specific anti-pattern dictionaries
need expansion to match the test cases more precisely.

## File layout (v0.3.0)

```
cmre-engine/
├── README.md, DELIVERY.md
├── docs/
│   ├── architecture.md
│   ├── SCORING.md        ← new
│   └── EVALUATION.md     ← new
├── Makefile, docker-compose.yml, pyproject.toml, .env.example, .gitignore
├── smoke_test.py
├── scripts/
│   └── evaluate_golden.py   ← new
├── src/cmre/
│   ├── agents/             (AntigravityClient, JulesAPIAdapter, Mock)
│   ├── connectors/         (HF Papers + SS + arXiv + GitHub)
│   ├── services/
│   │   ├── scoring.py      ← new (deterministic breakdown)
│   │   ├── recency.py      ← new (per-type decay)
│   │   ├── reasoner.py     ← updated (soft modality, deterministic)
│   │   ├── retrieval.py    ← updated (bounded LLM delta)
│   │   ├── profiler, planner, embedder, KB, seeder, reporter
│   ├── schemas.py          (added ScoreBreakdown, SourceRef, ClaimType, etc.)
│   ├── models.py           (added claim_type, provenance, validation fields)
│   └── cli.py              (added evaluate-golden command)
├── data/
│   ├── examples/           (6 competitions)
│   ├── postmortems/        (5 retrospective post-mortems)
│   └── golden_cases/       ← new (3 cases with known outcomes)
├── db_migrations/0001_pgvector.sql
├── prompts/competition_generic.md
└── tests/                  (68 tests, all passing)
```

## How to run it

```bash
# 1. Quick demo (no Postgres)
PYTHONPATH=src python smoke_test.py
# Generates 6 reports in reports/*.md

# 2. Golden evaluation
python scripts/evaluate_golden.py

# 3. Full stack (Postgres + pgvector)
make db-up && make install-dev
cp .env.example .env
make init-db && make seed
make report-all
make test
```

## Tests output (v0.3.0)

```
68 passed in 4.11s
```

## What is NOT in v0.3.0 (deferred to v0.4.0+)

- 10+ golden cases (only 3 shipped)
- MLflow integration for experiment tracking
- Native pgvector columns (migration path documented)
- Contradiction detector between claims
- Streamlit review UI
- Auto Problem Profiler from raw data
- Spark Drive export integration

These are tracked in `docs/architecture.md` roadmap section.
