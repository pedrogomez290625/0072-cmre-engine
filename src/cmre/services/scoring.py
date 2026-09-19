"""Deterministic scoring with transparent breakdown.

Design (v0.3.0):
- Pure function: no I/O, no DB. Same input → same output.
- Components weighted explicitly. Easy to test.
- Modality is a soft bonus, NOT a hard filter. Mechanism claims transfer.
- License and provenance multipliers penalize untrusted sources.
- LLM rerank is recorded separately as a bounded delta.

The reasoner uses this as the base ranking. Retrieval then optionally
applies a bounded LLM delta (±0.10).
"""

from __future__ import annotations

from typing import List

import structlog

from ..models import Claim
from ..schemas import ProblemDNA, ScoreBreakdown
from .recency import recency_factor

log = structlog.get_logger("cmre.services.scoring")


# Multipliers applied last. Values are intentional.
PROVENANCE_MULTIPLIER = {
    "internal_experiment": 1.20,
    "paper": 1.10,
    "competition_writeup": 0.95,
    "notebook": 0.90,
    "human_annotation": 1.00,
    "llm_extraction": 0.80,
    "curated_hypothesis": 0.75,
    "unknown": 0.70,
}

LICENSE_MULTIPLIER = {
    "allowed": 1.00,
    "restricted": 0.75,
    "unknown": 0.60,
    "forbidden": 0.0,
}


def _mechanism_fit(claim: Claim, dna: ProblemDNA) -> float:
    """How well does this claim's mechanism address the problem's constraints?

    Mechanism claims: scored by whether their mechanism appears in the DNA's
    risk_flags / validation_recommendations / leak_risks. Strong signal.
    Empirical_trick and platform_specific: scored by tag / condition match.
    """
    mechanism = (claim.mechanism_slug or "").lower()
    if not mechanism:
        return 0.3  # unknown mechanism → weak fit signal

    if claim.claim_type == "mechanism":
        # Direct mechanism match against DNA flags / validation recs / leak_risks.
        signals: list[str] = list(dna.risk_flags) + list(dna.validation_recommendations) + list(dna.leak_risks)
        # Add derived hints from DNA attributes that indicate the mechanism matters.
        derived: list[str] = []
        if dna.has_temporal_component:
            derived.append("temporal_dependency temporal time_series")
        if dna.has_group_structure:
            derived.append("group_dependency")
        if not dna.is_iid:
            derived.append("non_iid distribution_shift")
        joined = " ".join(s.lower() for s in signals + derived)
        # Also look at metric family and modality hints
        joined += f" {dna.modality} {dna.task_type} {dna.metric_family} {dna.compute_constraint}"

        if mechanism in joined:
            return 1.0
        # Partial matches: word-level
        words = [w for w in mechanism.replace("_", " ").split() if w]
        if not words:
            return 0.4
        hits = sum(1 for w in words if w and w in joined)
        if hits:
            return 0.5 + 0.5 * hits / len(words)
        return 0.4  # generic mechanism → modest fit

    # Non-mechanism: tag/condition match
    text_blob = " ".join(
        list(claim.applicable_when or []) + list(claim.tags or [])
    ).lower()
    dna_blob = (
        f"{dna.modality} {dna.task_type} {dna.metric_family} "
        f"imbalance:{dna.class_imbalance} noise:{dna.label_noise_risk} "
        f"shift:{dna.distribution_shift_risk} compute:{dna.compute_constraint}"
    ).lower()
    matches = sum(1 for tok in text_blob.split() if len(tok) > 3 and tok in dna_blob)
    return min(1.0, 0.4 + 0.15 * matches)


def _evidence_quality(claim: Claim) -> float:
    """How strong is the evidence behind this claim?

    evidence_level (0..6) + citations count + reproducibility_score.
    """
    base = min(1.0, claim.evidence_level / 6.0)
    citations = len(claim.citations or []) + len(claim.source_artifact_ids or [])
    base += 0.05 * min(citations, 6)
    base += 0.10 * max(0.0, min(1.0, claim.reproducibility_score))
    # Validation status bumps
    if claim.validation_status == "validated":
        base += 0.15
    elif claim.validation_status == "partially_validated":
        base += 0.07
    elif claim.validation_status == "contradicted":
        base -= 0.40
    return max(0.0, min(1.0, base))


def _constraint_compatibility(claim: Claim, dna: ProblemDNA) -> float:
    """Does this claim conflict with the competition's constraints?

    Checks: not_recommended_when tags against DNA attribute hints. Higher =
    more compatible. A score of 1.0 means no contraindications match.
    """
    if not claim.not_recommended_when:
        return 1.0

    dna_blob = (
        f"{dna.modality} {dna.task_type} {dna.metric_family} "
        f"imbalance:{dna.class_imbalance} noise:{dna.label_noise_risk} "
        f"shift:{dna.distribution_shift_risk} compute:{dna.compute_constraint} "
        f"interpretability_required={dna.interpretability_required} "
        f"iid={dna.is_iid} "
        f"has_temporal_component={dna.has_temporal_component} "
        f"has_group_structure={dna.has_group_structure}"
    ).lower()

    penalty = 0
    for cond in claim.not_recommended_when:
        cond_low = cond.lower()
        for tok in cond_low.replace(",", " ").split():
            if len(tok) > 3 and tok in dna_blob:
                penalty += 1
                break

    return max(0.0, 1.0 - 0.30 * penalty)


