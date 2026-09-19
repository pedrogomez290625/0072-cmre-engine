# Post-mortem 04: Near-miss fixed by postprocessing

> Generic post-mortem illustrating a competition where the difference between
> rank 4 and rank 1 was entirely in postprocessing.

## Competition metadata

- **Modality**: image
- **Task**: classification (10 classes)
- **Metric**: accuracy

## Problem DNA snapshot

- compute_constraint: high
- pretrained_models_allowed: true
- class_imbalance: medium

## What we did

1. Fine-tuned a pretrained ResNet-50 with mixup + cutmix.
2. 5-seed average.
3. Submitted raw argmax predictions.
4. Final rank: 4th, 0.5% accuracy behind the winner.

## What the winner did differently

- They applied test-time augmentation (TTA) with 5 crops + flip.
- They calibrated the logits with temperature scaling before averaging.
- They did a single model selection based on public LB; we did not.

## Lessons extracted

1. **TTA is cheap and almost always helps small-margin image problems.**
2. **Logit calibration before averaging is non-trivial when models come from
   different runs.**
3. **Submission budget: spend 2-3 of 5 attempts on TTA + calibration variants.**

## KB updates proposed

- ADD claim: "TTA (5 crops + flip) typically adds +0.1-0.3% accuracy on
  classification with pretrained backbones."
- ADD claim: "Temperature-scale logits before ensemble averaging to align
  calibrations across independently trained models."
- ADD claim: "For tight competitions, dedicate 40-60% of submission budget to
  postprocessing variants."
