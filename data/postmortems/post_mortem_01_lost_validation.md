# Post-mortem 01: Lost due to validation strategy

> Generic post-mortem illustrating a tabular binary classification competition
> where the wrong validation strategy caused a 0.04 AUC gap between local CV
> and the private leaderboard.

## Competition metadata

- **Modality**: tabular
- **Task**: binary classification
- **Metric**: ROC AUC
- **Class imbalance**: 1:25
- **Submission limit**: 5
- **External data**: not allowed

## Problem DNA snapshot

- has_temporal_component: false (timestamp hidden in numeric features but
  adversary analysis later revealed weak temporal signal)
- has_group_structure: false (assumed; later confirmed low)
- distribution_shift_risk: medium (private LB drift detected via adversarial validation)
- compute_constraint: low

## What we did

1. Built baseline LightGBM with 5-fold StratifiedKFold, 5 seeds.
2. Local CV AUC: 0.942.
3. Tuned hyperparameters on this CV.
4. Submitted top-5 model ensemble.
5. Public LB: 0.939, Private LB: 0.901 (4% gap).

## Why it failed

- We used random KFold. Adversarial validation (which we did not run) showed
  train/test distribution drift.
- A specific feature that leaked the proxy target in train was driving the CV
  signal but was partially absent in the private test set.
- Our tuning was overfit to the proxy CV, not to the true generalization.

## Lessons extracted

1. **Always run adversarial validation early** when distribution_shift_risk is
   unknown.
2. **Never trust random CV when timestamps or row order carry information** —
   use time-based or rolling-origin splits as a sanity check.
3. **Watch the public/private gap**: if it diverges by more than 0.5% with
   small submission limits, down-weight the public signal.

## KB updates proposed

- ADD claim: "Run adversarial validation before tuning on tabular problems
  when distribution_shift_risk is unknown or medium."
- ADD failure: "Random KFold with hidden temporal structure → 4% CV/test gap."
- ADD anti-pattern: "Do not trust public LB when adversarial AUC < 0.55."
