"""Multi-modal KB seeder (v0.3.0).

Inserts mechanisms + 32+ claims covering tabular, text, image, time-series
and multimodal competitions. v0.3.0:
- Every claim has a `claim_type` (mechanism / empirical_trick / platform_specific).
- Every claim has `compatible_modalities` and `transferable_modalities`.
- Seeds are explicitly tagged `provenance_type="curated_hypothesis"` and
  `validation_status="unvalidated"` so the scoring distinguishes them from
  real validated evidence.

Idempotent.
"""

from __future__ import annotations

from typing import List

import structlog
from sqlmodel import Session, select

from ..models import Claim, Mechanism
from ..schemas import ClaimDraft, EvidenceLevel, LicenseStatus
from .knowledge_base import upsert_mechanism

log = structlog.get_logger("cmre.services.seeder")

MECHANISMS = [
    ("temporal_validation", "Temporal validation", "Use rolling-origin / walk-forward validation for time-dependent data."),
    ("adversarial_validation", "Adversarial validation", "Train classifier to distinguish train vs test; use it to design CV."),
    ("tree_baseline", "Tree-based baseline", "Gradient-boosted trees on structured features."),
    ("class_imbalance_handling", "Class imbalance handling", "Techniques for skewed label distributions."),
    ("metric_alignment", "Metric alignment", "Optimize or postprocess toward the actual evaluation metric."),
    ("regularization", "Regularization", "Methods to reduce variance / overfitting."),
    ("domain_adaptation", "Domain adaptation", "Bridge distribution shift between train and deployment."),
    ("augmentation_strategy", "Augmentation strategy", "Domain-appropriate data augmentation."),
]


def _claim(
    statement: str,
    mechanism: str,
    claim_type: str,
    compatible: List[str],
    transferable: List[str],
    applicable: List[str],
    not_recommended: List[str],
    evidence: int = 4,
    expected_effect: dict | None = None,
    cost: dict | None = None,
    risk: dict | None = None,
    tags: List[str] | None = None,
    provenance: str = "curated_hypothesis",
) -> ClaimDraft:
    return ClaimDraft(
        statement=statement,
        mechanism_slug=mechanism,
        tags=tags or [],
        applicable_when=applicable,
        not_recommended_when=not_recommended,
        expected_effect=expected_effect or {"direction": "positive", "confidence": 0.7},
        cost=cost or {"implementation": "low", "tuning": "low", "compute": "low"},
        risk=risk or {"overfit_public_lb": "low", "instability_seed": "low"},
        evidence_level=evidence,
        license_status=LicenseStatus.allowed.value,
        metadata={
            "claim_type": claim_type,
            "compatible_modalities": compatible,
            "transferable_modalities": transferable,
            "hard_exclude_modalities": [],
            "provenance_type": provenance,
            "validation_status": "unvalidated",
        },
    )


def _claim_row(draft: ClaimDraft) -> Claim:
    md = draft.metadata or {}
    return Claim(
        technique_slug=draft.technique_slug,
        mechanism_slug=draft.mechanism_slug,
        statement=draft.statement,
        summary=draft.summary,
        tags=list(draft.tags),
        modality_tags=list(md.get("compatible_modalities") or []),
        applicable_when=list(draft.applicable_when),
        not_recommended_when=list(draft.not_recommended_when),
        expected_effect=draft.expected_effect or {},
        cost=draft.cost or {},
        risk=draft.risk or {},
        evidence_level=draft.evidence_level,
        license_status=draft.license_status,
        approved=True,
        source_artifact_ids=list(draft.source_artifact_ids),
        citations=list(draft.citations),
        # v0.3.0 fields
        claim_type=md.get("claim_type", "empirical_trick"),
        compatible_modalities=list(md.get("compatible_modalities") or []),
        transferable_modalities=list(md.get("transferable_modalities") or []),
        hard_exclude_modalities=list(md.get("hard_exclude_modalities") or []),
        provenance_type=md.get("provenance_type", "curated_hypothesis"),
        validation_status=md.get("validation_status", "unvalidated"),
        reproducibility_score=0.0,
        validation_count=0,
    )


