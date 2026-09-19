# CMRE Architecture

## 9 layers

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. Ingestion & Provenance                                          │
│    Connectors: HF Papers, Semantic Scholar, arXiv, GitHub          │
│    Output: ArtifactCandidate[] (license_status guaranteed)         │
└─────────────────────────────────────┬────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. Normalization & Extraction                                      │
│    Notebook AST, paper PDF→text, model metadata, write-up→LLM      │
│    Output: ClaimDraft[] + Failure[]                                │
└─────────────────────────────────────┬────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│ 3. Knowledge Base (Postgres + pgvector)                            │
│    Mechanisms, Techniques, Claims, Failures, ProblemProfiles       │
│    Embeddings stored per row; HNSW index planned                   │
└─────────────────────────────────────┬────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│ 4. Problem Profiler                                                │
│    Input: CompetitionInput (any modality)                          │
│    Output: ProblemDNA (modal-agnostic)                              │
└─────────────────────────────────────┬────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│ 5. Reasoning Engine                                                │
│    Hybrid retrieval: cosine + filters + LLM re-rank                 │
│    Recency decay: 0.5 ** (days_old / half_life)                    │
│    Output: RankedClaim[]                                            │
└─────────────────────────────────────┬────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│ 6. Experiment Planner                                              │
│    6 phases: Validation → Baseline → Diagnose → Improve → Robust → Submit │
│    Output: ExperimentPlan                                           │
└─────────────────────────────────────┬────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│ 7. Execution Lab (user-side)                                        │
│    Local notebooks + MLflow / W&B (when integrated)                 │
│    Track every Experiment → register_outcome                       │
└─────────────────────────────────────┬────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│ 8. Feedback Loop                                                   │
│    Outcomes → Claims (boost/demote evidence level)                  │
│    Negative outcomes → Failure records                              │
│    Periodic: contradiction detection + decay recalibration           │
└─────────────────────────────────────┬────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│ 9. Governance & Evaluation                                         │
│    License guards, ToS, attribution, KB quality metrics              │
└──────────────────────────────────────────────────────────────────┘
```

## Data flow

```
CompetitionInput JSON
        │
        ▼
   Problem Profiler  ─────────┐
        │                    │
        ▼                    │
   ProblemDNA                 │
        │                    │
        ▼                    │
   Hybrid Retriever ◀────────┘  (uses KB embeddings)
        │
        ▼
   LLM Re-ranker
        │
        ▼
   Recency decay
        │
        ▼
   RankedClaim[]
        │
        ▼
   Planner ── ExperimentPlan (6 phases)
        │
        ▼
   Reporter ── Markdown report
```

## Storage layout

```
Postgres (pgvector)
├── mechanisms                 (8 baseline mechanisms)
├── techniques                 (per-claim technique refs)
├── claims                     (30+ baseline claims, multi-modal)
│   └── embedding JSON         (cosine similarity)
├── failures                   (negative-outcome records)
├── problem_profiles           (DNA + embedding)
├── artifacts                  (ingestion cache)
├── competitions               (raw competition metadata)
├── experiments                (hypothesis + result + decision)
└── review_tasks               (pending human reviews)
```

## Recency decay

```
weight = 0.5 ** (days_since_published / CMRE_EVIDENCE_HALF_LIFE_DAYS)
```

Default half-life is 365 days. Override per-environment.

## Embedding strategy

- Default model: `sentence-transformers/all-MiniLM-L6-v2` (384 dims).
- Embeddings are produced via the configured LLM client (Antigravity by default).
- On API failure, a deterministic hash-based pseudo-embedding is used so
  pipelines keep working offline.
- Migration 0001 plans the move to native `vector(384)` columns with HNSW
  indexes.

## Contradiction detection (placeholder)

Two claims are considered candidates for contradiction if:
- They share at least one `applicable_when` tag.
- They have opposite `expected_effect.direction`.
- They were both ingested in the last 30 days.

Future work: graph-based reasoning to surface these in a review queue.

## Roadmap

| Quarter | Milestone |
|---|---|
| Now | MVP with 30+ multi-modal claims, hybrid retrieval, 6 example competitions |
| Q1 | Native pgvector columns + HNSW indexes |
| Q1 | MLflow experiment tracking integration |
| Q2 | Contradiction detector + auto-decay job |
| Q2 | Streamlit review UI |
| Q3 | Spark Drive integration (export reports to Drive folder) |
| Q4 | Multi-user + roles |
