# Post-mortem 03: Lost due to undetected leakage

> Generic post-mortem illustrating a competition where a leak in the data went
> undetected, inflated CV, and silently broke private LB.

## Competition metadata

- **Modality**: tabular
- **Task**: binary classification
- **Metric**: Log Loss
- **Class imbalance**: 1:5

## Problem DNA snapshot

- leak_risk: medium
- leak_signals: ["near_duplicate_rows_suspected"]
- distribution_shift_risk: medium

## What we did

1. Quick LightGBM baseline: CV log loss = 0.12 (very strong).
2. Tuned for two weeks; CV log loss reached 0.07.
3. Submitted ensemble. Public LB: 0.09 (great). Private LB: 0.32 (catastrophic).

## Why it failed

- A near-duplicate of the target column existed in the test metadata (an ID
  hash that correlated 0.99 with the target in train).
- Our CV splits put duplicates across folds, inflating CV.
- Private LB held-out the duplicates, so the signal evaporated.

## Lessons extracted

1. **Always inspect duplicate rows and near-duplicate IDs** before tuning.
2. **If CV looks too good (>30% better than sanity baseline), suspect leakage.**
3. **Sanity-check feature importances against expected domain knowledge.**

## KB updates proposed

- ADD claim: "If CV metric is dramatically better than a domain-informed
  baseline, suspect leakage before celebrating."
- ADD claim: "Near-duplicate row detection across train/test should be a
  pre-flight check in any tabular competition."
- ADD failure: "Undetected near-duplicate ID leakage → 4× CV-to-private gap."
