"""Experiment planner.

Translates a ranked list of claims + the Problem DNA into an actionable
6-phase experiment plan. Phases are modality-aware but the structure
(validation → baseline → diagnose → high-ROI → robustness → submission) is
generic across modalities.
"""

from __future__ import annotations

from typing import List

from ..schemas import ExperimentPhase, ExperimentPlan, ProblemDNA, RankedClaim
from .problem_profiler import modality_baselines, modality_validation


def generate_plan(
    dna: ProblemDNA,
    ranked_claims: List[RankedClaim],
    max_techniques: int = 10,
) -> ExperimentPlan:
    top = ranked_claims[:max_techniques]

    validation_actions = list(dna.validation_recommendations) or modality_validation(dna.modality)
    anti_patterns = list(dna.anti_patterns)
    baseline_actions = modality_baselines(dna.modality)

    phase_1 = ExperimentPhase(
        name="Phase 1: Credible validation",
        objective="Construct a CV that exposes the dominant constraint (drift, leak, label noise).",
        actions=validation_actions
        + [
            "Fix seeds",
            "Record CV score per fold / segment",
            "Compare train vs test feature distributions if adversarial AUC is feasible",
        ],
        success_criteria=[
            "Validation explains public LB within 0.5% (or explained gap is documented)",
            "No obvious leakage (adversarial AUC < 0.55 for IID, < 0.65 with caveats)",
            "Baseline is reproducible across seeds",
        ],
        risks=[
            "Using KFold on temporal / grouped data",
            "Trusting public LB on small test sets",
            "Ignoring class imbalance in split (no stratification)",
        ],
    )

    phase_2 = ExperimentPhase(
        name="Phase 2: Strong baseline",
        objective="Capture the dominant signal with minimal cost.",
        actions=baseline_actions,
        success_criteria=[
            "Improvement over dummy / random baseline",
            "Reproducible across seeds",
            "Single-digit-hour training time",
        ],
        risks=[
            "Overfitting via excessive early tuning",
            "Skipping sanity-check baselines",
        ],
    )

    phase_3 = ExperimentPhase(
        name="Phase 3: Diagnostic",
        objective="Identify the dominant constraint (validation, data, metric, model).",
        actions=[
            "Error analysis per segment / class / time bucket",
            "Feature importance (permutation or attribution)",
            "Leak detection (duplicate IDs, future features, target encoding)",
            "Train/test drift (adversarial validation, KS test, PSI)",
            "Tail of metric (where does the model lose points?)",
        ],
        success_criteria=[
            "Know which kind of errors dominate",
            "Detect whether problem is validation, data, metric, or model",
        ],
        risks=[
            "Looking only at global average metrics",
            "Confusing correlation with causation",
        ],
    )

    phase_4 = ExperimentPhase(
        name="Phase 4: High-ROI improvements",
        objective="Try conditional techniques ranked by expected lift.",
        actions=[c.statement for c in top],
        success_criteria=[
            "Each experiment has explicit hypothesis",
            "Lift measured against the credible validation",
            "Discarded quickly if no signal",
        ],
        risks=[
            "Adopting write-up tricks without reproducing conditions",
            "Adding complexity without measurable gain",
        ],
    )

    phase_5 = ExperimentPhase(
        name="Phase 5: Robustness",
        objective="Reduce variance and submission risk.",
        actions=[
            "Multi-seed evaluation",
            "Stress test on sub-periods / segments",
            "Consistency between public and private signals",
            "License / rules review before using external artifacts",
        ],
        success_criteria=[
            "Model does not depend on a lucky seed",
            "No legal / regulatory risk",
        ],
        risks=[
            "Blind ensembling without diversity measurement",
            "Overfitting to public LB",
        ],
    )

    phase_6 = ExperimentPhase(
        name="Phase 6: Final submission",
        objective="Send lowest-expected-risk submission.",
        actions=[
            "Conservative ensemble (only if measured diversity)",
            "Postprocessing aligned to metric",
            "Document assumptions and risks",
            "Plan B in case private LB behaves differently",
        ],
        success_criteria=[
            "Reproducible submission script",
            "Documented risks",
        ],
        risks=anti_patterns,
    )

    dna_summary = (
        f"Task: {dna.task_type}; modality: {dna.modality}; metric: {dna.metric} ({dna.metric_family}); "
        f"risks: {', '.join(dna.risk_flags) or 'none detected'}"
    )

    return ExperimentPlan(
        competition_title=dna.title,
        dna_summary=dna_summary,
        phases=[phase_1, phase_2, phase_3, phase_4, phase_5, phase_6],
        top_techniques=top,
        avoid=anti_patterns,
        next_steps=[
            "Review claims with low evidence before running experiments",
            "Record each experiment with hypothesis + result",
            "After competition: post-mortem and update KB",
        ],
    )
