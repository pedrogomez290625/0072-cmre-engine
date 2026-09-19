# CMRE v0.3.0 — Golden evaluation harness

> Without measuring competitive impact, CMRE is just a Markdown generator.

## Run

```bash
# All cases
python scripts/evaluate_golden.py

# Single case
python scripts/evaluate_golden.py --case fraud_temporal_leak_001

# Or via CLI:
cmre evaluate-golden
cmre evaluate-golden --case text_classification_dedup_002
```

## What it does

1. Loads each case in `data/golden_cases/*.json`.
2. Builds the Problem DNA from the embedded `competition_input`.
3. Runs the deterministic scoring against all seeded claims.
4. Compares the resulting DNA + ranked techniques against the case's
   expected assertions.

## Metrics

| Metric | Target | Meaning |
|---|---|---|
| **risk_flag_recall** | ≥ 0.80 | Did we surface the main risks? |
| **validation_recall** | ≥ 0.70 | Did we recommend the right validation? |
| **anti_pattern_recall** | ≥ 0.50 | Did we flag the failure mode? |
| **mechanism_p@10** | ≥ 0.70 | Did the top-10 contain the right mechanisms? |
| **forbidden_hits** | 0 | Did we recommend forbidden techniques? |

These are substring-match metrics, intentionally lenient. They are
starting points, not the final word on quality.

## Sample output

```
---
case: fraud_temporal_leak_001
  risk_flag_recall:      1.00
  validation_recall:     0.50
  anti_pattern_recall:   0.00
  mechanism_p@10:        1.00
  outcome: {'public_score': 0.91, 'private_score': 0.87, 'placement': 'silver',
            'main_failure': 'random_kfold_overfit_public_lb',
            'lesson': 'Winners ran adversarial validation first...'}

=== aggregate ===
  avg risk_flag_recall:    1.0
  avg validation_recall:   0.39
  avg anti_pattern_recall: 0.17
  avg mechanism_p@10:      1.0
  total forbidden hits:    0
```

## Cases shipped in v0.3.0

1. **fraud_temporal_leak_001** — tabular fraud with hidden temporal structure; winners used adversarial + temporal CV.
2. **text_classification_dedup_002** — multilingual text classification with duplicate leak across train/test.
3. **timeseries_forecast_grouped_003** — store-sales forecasting with 1800 series; winners used global models + rolling-origin CV.

Each case is a minimal, generic sketch — no proprietary info. They are
enough to validate that the system detects obvious signals.

## Adding new cases

1. Create `data/golden_cases/<case_id>.json`:
   ```json
   {
     "case_id": "<your_id>",
     "description": "What happened.",
     "competition_input": { ...CompetitionInput... },
     "expected_dna_flags": ["temporal_dependency"],
     "expected_validation_recommendations": ["temporal_validation"],
     "expected_anti_patterns": ["random_kfold_on_temporal"],
     "expected_top_mechanisms": ["temporal_validation", "tree_baseline"],
     "forbidden_recommendations": ["use_random_kfold_as_primary_validation"],
     "known_outcome": { "public_score": 0.91, "private_score": 0.87, "placement": "silver" }
   }
   ```

2. Run `python scripts/evaluate_golden.py` and review the metrics.

3. Iterate on the KB / scoring until the metrics improve.

## Roadmap

- v0.4.0: 10+ cases with private-leaderboard-style hidden outcomes.
- v0.4.0: LLM-reranked evaluation variant for comparison.
- v0.5.0: cross-validation against actual Kaggle public leaderboard
  data (where permitted by ToS).