def seed(session: Session) -> int:
    """Insert mechanisms + claims. Returns count of claims inserted."""
    existing = session.exec(select(Claim)).first()
    if existing is not None:
        log.info("seed_skipped_already_present")
        return 0

    for slug, name, desc in MECHANISMS:
        upsert_mechanism(session, slug=slug, name=name, description=desc)

    drafts: List[ClaimDraft] = [
        # ========================== TABULAR ==========================
        _claim(
            "LightGBM is a strong baseline for tabular data with mixed numeric/categorical features.",
            "tree_baseline",
            claim_type="empirical_trick",
            compatible=["tabular"],
            transferable=[],
            applicable=["modality:tabular", "structured_features"],
            not_recommended=["strong_sequence_structure", "graph_structure_required"],
            evidence=5,
            tags=["tabular", "baseline", "lgbm"],
            cost={"implementation": "low", "tuning": "medium", "compute": "low"},
        ),
        _claim(
            "CatBoost often beats LightGBM when there are many high-cardinality categorical features.",
            "tree_baseline",
            claim_type="empirical_trick",
            compatible=["tabular"],
            transferable=[],
            applicable=["high_cardinality_categoricals"],
            not_recommended=["pure_numeric_features"],
            evidence=5,
            tags=["tabular", "catboost"],
        ),
        _claim(
            "For tabular binary classification with severe class imbalance, focal loss can outperform weighted log loss.",
            "class_imbalance_handling",
            claim_type="mechanism",
            compatible=["tabular"],
            transferable=["text", "image", "multimodal"],
            applicable=["class_imbalance_extreme", "binary_classification", "metric_auc_or_ap"],
            not_recommended=["balanced_classes", "calibration_required"],
            evidence=4,
            tags=["imbalance", "focal_loss"],
        ),
        _claim(
            "When timestamps exist and test is in the future, use time-based split instead of random KFold.",
            "temporal_validation",
            claim_type="mechanism",
            compatible=["tabular", "time_series"],
            transferable=[],
            applicable=["has_temporal_component", "test_is_future"],
            not_recommended=["confirmed_iid", "timestamp_is_noise"],
            evidence=5,
            tags=["temporal", "validation"],
        ),
        _claim(
            "Adversarial validation exposes train/test distribution shift before fitting any model.",
            "adversarial_validation",
            claim_type="mechanism",
            compatible=["tabular"],
            transferable=["text", "image", "audio", "multimodal"],
            applicable=["distribution_shift_risk_high"],
            not_recommended=["train_test_identical_distribution"],
            evidence=4,
            tags=["drift", "validation"],
        ),
        _claim(
            "Logistic regression / Ridge serves as a fast sanity-check baseline before any tree-based or deep model.",
            "tree_baseline",
            claim_type="empirical_trick",
            compatible=["tabular"],
            transferable=["text"],
            applicable=["any_tabular_problem"],
            not_recommended=["strong_nonlinear_structure_untreated"],
            evidence=5,
            tags=["baseline", "sanity"],
        ),
        _claim(
            "Per-row feature interactions (target encoding, count encoding) often beat raw features on tabular tasks.",
            "regularization",
            claim_type="empirical_trick",
            compatible=["tabular"],
            transferable=[],
            applicable=["high_cardinality_categoricals", "enough_data"],
            not_recommended=["small_dataset", "leakage_risk_high"],
            evidence=4,
            tags=["tabular", "feature_engineering"],
        ),

        # ========================== TEXT ==========================
        _claim(
            "TF-IDF + linear model is a strong, fast baseline for short text classification.",
            "tree_baseline",
            claim_type="empirical_trick",
            compatible=["text"],
            transferable=[],
            applicable=["short_text", "classification"],
            not_recommended=["long_context_needed", "semantic_similarity_focus"],
            evidence=5,
            tags=["text", "tfidf", "baseline"],
        ),
        _claim(
            "Fine-tuning a pretrained transformer (RoBERTa / DistilBERT) beats TF-IDF when data is medium-sized and labels are clean.",
            "augmentation_strategy",
            claim_type="empirical_trick",
            compatible=["text"],
            transferable=[],
            applicable=["pretraining_available", "clean_labels", "moderate_data"],
            not_recommended=["very_small_data", "no_pretrained_models_allowed", "noisy_labels"],
            evidence=5,
            tags=["text", "transformer", "finetuning"],
        ),
        _claim(
            "If duplicate or near-duplicate texts exist across train/test, deduplication or hold-out by source is mandatory.",
            "temporal_validation",
            claim_type="mechanism",
            compatible=["text"],
            transferable=["tabular"],
            applicable=["duplicates_suspected"],
            not_recommended=["confirmed_unique"],
            evidence=4,
            tags=["text", "validation", "deduplication"],
        ),
        _claim(
            "Back-translation and contextual augmentation help when text data is small.",
            "augmentation_strategy",
            claim_type="empirical_trick",
            compatible=["text"],
            transferable=[],
            applicable=["small_data", "languages_with_pretrained_models"],
            not_recommended=["code_switching", "domain_specific_jargon"],
            evidence=3,
            tags=["text", "augmentation"],
        ),
        _claim(
            "For NER or token-level tasks, use BIO-aware splitting to avoid leaking entity context.",
            "temporal_validation",
            claim_type="mechanism",
            compatible=["text"],
            transferable=[],
            applicable=["token_task", "named_entities"],
            not_recommended=["document_classification"],
            evidence=4,
            tags=["text", "ner", "validation"],
        ),

        # ========================== IMAGE ==========================
        _claim(
            "A pretrained ResNet or EfficientNet with standard augmentation is the fastest reliable baseline for image classification.",
            "tree_baseline",
            claim_type="empirical_trick",
            compatible=["image"],
            transferable=[],
            applicable=["classification", "pretrained_allowed"],
            not_recommended=["extreme_resolution", "domain_far_from_imagenet"],
            evidence=5,
            tags=["image", "baseline", "pretrained"],
        ),
        _claim(
            "For medical or domain-specific images, ImageNet pretraining may transfer poorly; consider self-supervised pretraining if labels are scarce.",
            "domain_adaptation",
            claim_type="mechanism",
            compatible=["image"],
            transferable=["text", "audio"],
            applicable=["domain_specific", "few_labels"],
            not_recommended=["imagenet_like_domain"],
            evidence=3,
            tags=["image", "pretraining", "ssl"],
        ),
        _claim(
            "Albumentations + mixup/cutmix improves image classification generalization when training data is limited.",
            "augmentation_strategy",
            claim_type="empirical_trick",
            compatible=["image"],
            transferable=[],
            applicable=["limited_data", "classification"],
            not_recommended=["segmentation", "detection"],
            evidence=4,
            tags=["image", "augmentation"],
        ),
        _claim(
            "For object detection, anchor-free architectures (FCOS, CenterNet) are easier to tune than anchor-based ones.",
            "tree_baseline",
            claim_type="empirical_trick",
            compatible=["image"],
            transferable=[],
            applicable=["detection"],
            not_recommended=["very_small_objects", "extreme_aspect_ratios"],
            evidence=3,
            tags=["image", "detection", "baseline"],
        ),
        _claim(
            "When test images come from different devices/sites than train, adversarial validation helps select which training images to up-weight.",
            "domain_adaptation",
            claim_type="mechanism",
            compatible=["image"],
            transferable=["text", "tabular"],
            applicable=["multi_source_data"],
            not_recommended=["single_source"],
            evidence=4,
            tags=["image", "domain_adaptation"],
        ),
        _claim(
            "For segmentation, combined Dice + BCE loss is more stable than Dice alone when class balance is uneven.",
            "metric_alignment",
            claim_type="mechanism",
            compatible=["image"],
            transferable=["tabular", "multimodal"],
            applicable=["segmentation", "uneven_classes"],
            not_recommended=["balanced_classes", "tiny_objects"],
            evidence=4,
            tags=["image", "segmentation", "loss"],
        ),

        # ========================== TIME SERIES ==========================
        _claim(
            "Seasonal naive is the mandatory sanity-check baseline for any forecasting competition.",
            "tree_baseline",
            claim_type="empirical_trick",
            compatible=["time_series"],
            transferable=[],
            applicable=["forecasting"],
            not_recommended=["non_seasonal_data"],
            evidence=5,
            tags=["time_series", "baseline"],
        ),
        _claim(
            "Use rolling-origin (walk-forward) validation for time-series, never random KFold.",
            "temporal_validation",
            claim_type="mechanism",
            compatible=["time_series"],
            transferable=["tabular"],
            applicable=["any_time_series"],
            not_recommended=["confirmed_iid_static"],
            evidence=5,
            tags=["time_series", "validation"],
        ),
        _claim(
            "For many related series, a global forecasting model (TFT, N-BEATS, LightGBM with lag features) usually beats per-series ARIMA.",
            "domain_adaptation",
            claim_type="empirical_trick",
            compatible=["time_series"],
            transferable=[],
            applicable=["many_related_series"],
            not_recommended=["single_series", "very_short_history"],
            evidence=4,
            tags=["time_series", "global_model"],
        ),
        _claim(
            "Lag features and rolling statistics are the most reliable feature engineering for tabular forecasting.",
            "regularization",
            claim_type="mechanism",
            compatible=["time_series", "tabular"],
            transferable=[],
            applicable=["forecasting"],
            not_recommended=["irregular_timestamps"],
            evidence=5,
            tags=["time_series", "feature_engineering"],
        ),
        _claim(
            "Exponentially weighted features give more weight to recent observations and often beat uniform windows.",
            "regularization",
            claim_type="empirical_trick",
            compatible=["time_series"],
            transferable=[],
            applicable=["non_stationary_series"],
            not_recommended=["stationary_series"],
            evidence=4,
            tags=["time_series", "features"],
        ),

        # ========================== MULTIMODAL ==========================
        _claim(
            "Late fusion (each modality encoded separately, concatenated) is more robust than early fusion when modalities have different missingness patterns.",
            "domain_adaptation",
            claim_type="mechanism",
            compatible=["multimodal"],
            transferable=["text", "image"],
            applicable=["missing_modality_test", "modality_mismatch"],
            not_recommended=["aligned_modalities", "tight_compute_budget"],
            evidence=4,
            tags=["multimodal", "fusion"],
        ),
        _claim(
            "Start with unimodal baselines before any multimodal model; the gap often comes from one weak modality.",
            "tree_baseline",
            claim_type="empirical_trick",
            compatible=["multimodal"],
            transferable=["text", "image"],
            applicable=["multimodal_problem"],
            not_recommended=["modality_balance_known"],
            evidence=5,
            tags=["multimodal", "baseline"],
        ),
        _claim(
            "For text + image retrieval/ranking, CLIP-style pretrained encoders give a strong zero-shot starting point.",
            "augmentation_strategy",
            claim_type="empirical_trick",
            compatible=["multimodal"],
            transferable=["text", "image"],
            applicable=["retrieval", "matching", "pretrained_allowed"],
            not_recommended=["domain_far_from_web_data"],
            evidence=4,
            tags=["multimodal", "clip", "retrieval"],
        ),
        _claim(
            "When modalities come in pairs but test has missing modalities, train a missing-modality classifier to detect this and fall back per modality.",
            "domain_adaptation",
            claim_type="mechanism",
            compatible=["multimodal"],
            transferable=["tabular"],
            applicable=["test_missing_modality"],
            not_recommended=["all_test_complete"],
            evidence=3,
            tags=["multimodal", "missing"],
        ),

        # ========================== CROSS-MODAL (mechanisms) ==========================
        _claim(
            "Postprocessing aligned to the metric (rounding, threshold tuning, calibration) often beats architecture changes.",
            "metric_alignment",
            claim_type="mechanism",
            compatible=["tabular", "text", "image", "time_series", "multimodal"],
            transferable=[],
            applicable=["any"],
            not_recommended=[],
            evidence=5,
            tags=["postprocessing", "metric"],
        ),
        _claim(
            "Probability calibration (Platt, isotonic) is essential when comparing model outputs or thresholding.",
            "metric_alignment",
            claim_type="mechanism",
            compatible=["tabular", "text", "image", "time_series", "multimodal"],
            transferable=[],
            applicable=["needs_calibration", "binary_probability_outputs"],
            not_recommended=["ranking_only_metrics"],
            evidence=5,
            tags=["calibration", "postprocessing"],
        ),
        _claim(
            "Public leaderboard signal is unreliable on small test sets (<500 rows); trust local CV more.",
            "regularization",
            claim_type="empirical_trick",
            compatible=["tabular", "text", "image", "time_series", "multimodal"],
            transferable=[],
            applicable=["small_test_set"],
            not_recommended=["large_test_set"],
            evidence=5,
            tags=["leaderboard", "validation"],
        ),
        _claim(
            "Multi-seed averaging reduces variance in CV estimates and reduces risk of overfitting to a single seed.",
            "regularization",
            claim_type="empirical_trick",
            compatible=["tabular", "text", "image", "time_series", "multimodal"],
            transferable=[],
            applicable=["any"],
            not_recommended=["stochastic_data_dominates"],
            evidence=5,
            tags=["seeds", "variance"],
        ),
        _claim(
            "Ensemble diversity matters more than ensemble size: include models that err on different examples.",
            "metric_alignment",
            claim_type="empirical_trick",
            compatible=["tabular", "text", "image", "time_series", "multimodal"],
            transferable=[],
            applicable=["ensemble"],
            not_recommended=["single_model_strong"],
            evidence=4,
            tags=["ensemble", "diversity"],
        ),
        _claim(
            "Detect and fix target leakage BEFORE tuning models; leakage inflates CV and silently kills private LB.",
            "regularization",
            claim_type="mechanism",
            compatible=["tabular", "text", "image", "time_series", "multimodal"],
            transferable=[],
            applicable=["any"],
            not_recommended=[],
            evidence=5,
            tags=["leakage", "validation"],
        ),
        _claim(
            "Contrastive pretraining learns representations that transfer across modalities with the same data structure (pairs, triplets).",
            "augmentation_strategy",
            claim_type="mechanism",
            compatible=["text", "image", "audio"],
            transferable=["multimodal"],
            applicable=["paired_data_available", "self_supervised_allowed"],
            not_recommended=["single_sample_per_entity"],
            evidence=4,
            tags=["contrastive", "representation"],
        ),
        _claim(
            "Pseudo-labeling on confident test predictions can boost performance when unlabeled test is much larger than labeled train.",
            "augmentation_strategy",
            claim_type="empirical_trick",
            compatible=["text", "image", "tabular"],
            transferable=[],
            applicable=["large_test_set", "moderate_label_noise"],
            not_recommended=["small_test_set", "high_label_noise"],
            evidence=3,
            tags=["pseudo_label", "semi_supervised"],
        ),
    ]

    count = 0
    for draft in drafts:
        session.add(_claim_row(draft))
        count += 1
    session.commit()
    log.info("seed_completed", claims=count)
    return count