def _modality_soft_bonus(claim: Claim, dna: ProblemDNA) -> float:
    """Soft bonus/penalty based on modality fit. NOT a hard filter.

    - DNA modality in compatible_modalities → 1.0
    - DNA modality in transferable_modalities → 0.8 (boosted from 0.6)
    - DNA modality in hard_exclude_modalities → 0.0 (rare, exceptional)
    - Claim has no modality metadata → 0.9 (don't penalize unknown)
    - DNA modality == "any" or claim compatible_modalities == ["any"] → 1.0
    """
    compatible = claim.compatible_modalities or claim.modality_tags or []
    transferable = claim.transferable_modalities or []
    hard_exclude = claim.hard_exclude_modalities or []

    if "any" in compatible or dna.modality == "any":
        return 1.0
    if dna.modality in hard_exclude:
        return 0.0
    if dna.modality in compatible:
        return 1.0
    if dna.modality in transferable:
        return 0.85
    if not compatible:
        return 0.9  # unknown → don't penalize
    return 0.7  # known modality, but neither matches → mild penalty, not exclusion


def compute_deterministic_score(claim: Claim, dna: ProblemDNA) -> ScoreBreakdown:
    """Compute the deterministic base score for a claim against a DNA.

    Pure function. Same input always yields the same output. The full
    breakdown is returned so the report can show "why this rank".
    """
    mech = _mechanism_fit(claim, dna)
    ev = _evidence_quality(claim)
    constraint = _constraint_compatibility(claim, dna)
    rec = recency_factor(claim)

    modality_bonus = _modality_soft_bonus(claim, dna)
    provenance_mult = PROVENANCE_MULTIPLIER.get(claim.provenance_type, 0.70)
    license_mult = LICENSE_MULTIPLIER.get(claim.license_status, 0.60)

    # Weighted sum. Weights sum to 1.0; modality is multiplicative.
    deterministic = (
        0.40 * mech
        + 0.25 * ev
        + 0.20 * constraint
        + 0.10 * rec
        + 0.05  # base relevance (so even unknown claims get a tiny floor)
    ) * modality_bonus * provenance_mult * license_mult

    deterministic = round(max(0.0, min(1.0, deterministic)), 4)

    reasons: list[str] = []
    warnings: list[str] = []

    reasons.append(f"mechanism_fit={mech:.2f} evidence={ev:.2f} constraint={constraint:.2f} recency={rec:.2f}")
    reasons.append(f"modality_bonus={modality_bonus:.2f} provenance×={provenance_mult:.2f} license×={license_mult:.2f}")

    if claim.claim_type == "mechanism" and modality_bonus < 1.0:
        warnings.append(
            f"Mechanism from a different modality (compat={claim.compatible_modalities or claim.modality_tags}, "
            f"transferable={claim.transferable_modalities}, exclude={claim.hard_exclude_modalities}). "
            f"Consider cross-domain evidence."
        )
    if claim.provenance_type == "curated_hypothesis":
        warnings.append("Source: curated hypothesis. Treat as untested until validated.")
    if claim.validation_status == "unvalidated":
        warnings.append("Validation status: unvalidated.")
    if license_mult < 0.8:
        warnings.append(f"License status: {claim.license_status} → score multiplied.")

    return ScoreBreakdown(
        mechanism_fit=round(mech, 4),
        evidence_quality=round(ev, 4),
        constraint_compatibility=round(constraint, 4),
        recency_factor=round(rec, 4),
        modality_bonus=round(modality_bonus, 4),
        provenance_multiplier=round(provenance_mult, 4),
        license_multiplier=round(license_mult, 4),
        deterministic_score=deterministic,
        llm_rerank_delta=0.0,
        final_score=deterministic,
        reasons=reasons,
        warnings=warnings,
    )


def apply_llm_delta(score: ScoreBreakdown, llm_score_0_100: float) -> ScoreBreakdown:
    """Apply a bounded LLM rerank delta on top of the deterministic score.

    The LLM score is in 0..100 (50 = neutral). We map it to ±0.10 delta on
    the 0..1 final score, never more. This keeps the system auditable even
    if the LLM changes tomorrow.
    """
    delta_unscaled = (float(llm_score_0_100) - 50.0) / 100.0  # [-0.5, +0.5]
    bounded = max(-0.10, min(0.10, delta_unscaled))
    final = round(max(0.0, min(1.0, score.deterministic_score + bounded)), 4)
    new = score.model_copy()
    new.llm_rerank_delta = round(bounded, 4)
    new.final_score = final
    new.reasons.append(f"llm_rerank_delta={bounded:+.3f} (bounded ±0.10)")
    return new
