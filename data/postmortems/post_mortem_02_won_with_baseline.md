# Post-mortem 02: Won with strong baseline + postprocessing

> Generic post-mortem illustrating a competition won without fancy models,
> only solid baselines, careful CV, and postprocessing aligned to the metric.

## Competition metadata

- **Modality**: tabular
- **Task**: binary classification
- **Metric**: Average Precision (PR-AUC)
- **Class imbalance**: 1:200 (extreme)
- **Submission limit**: 5

## Problem DNA snapshot

- distribution_shift_risk: low
- leak_risk: low
- compute_constraint: low
- class_imbalance: extreme

## What we did

1. LightGBM with class weights, 5-fold StratifiedKFold, 10 seeds.
2. CatBoost on raw categoricals, same CV.
3. Logistic regression on standardized + one-hot features (sanity check).
4. Rank-blend ensemble (uniform weights, rank-mean).
5. Threshold-tuned output to optimize AP, not raw probability.
6. Final submission: simple rank ensemble + threshold tuning.

## Why it worked

- Baseline was already strong (LGBM CV AP = 0.42).
- Threshold tuning against the actual metric (AP) gave +0.015 AP.
- We avoided ensembling models that didn't add diversity (we measured
  pairwise correlation first).

## Lessons extracted

1. **Diversity matters more than ensemble size** in low-data tabular problems.
2. **Threshold tuning on the actual metric often beats architecture changes.**
3. **Sanity-check baseline first**: a logistic regression at AP=0.35 tells you
   the signal is mostly linear.

## KB updates proposed

- ADD claim: "Rank-blend ensembles work well for AP/AUC metrics when models
  have low pairwise correlation (<0.95)."
- ADD claim: "Threshold tuning on PR-AUC can give +0.01 to +0.03 over raw
  probabilities."
- ADD claim: "For extreme class imbalance, logistic regression is a useful
  sanity-check baseline (not just a placeholder)."
