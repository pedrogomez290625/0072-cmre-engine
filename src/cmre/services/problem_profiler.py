"""Competition-agnostic problem profiler.

Builds a ProblemDNA from a CompetitionInput. Works for tabular, text, image,
time-series and multimodal without code branches — modality-specific behavior
is encoded in the risk_flags / validation_recommendations / anti_patterns
lists, which downstream services consume generically.
"""

from __future__ import annotations

from typing import Optional

import structlog

from ..agents.base import LLMClient
from ..schemas import (
    CompetitionInput,
    ProblemDNA,
    TASK_TYPES,
)

log = structlog.get_logger("cmre.services.profiler")


# ---------------------------------------------------------------------------
# Modality-specific knowledge tables (pure data, not code branches)
# ---------------------------------------------------------------------------

_VALIDATION_BY_MODALITY = {
    "tabular": [
        "Stratified KFold if classification with class imbalance",
        "Group KFold if multiple rows per entity (user, patient, session)",
        "Adversarial validation to detect train/test distribution shift",
        "Time-based split if timestamp exists and test is future",
        "Repeated KFold (3 seeds × 5 folds) for variance estimation",
    ],
    "text": [
        "Hold-out by source/author to detect domain shift",
        "Stratified KFold on labels (most text tasks)",
        "Nested KFold if doing hyperparameter search",
        "Watch for duplicate texts across train/val",
    ],
    "image": [
        "Patient/identity-level split if medical imaging",
        "Domain-based split if multiple devices/sites",
        "Stratified KFold otherwise",
        "Adversarial validation if test distribution is unclear",
    ],
    "video": [
        "Scene/video-level split (avoid leaking frames)",
        "Group KFold if videos come from same channel",
        "Time-based split if chronological",
    ],
    "audio": [
        "Speaker-level split (not utterance-level)",
        "Stratified KFold otherwise",
        "Check recording device metadata for domain shift",
    ],
    "time_series": [
        "Rolling-origin / walk-forward validation",
        "Never use random KFold on temporal data",
        "Use multiple forecast horizons",
        "Include regime-change scenarios",
    ],
    "graph": [
        "Subgraph split (not random node split)",
        "Bipartite-aware split if heterogeneous",
        "Time-aware split if temporal edges",
    ],
    "multimodal": [
        "Modality-aligned split (keep pairs together)",
        "Adversarial validation to detect modality drift",
        "Per-modality fallback if one modality is missing in test",
    ],
}


_ANTI_PATTERNS_BY_MODALITY = {
    "tabular": [
        "Don't trust public leaderboard without sanity check vs CV",
        "Don't tune hyperparameters on test set",
        "Don't ignore class imbalance in split (stratify)",
        "Don't use random KFold when IDs/timestamps exist",
    ],
    "text": [
        "Don't do random splits if duplicate paraphrases exist",
        "Don't use accuracy on highly imbalanced classes",
        "Don't fine-tune on full corpus without val split",
    ],
    "image": [
        "Don't split by image when images come in groups (patient, video)",
        "Don't trust leaderboard on small test sets",
        "Don't skip empty/corrupt image checks",
    ],
    "time_series": [
        "Don't use random KFold on temporal data",
        "Don't evaluate only on a single window",
        "Don't include future-lagged features",
    ],
    "audio": [
        "Don't split by utterance when speakers overlap train/test",
    ],
    "graph": [
        "Don't random-split nodes from the same subgraph",
    ],
    "multimodal": [
        "Don't mix-modality pairs across folds",
        "Don't trust single-modality accuracy on missing-modality test",
    ],
}


_BASELINE_BY_MODALITY = {
    "tabular": [
        "LightGBM with default hyperparameters",
        "CatBoost if many high-cardinality categoricals",
        "Logistic regression / Ridge as sanity check",
    ],
    "text": [
        "TF-IDF + linear model (often strong on small data)",
        "Pretrained transformer (DistilBERT / RoBERTa) with linear head",
    ],
    "image": [
        "Pretrained ResNet/EfficientNet with augmentation",
        "Self-supervised pretraining if labels scarce",
    ],
    "time_series": [
        "Seasonal naive baseline",
        "LightGBM with lag features",
        "Global forecasting model (TFT, N-BEATS) if many series",
    ],
    "audio": [
        "Pretrained audio encoder (Whisper / wav2vec)",
    ],
    "graph": [
        "GraphSAGE or simple GCN baseline",
    ],
    "multimodal": [
        "Each modality independently first",
        "Late fusion vs early fusion ablation",
        "Cross-modal contrastive if data scale allows",
    ],
}


def _metric_family(task_type: str, metric: str) -> str:
    metric_lower = (metric or "").lower()
    for family in (
        "auc",
        "average_precision",
        "log_loss",
        "rmse",
        "mae",
        "ndcg",
        "map",
        "f1",
        "f_beta",
        "accuracy",
        "bleu",
        "rouge",
        "wer",
    ):
        if family in metric_lower:
            return family
    if "logloss" in metric_lower:
        return "log_loss"
    if "mse" in metric_lower or "rmse" in metric_lower:
        return "rmse"
    if task_type in {"ranking"}:
        return "ndcg"
    if task_type in {"regression"}:
        return "rmse"
    if task_type in {"binary_classification", "multiclass_classification"}:
        return "auc"
    return "custom"


