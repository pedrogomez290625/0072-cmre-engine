"""Knowledge Base service.

Thin layer over the ORM models. Every operation is idempotent where
possible and gracefully degrades on missing data.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import inspect
from sqlmodel import Session, select

from ..models import Artifact, Claim, Failure, Mechanism, ProblemProfile, ReviewTask, Technique
from ..schemas import ArtifactCandidate, ClaimDraft


def _utcnow():
    return datetime.utcnow()


# ---------------------------------------------------------------------------
# Artifact
# ---------------------------------------------------------------------------

def upsert_artifact(session: Session, candidate: ArtifactCandidate) -> Artifact:
    existing = session.exec(select(Artifact).where(Artifact.url == candidate.url)).first()
    if existing:
        return existing

    pub_at = None
    if candidate.published_at:
        try:
            pub_at = datetime.fromisoformat(candidate.published_at.replace("Z", "+00:00"))
        except Exception:
            pub_at = None

    artifact = Artifact(
        source_type=candidate.source_type,
        platform=candidate.platform,
        url=candidate.url,
        title=candidate.title,
        author=candidate.author,
        published_at=pub_at,
        license=candidate.license,
        license_status=candidate.license_status,
        processing_state="new",
        metadata_json=candidate.metadata or {},
    )
    session.add(artifact)
    session.commit()
    session.refresh(artifact)
    return artifact


def get_artifacts_for_extraction(session: Session, limit: int = 10) -> list[Artifact]:
    rows = session.exec(
        select(Artifact)
        .where(Artifact.processing_state == "new")
        .where(Artifact.license_status == "allowed")
        .order_by(Artifact.created_at)
        .limit(limit)
    ).all()
    return list(rows)


def mark_artifact_processed(session: Session, artifact_id: int, state: str) -> None:
    artifact = session.get(Artifact, artifact_id)
    if artifact:
        artifact.processing_state = state
        artifact.updated_at = _utcnow()
        session.add(artifact)
        session.commit()


# ---------------------------------------------------------------------------
# Claims
# ---------------------------------------------------------------------------

def create_claim_draft(session: Session, draft: ClaimDraft) -> Claim:
    claim = Claim(
        technique_slug=draft.technique_slug,
        mechanism_slug=draft.mechanism_slug,
        statement=draft.statement,
        summary=draft.summary,
        tags=list(draft.tags),
        modality_tags=_infer_modality_tags(draft.tags, draft.applicable_when),
        applicable_when=list(draft.applicable_when),
        not_recommended_when=list(draft.not_recommended_when),
        expected_effect=draft.expected_effect or {},
        cost=draft.cost or {},
        risk=draft.risk or {},
        evidence_level=draft.evidence_level,
        license_status=draft.license_status,
        approved=False,
        source_artifact_ids=list(draft.source_artifact_ids),
        citations=list(draft.citations),
    )
    session.add(claim)
    session.commit()
    session.refresh(claim)
    return claim


def _infer_modality_tags(tags: list[str], applicable_when: list[str]) -> list[str]:
    MODAL = {"tabular", "text", "image", "video", "audio", "time_series", "graph", "multimodal"}
    out: list[str] = []
    for source in (tags or []) + (applicable_when or []):
        s = source.lower() if isinstance(source, str) else ""
        for m in MODAL:
            if m in s and m not in out:
                out.append(m)
    return out or ["any"]


def approve_claim(session: Session, claim_id: int) -> None:
    claim = session.get(Claim, claim_id)
    if claim:
        claim.approved = True
        claim.updated_at = _utcnow()
        session.add(claim)
        session.commit()


def reject_claim(session: Session, claim_id: int, note: str = "") -> None:
    claim = session.get(Claim, claim_id)
    if claim:
        claim.approved = False
        claim.summary = (claim.summary or "") + (f"\n\nRejected: {note}" if note else "")
        claim.updated_at = _utcnow()
        session.add(claim)
        session.commit()


def get_approved_claims(
    session: Session,
    modality: Optional[str] = None,
    task_type: Optional[str] = None,
) -> list[Claim]:
    stmt = select(Claim).where(Claim.approved == True)  # noqa: E712
    claims = session.exec(stmt).all()
    out = []
    for c in claims:
        if modality and c.modality_tags and modality not in c.modality_tags and "any" not in c.modality_tags:
            continue
        if task_type and task_type not in (c.tags or []):
            # Soft match; we don't strictly filter, but boost
            pass
        out.append(c)
    return list(out)


# ---------------------------------------------------------------------------
# Failures
# ---------------------------------------------------------------------------

def create_failure(session: Session, failure: Failure) -> Failure:
    session.add(failure)
    session.commit()
    session.refresh(failure)
    return failure


# ---------------------------------------------------------------------------
# Mechanisms & techniques (ontology)
# ---------------------------------------------------------------------------

def upsert_mechanism(session: Session, slug: str, name: str, description: str | None = None, parent_slug: str | None = None) -> Mechanism:
    existing = session.exec(select(Mechanism).where(Mechanism.slug == slug)).first()
    if existing:
        return existing
    m = Mechanism(slug=slug, name=name, description=description, parent_slug=parent_slug)
    session.add(m)
    session.commit()
    session.refresh(m)
    return m


def upsert_technique(session: Session, slug: str, name: str, category: str | None = None, mechanism_slug: str | None = None) -> Technique:
    existing = session.exec(select(Technique).where(Technique.slug == slug)).first()
    if existing:
        return existing
    t = Technique(slug=slug, name=name, category=category, mechanism_slug=mechanism_slug)
    session.add(t)
    session.commit()
    session.refresh(t)
    return t


# ---------------------------------------------------------------------------
# Review tasks
# ---------------------------------------------------------------------------

def create_review_task(
    session: Session,
    entity_type: str,
    entity_id: int,
    status: str = "pending",
    notes: str | None = None,
    payload: dict | None = None,
) -> ReviewTask:
    rt = ReviewTask(
        entity_type=entity_type,
        entity_id=entity_id,
        status=status,
        notes=notes,
        payload_json=payload or {},
    )
    session.add(rt)
    session.commit()
    session.refresh(rt)
    return rt


# ---------------------------------------------------------------------------
# Problem DNA persistence
# ---------------------------------------------------------------------------

def save_problem_dna(session: Session, competition_id: Optional[int], dna: dict) -> ProblemProfile:
    profile = ProblemProfile(
        competition_id=competition_id,
        dna_json=dna,
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
