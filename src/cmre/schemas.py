"""Competition-agnostic schemas.

DNA, claims, plans are designed to work for tabular, text, image, time-series,
audio and multimodal competitions without code changes. Modality-specific
behavior is captured in tags and condition strings, not in code branches.
"""

from __future__ import annotations

from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SourceType(str, Enum):
    notebook = "notebook"
    writeup = "writeup"
    paper = "paper"
    repo = "repo"
    model = "model"
    dataset = "dataset"
    forum = "forum"
    other = "other"


class Platform(str, Enum):
    kaggle = "kaggle"
    drivendata = "drivendata"
    zindi = "zindi"
    aicrowd = "aicrowd"
    codalab = "codalab"
    github = "github"
    arxiv = "arxiv"
    huggingface = "huggingface"
    semantic_scholar = "semantic_scholar"
    other = "other"


class LicenseStatus(str, Enum):
    allowed = "allowed"
    restricted = "restricted"
    forbidden = "forbidden"
    unknown = "unknown"


class EvidenceLevel(IntEnum):
    rumor = 0
    mentioned = 1
    code_visible = 2
    partially_reproduced = 3
    internal_ablation = 4
    multiple_problems = 5
    theoretical_strong = 6


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class EffectDirection(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    mixed = "mixed"


# --- v0.3.0: claim lifecycle -------------------------------------------------

class ClaimType(str, Enum):
    """How a claim should be ranked and decayed.

    - mechanism: fundamental mechanism (focal loss, contrastive, calibration).
      Decays slowly. Transfers across modalities.
    - empirical_trick: a heuristic that empirically helps (specific tuning,
      platform workarounds). Medium decay. Mostly modality-bound.
    - platform_specific: tied to a specific platform / leaderboard behavior.
      Fast decay. Hard filter to its native platform.
    """
    mechanism = "mechanism"
    empirical_trick = "empirical_trick"
    platform_specific = "platform_specific"


class ProvenanceType(str, Enum):
    paper = "paper"
    competition_writeup = "competition_writeup"
    notebook = "notebook"
    internal_experiment = "internal_experiment"
    curated_hypothesis = "curated_hypothesis"
    llm_extraction = "llm_extraction"
    human_annotation = "human_annotation"
    unknown = "unknown"


class ValidationStatus(str, Enum):
    unvalidated = "unvalidated"
    partially_validated = "partially_validated"
    validated = "validated"
    contradicted = "contradicted"


# ---------------------------------------------------------------------------
# Score breakdown (v0.3.0: deterministic + bounded LLM delta)
# ---------------------------------------------------------------------------

class ScoreBreakdown(BaseModel):
    """Transparent breakdown of how a claim's score was computed.

    The deterministic score = weighted sum of the named components, scaled
    by provenance / license multipliers and modality soft-bonus. LLM delta
    is recorded separately and capped at ±0.10.
    """

    mechanism_fit: float = 0.0
    evidence_quality: float = 0.0
    constraint_compatibility: float = 0.0
    recency_factor: float = 0.0

    modality_bonus: float = 1.0
    provenance_multiplier: float = 1.0
    license_multiplier: float = 1.0

    deterministic_score: float = 0.0
    llm_rerank_delta: float = 0.0
    final_score: float = 0.0

    reasons: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class SourceRef(BaseModel):
    type: str  # paper | notebook | writeup | internal_experiment
    identifier: str  # arxiv:..., github:..., run_id, etc.
    license_status: str = "unknown"
    effect: Optional[str] = None


# --- v0.3.0: golden case schema ---------------------------------------------

class GoldenCase(BaseModel):
    case_id: str
    description: str

    competition_input: dict  # raw CompetitionInput-compatible dict

    expected_dna_flags: List[str] = Field(default_factory=list)
    expected_validation_recommendations: List[str] = Field(default_factory=list)
    expected_anti_patterns: List[str] = Field(default_factory=list)
    expected_top_mechanisms: List[str] = Field(default_factory=list)
    forbidden_recommendations: List[str] = Field(default_factory=list)

    known_outcome: Optional[dict] = None  # public_score, private_score, placement, etc.


# ---------------------------------------------------------------------------
# Canonical taxonomy (free-form strings but a closed vocabulary helps retrieval)
# ---------------------------------------------------------------------------

MODALITIES = {
    "tabular",
    "text",
    "image",
    "video",
    "audio",
    "time_series",
    "graph",
    "multimodal",
}

TASK_TYPES = {
    "binary_classification",
    "multiclass_classification",
    "regression",
    "ranking",
    "detection",
    "segmentation",
    "generation",
    "recommendation",
    "forecasting",
    "anomaly_detection",
    "matching",
    "other",
}

METRIC_FAMILIES = {
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
    "recall_at_k",
    "precision_at_k",
    "bleu",
    "rouge",
    "wer",
    "custom",
}


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

class ArtifactCandidate(BaseModel):
    model_config = ConfigDict(extra="allow")

    source_type: str
    platform: str
    url: str
    title: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[str] = None
    competition_external_id: Optional[str] = None

    license: Optional[str] = None
    license_status: str = LicenseStatus.unknown.value

    metadata: Dict[str, Any] = Field(default_factory=dict)


class ClaimDraft(BaseModel):
    model_config = ConfigDict(extra="allow")

    statement: str
    summary: Optional[str] = None

    technique_slug: Optional[str] = None
    mechanism_slug: Optional[str] = None

    tags: List[str] = Field(default_factory=list)

    # Free-form strings, but typically:
    # modality, task_type, metric_family, presence of temporal/group/label_noise
    applicable_when: List[str] = Field(default_factory=list)
    not_recommended_when: List[str] = Field(default_factory=list)

    expected_effect: Dict[str, Any] = Field(default_factory=dict)
    cost: Dict[str, Any] = Field(default_factory=dict)
    risk: Dict[str, Any] = Field(default_factory=dict)

    evidence_level: int = EvidenceLevel.mentioned.value
    license_status: str = LicenseStatus.unknown.value

    source_artifact_ids: List[int] = Field(default_factory=list)
    citations: List[Dict[str, Any]] = Field(default_factory=list)


class CompetitionInput(BaseModel):
    """Generic input describing any ML competition.

    Fields are intentionally permissive: a competition may have empty
    description (cold start) or rich description (post-mortem style).
    The profiler fills the gaps with sensible defaults.
    """

    model_config = ConfigDict(extra="allow")

    title: str
    platform: str = Platform.other.value
    task_type: str = "other"
    modality: str = "tabular"  # most common default; profiler may override
    metric: str = "custom"

    description: Optional[str] = None
    data_summary: Optional[str] = None
    rules: Dict[str, Any] = Field(default_factory=dict)

    # Profiled flags (may be auto-detected by an LLM from description)
    has_temporal_component: bool = False
    has_group_structure: bool = False
    is_iid: bool = True
    has_external_data_allowed: Optional[bool] = None
    has_pretrained_models_allowed: Optional[bool] = None

    class_imbalance: str = "unknown"  # unknown|low|medium|high|extreme
    label_noise_risk: str = "unknown"  # unknown|low|medium|high
    distribution_shift_risk: str = "unknown"
    leak_risk: str = "unknown"  # unknown|none|low|medium|high
    leak_signals: List[str] = Field(default_factory=list)

    compute_constraint: str = "unknown"  # unknown|low|medium|high|gpu_only
    interpretability_required: bool = False
    submission_limit: Optional[int] = None


# ---------------------------------------------------------------------------
# Problem DNA — fully derived, multi-modal
# ---------------------------------------------------------------------------

class ProblemDNA(BaseModel):
    title: str
    platform: str
    task_type: str
    modality: str
    metric: str
    metric_family: str = "custom"

    has_temporal_component: bool = False
    has_group_structure: bool = False
    is_iid: bool = True
    external_data_allowed: Optional[bool] = None
    pretrained_models_allowed: Optional[bool] = None

    class_imbalance: str = "unknown"
    label_noise_risk: str = "unknown"
    distribution_shift_risk: str = "unknown"
    leak_risks: List[str] = Field(default_factory=list)
    compute_constraint: str = "unknown"
    interpretability_required: bool = False
    risk_flags: List[str] = Field(default_factory=list)
    validation_recommendations: List[str] = Field(default_factory=list)
    anti_patterns: List[str] = Field(default_factory=list)

    raw: Dict[str, Any] = Field(default_factory=dict)


class RankedClaim(BaseModel):
    claim_id: Optional[int] = None
    statement: str
    mechanism_slug: Optional[str] = None
    technique_slug: Optional[str] = None
    score: float
    reasons: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    evidence_level: int = 1
    license_status: str = LicenseStatus.unknown.value
    recency_weight: float = 1.0
    embedding_similarity: Optional[float] = None

    # --- v0.3.0 additions ---
    claim_type: str = "empirical_trick"
    provenance_type: str = "unknown"
    validation_status: str = "unvalidated"
    score_breakdown: Optional[ScoreBreakdown] = None
    sources: List[SourceRef] = Field(default_factory=list)
    review_status: str = "approved"


# ---------------------------------------------------------------------------
# Plans and reports
# ---------------------------------------------------------------------------

class ExperimentPhase(BaseModel):
    name: str
    objective: str
    actions: List[str]
    success_criteria: List[str]
    risks: List[str] = Field(default_factory=list)


class ExperimentPlan(BaseModel):
    competition_title: str
    dna_summary: str
    phases: List[ExperimentPhase]
    top_techniques: List[RankedClaim]
    avoid: List[str]
    next_steps: List[str]


# ---------------------------------------------------------------------------
# Coding tasks for Jules / Antigravity
# ---------------------------------------------------------------------------

class JulesTask(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    title: str
    description: str
    acceptance_criteria: List[str] = Field(default_factory=list)
    files: List[str] = Field(default_factory=list)
    labels: List[str] = Field(default_factory=list)
    priority: str = "medium"