def _risk_flags(inp: CompetitionInput) -> list[str]:
    flags: list[str] = []
    if inp.has_temporal_component:
        flags.append("temporal_dependency")
    if inp.has_group_structure:
        flags.append("group_dependency")
    if inp.distribution_shift_risk in {"medium", "high"}:
        flags.append("distribution_shift")
    if inp.label_noise_risk in {"medium", "high"}:
        flags.append("label_noise")
    if inp.class_imbalance in {"high", "extreme"}:
        flags.append("class_imbalance")
    if inp.leak_risk in {"medium", "high"}:
        flags.append("leak_risk")
    if inp.leak_signals:
        for sig in inp.leak_signals:
            flags.append(f"leak_signal:{sig}")
    if inp.compute_constraint == "gpu_only":
        flags.append("compute_constrained_gpu")
    if inp.is_iid is False:
        flags.append("non_iid")
    if inp.interpretability_required:
        flags.append("interpretability_required")
    return flags


def _maybe_enrich_with_llm(inp: CompetitionInput, dna: ProblemDNA, llm: Optional[LLMClient]) -> ProblemDNA:
    """If an LLM is available and the description is rich, enrich DNA fields.

    Gracefully degrades when the LLM returns invalid JSON or is unavailable.
    """
    if not llm or not inp.description:
        return dna

    system_prompt = (
        "You are an ML competition profiler. Given a competition description, "
        "return ONLY valid JSON with these fields: class_imbalance, label_noise_risk, "
        "distribution_shift_risk, leak_risk, additional_risk_flags (list), "
        "additional_validation_recommendations (list). Use values: "
        "low|medium|high|extreme|unknown|none. Be conservative."
    )
    user_prompt = (
        f"Title: {inp.title}\n"
        f"Modality: {inp.modality}\n"
        f"Task: {inp.task_type}\n"
        f"Metric: {inp.metric}\n"
        f"Description:\n{inp.description}\n"
    )
    try:
        payload = llm.complete_json(system_prompt, user_prompt, schema_name="DNAEnrichment")
    except Exception as exc:
        log.warning("dna_enrich_failed", error=str(exc))
        return dna

    if not isinstance(payload, dict):
        return dna

    for field in ("class_imbalance", "label_noise_risk", "distribution_shift_risk", "leak_risk"):
        val = payload.get(field)
        if isinstance(val, str) and val in {"unknown", "none", "low", "medium", "high", "extreme"}:
            setattr(dna, field, val)
    extras = payload.get("additional_risk_flags") or []
    if isinstance(extras, list):
        dna.risk_flags = list(dict.fromkeys(dna.risk_flags + [str(x) for x in extras]))
    extra_val = payload.get("additional_validation_recommendations") or []
    if isinstance(extra_val, list):
        dna.validation_recommendations = list(
            dict.fromkeys(dna.validation_recommendations + [str(x) for x in extra_val])
        )
    dna.risk_flags = _risk_flags(inp)  # recompute from enriched fields
    return dna


def build_dna(inp: CompetitionInput, llm: Optional[LLMClient] = None) -> ProblemDNA:
    modality = inp.modality if inp.modality in {"tabular", "text", "image", "video", "audio", "time_series", "graph", "multimodal"} else "tabular"

    task = inp.task_type if inp.task_type in TASK_TYPES else "other"
    metric_family = _metric_family(task, inp.metric)

    dna = ProblemDNA(
        title=inp.title,
        platform=inp.platform,
        task_type=task,
        modality=modality,
        metric=inp.metric,
        metric_family=metric_family,
        has_temporal_component=inp.has_temporal_component,
        has_group_structure=inp.has_group_structure,
        is_iid=inp.is_iid,
        external_data_allowed=inp.has_external_data_allowed,
        pretrained_models_allowed=inp.has_pretrained_models_allowed,
        class_imbalance=inp.class_imbalance,
        label_noise_risk=inp.label_noise_risk,
        distribution_shift_risk=inp.distribution_shift_risk,
        leak_risks=list(inp.leak_signals),
        compute_constraint=inp.compute_constraint,
        interpretability_required=inp.interpretability_required,
        risk_flags=_risk_flags(inp),
        validation_recommendations=list(_VALIDATION_BY_MODALITY.get(modality, ["Define a credible validation strategy"])),
        anti_patterns=list(_ANTI_PATTERNS_BY_MODALITY.get(modality, [])),
        raw=inp.model_dump(),
    )

    dna = _maybe_enrich_with_llm(inp, dna, llm)
    return dna


def modality_baselines(modality: str) -> list[str]:
    return list(_BASELINE_BY_MODALITY.get(modality, ["Build a simple reproducible baseline"]))


def modality_validation(modality: str) -> list[str]:
    return list(_VALIDATION_BY_MODALITY.get(modality, []))
