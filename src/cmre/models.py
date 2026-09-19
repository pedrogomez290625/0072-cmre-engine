"""Database models with pgvector embeddings.

Embedding columns live alongside relational data. Embeddings are stored as
JSON-friendly lists for portability; pgvector's optional index is added via
a migration (see db_migrations/).
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Artifacts
# ---------------------------------------------------------------------------

class Artifact(SQLModel, table=True):
    __tablename__ = "artifacts"

    id: Optional[int] = Field(default=None, primary_key=True)
    source_type: str = Field(index=True)
    platform: str = Field(index=True)
    url: str = Field(index=True, unique=True)
    title: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    competition_external_id: Optional[str] = Field(default=None, index=True)

    license: Optional[str] = None
    license_status: str = Field(default="unknown", index=True)

    content_hash: Optional[str] = None
    raw_path: Optional[str] = None

    processing_state: str = Field(default="new", index=True)

    metadata_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    embedding: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


# ---------------------------------------------------------------------------
# Competitions + Problem DNA
# ---------------------------------------------------------------------------

class Competition(SQLModel, table=True):
    __tablename__ = "competitions"

    id: Optional[int] = Field(default=None, primary_key=True)

    platform: str = Field(index=True)
    external_id: Optional[str] = Field(default=None, index=True)
    title: str
    url: Optional[str] = None

    task_type: Optional[str] = Field(default=None, index=True)
    modality: Optional[str] = Field(default=None, index=True)
    metric: Optional[str] = Field(default=None, index=True)

    rules_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    data_profile_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    status: str = Field(default="active", index=True)

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class ProblemProfile(SQLModel, table=True):
    __tablename__ = "problem_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)

    competition_id: Optional[int] = Field(default=None, foreign_key="competitions.id", index=True)

    dna_json: Dict[str, Any] = Field(sa_column=Column(JSON))
    embedding: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=utcnow)


# ---------------------------------------------------------------------------
# Ontology
# ---------------------------------------------------------------------------

class Mechanism(SQLModel, table=True):
    __tablename__ = "mechanisms"

    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    name: str
    description: Optional[str] = None
    parent_slug: Optional[str] = Field(default=None, index=True)


class Technique(SQLModel, table=True):
    __tablename__ = "techniques"

    id: Optional[int] = Field(default=None, primary_key=True)

    slug: str = Field(index=True, unique=True)
    name: str
    category: Optional[str] = Field(default=None, index=True)
    mechanism_slug: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = None

    paper_refs: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    code_refs: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    model_refs: List[str] = Field(default_factory=list, sa_column=Column(JSON))


# ---------------------------------------------------------------------------
# Claims and failures (the heart of the KB)
# ---------------------------------------------------------------------------

class Claim(SQLModel, table=True):
    __tablename__ = "claims"

    id: Optional[int] = Field(default=None, primary_key=True)

    technique_slug: Optional[str] = Field(default=None, index=True)
    mechanism_slug: Optional[str] = Field(default=None, index=True)
    problem_profile_id: Optional[int] = Field(default=None, foreign_key="problem_profiles.id", index=True)

    statement: str
    summary: Optional[str] = None

    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    modality_tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))  # for fast filtering

    applicable_when: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    not_recommended_when: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    expected_effect: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    cost: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    risk: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    evidence_level: int = Field(default=1, index=True)
    published_at: Optional[datetime] = Field(default=None, index=True)
    license_status: str = Field(default="unknown", index=True)

    approved: bool = Field(default=False, index=True)

    source_artifact_ids: List[int] = Field(default_factory=list, sa_column=Column(JSON))
    citations: List[Dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))

    # --- v0.3.0 additions -------------------------------------------------

    # Type of claim: drives recency policy and filter strictness.
    claim_type: str = Field(default="empirical_trick", index=True)

    # Modality classification:
    # - compatible_modalities: modalities where this applies cleanly
    # - transferable_modalities: cross-modal mechanisms worth boosting
    # - hard_exclude_modalities: NEVER applies here (rare; e.g., CV-only)
    compatible_modalities: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    transferable_modalities: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    hard_exclude_modalities: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    # Provenance + validation lifecycle:
    provenance_type: str = Field(default="unknown", index=True)
    validation_status: str = Field(default="unvalidated", index=True)
    last_validated_at: Optional[datetime] = Field(default=None, index=True)
    validation_count: int = Field(default=0)
    reproducibility_score: float = Field(default=0.0)

    # Relationship to other claims (for contradiction detection):
    supports_claim_ids: List[int] = Field(default_factory=list, sa_column=Column(JSON))
    contradicts_claim_ids: List[int] = Field(default_factory=list, sa_column=Column(JSON))

    embedding: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class Failure(SQLModel, table=True):
    __tablename__ = "failures"

    id: Optional[int] = Field(default=None, primary_key=True)

    technique_slug: Optional[str] = Field(default=None, index=True)
    mechanism_slug: Optional[str] = Field(default=None, index=True)
    problem_profile_id: Optional[int] = Field(default=None, foreign_key="problem_profiles.id", index=True)

    statement: str
    symptoms: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    root_cause_hypothesis: Optional[str] = None
    lesson: Optional[str] = None
    condition_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    evidence_level: int = Field(default=1, index=True)
    source_artifact_ids: List[int] = Field(default_factory=list, sa_column=Column(JSON))
    approved: bool = Field(default=False, index=True)

    created_at: datetime = Field(default_factory=utcnow)


# ---------------------------------------------------------------------------
# Experiments + review tasks
# ---------------------------------------------------------------------------

class Experiment(SQLModel, table=True):
    __tablename__ = "experiments"

    id: Optional[int] = Field(default=None, primary_key=True)

    competition_id: Optional[int] = Field(default=None, foreign_key="competitions.id", index=True)

    hypothesis: str
    techniques_used: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    config_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    result_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    decision: str = Field(default="investigate", index=True)
    notes: Optional[str] = None
    run_id: Optional[str] = None

    created_at: datetime = Field(default_factory=utcnow)


class ReviewTask(SQLModel, table=True):
    __tablename__ = "review_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)

    entity_type: str = Field(index=True)
    entity_id: int = Field(index=True)

    status: str = Field(default="pending", index=True)
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    payload_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=utcnow)
