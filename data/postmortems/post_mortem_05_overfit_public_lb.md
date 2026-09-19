# Post-mortem 05: Overfit to public leaderboard

> Generic post-mortem illustrating a competition where repeated public-LB
> chasing destroyed private-LB performance.

## Competition metadata

- **Modality**: tabular
- **Task**: ranking
- **Metric**: NDCG@10
- **Submission limit**: 3

## Problem DNA snapshot

- compute_constraint: medium
- distribution_shift_risk: medium
- class_imbalance: high

## What we did

1. Submitted baseline LightGBM. Public LB NDCG: 0.78.
2. Tweaked features and re-submitted (using all 3 attempts quickly).
3. Got to 0.81 on public.
4. Final rank: 0.71 on private (collapsed).

## Why it failed

- Public LB was 1,000 rows; private was 50,000. The signal-to-noise on
  public was too low to optimize against.
- We treated public as ground truth.
- We had no internal CV discipline.

## Lessons extracted

1. **When public LB is small, treat it as a sanity check, not a target.**
2. **Reserve submissions for genuinely new approaches, not small tweaks.**
3. **Maintain an honest CV; let it be the optimization target.**

## KB updates proposed

- ADD claim: "If public test set has <5% of total samples, down-weight public
  LB signal in favor of internal CV."
- ADD claim: "Spend at most 1 of 5 submissions per approach; reserve the rest
  for qualitatively different methods."
- ADD anti-pattern: "Submitting multiple near-identical variants of the same
  model to chase a noisy public LB."
