# CMRE v0.3.0 — Scoring system

> How a claim ends up at position N in the report.

## Pipeline

```
CompetitionInput JSON
        │
        ▼
Problem Profiler            → Problem DNA (multi-modal aware)
        │
        ▼
Hard Filters                → license / approval / hard_exclude_modalities
        │
        ▼
Hybrid Retrieval            → top-50 candidates by embedding cosine
        │
        ▼
Deterministic Scoring       → primary ranking (PURE FUNCTION, deterministic)
        │
        ▼
Optional LLM Rerank         → ±0.10 BOUNDED delta + explanation
        │
        ▼
Final Ranked Claim
```

## Deterministic score (the primary ranking)

For each candidate claim, `compute_deterministic_score(claim, dna)` returns
a `ScoreBreakdown`:

```
deterministic =
    ( 0.40 * mechanism_fit
    + 0.25 * evidence_quality
    + 0.20 * constraint_compatibility
    + 0.10 * recency_factor
    + 0.05 )
    × modality_bonus
    × provenance_multiplier
    × license_multiplier
```

### Components

| Component | What it measures | Source |
|---|---|---|
| **mechanism_fit** (0..1) | Does the claim's mechanism match the DNA's risk flags / validation recs / leak signals? | Mechanism slug vs DNA keywords |
| **evidence_quality** (0..1) | How strong is the evidence? | evidence_level, citations, reproducibility, validation_status |
| **constraint_compatibility** (0..1) | Are there contraindications matching the DNA? | not_recommended_when tags vs DNA attributes |
| **recency_factor** (0.2..1) | How old is the claim, adjusted for its type? | per-claim-type half-life + validation boost |
| **modality_bonus** (0..1.0) | Soft penalty/bonus for cross-modal claims | compatible_modalities / transferable_modalities |
| **provenance_multiplier** | Trust multiplier based on source type | `curated_hypothesis=0.75`, `internal_experiment=1.20` |
| **license_multiplier** | Legal/ToS multiplier | `allowed=1.0`, `forbidden=0.0` |

### Per-claim-type recency (v0.3.0)

| claim_type | half-life | meaning |
|---|---|---|
| `mechanism` | 5 years | Focal loss, calibration, temporal validation → decay slowly |
| `empirical_trick` | 1 year | Specific tuning, platform workarounds → decay medium |
| `platform_specific` | 6 months | Kaggle forum tricks → decay fast |

Plus boosts:
- `validation_count` (max 5) → +0.02 each
- `reproducibility_score` (0..1) → +0.05 max

Clamped to [0.2, 1.0] so ancient validated claims keep some weight.

### Modality is soft (v0.3.0)

- DNA modality in `compatible_modalities` → bonus = 1.0
- DNA modality in `transferable_modalities` → bonus = 0.85
- DNA modality in `hard_exclude_modalities` → bonus = 0.0 (rare)
- Unknown compatible list → bonus = 0.9 (don't penalize unknown)
- Else → 0.7 (mild penalty, NOT exclusion)

This preserves cross-domain transfer (e.g., calibration from CV → tabular).

### Provenance multipliers

| provenance_type | multiplier |
|---|---|
| `internal_experiment` | 1.20 |
| `paper` | 1.10 |
| `competition_writeup` | 0.95 |
| `notebook` | 0.90 |
| `human_annotation` | 1.00 |
| `llm_extraction` | 0.80 |
| `curated_hypothesis` | 0.75 |
| `unknown` | 0.70 |

## LLM rerank (bounded)

The LLM can move a claim's final score by **at most ±0.10**:

```
llm_delta = max(-0.10, min(0.10, (llm_score - 50) / 100))
final_score = deterministic_score + llm_delta
```

LLM contributions:
- Rationale text (`"reason"`)
- Contraindication warning (`"contraindication"`)
- Confidence (recorded in breakdown)

LLM responses are **cached** by hash of (DNA + claim set + prompt version).

## Example breakdown (v0.3.0)

For a tabular fraud competition with hidden temporal structure:

```
Rank 1 (score=0.65)
  Statement: "Adversarial validation exposes train/test distribution shift..."
  Mechanism:  adversarial_validation
  Type:       mechanism          ← slow decay
  Provenance: curated_hypothesis  ← multiplier 0.75
  Validation: unvalidated         ← visible warning

  Breakdown:
    mechanism_fit:           1.00  ← perfect: DNA has temporal_dependency + distribution_shift risk
    evidence_quality:        0.67
    constraint_compatibility: 1.00
    recency_factor:          0.50  ← no published_at, neutral
    modality_bonus:          1.00  ← DNA=tabular, compatible_modalities includes tabular
    provenance_multiplier:   0.75
    license_multiplier:      1.00
    deterministic_score:     0.65
    llm_rerank_delta:        0.00  ← LLM neutral
    final_score:             0.65

  Warnings:
    - Source: curated hypothesis. Treat as untested until validated.
    - Validation status: unvalidated.
```

## Why this design

1. **Deterministic base** → reproducible, testable, no flaky CI.
2. **Modality is soft** → cross-domain mechanism transfer preserved.
3. **Per-type recency** → mechanism papers don't die, tricks do.
4. **Provenance labels** → seeds ≠ validated evidence.
5. **Bounded LLM** → LLM helps, never dominates.
6. **Full breakdown in report** → every score is auditable.

See `services/scoring.py` and `services/recency.py` for the implementation.
