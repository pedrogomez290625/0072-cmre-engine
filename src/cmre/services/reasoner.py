"""Reasoning engine: bridges DNA → ranked techniques.

v0.3.0 changes:
- Soft modality filter (modality is a bonus, not a hard exclusion).
- Deterministic base score from `services.scoring` is the primary ranking.
- LLM rerank is bounded to ±0.10 (recorded in score_breakdown).
- Provenance / license / validation multipliers are explicit.
"""

from __future__ import annotations

from typing import List, Optional

import structlog
from sqlmodel import Session, select

from ..agents.base import LLMClient
from ..models import Claim
from ..schemas import ProblemDNA, RankedClaim, ScoreBreakdown
from .embedder import Embedder
from .retrieval import HybridRetriever, LLMReranker
from .scoring import compute_deterministic_score

log = structlog.get_logger("cmre.services.reasoner")


def _passes_hard_filters(claim: Claim, allow_unknown_license: bool) -> bool:
    """Hard filters are now ONLY about license / approval / hard modality excludes.

    Cross-modal transfer is preserved.
    """
    if claim.license_status == "forbidden":
        return False
    if claim.license_status == "unknown" and not allow_unknown_license:
        return False
    if not claim.approved:
        return False
    return True


def _to_ranked(claim: Claim, dna: ProblemDNA, breakdown: ScoreBreakdown) -> RankedClaim:
    """Convert a Claim + breakdown into a RankedClaim."""
    from ..schemas import SourceRef

    sources: list[SourceRef] = []
    for art_id in claim.source_artifact_ids or []:
        sources.append(SourceRef(type="artifact", identifier=f"artifact:{art_id}", license_status=claim.license_status))
    for cit in claim.citations or []:
        try:
            sources.append(SourceRef(**cit))
        except Exception:
            pass

    return RankedClaim(
        claim_id=claim.id,
        statement=claim.statement,
        mechanism_slug=claim.mechanism_slug,
        technique_slug=claim.technique_slug,
        score=breakdown.final_score,
        reasons=list(breakdown.reasons),
        warnings=list(breakdown.warnings),
        evidence_level=claim.evidence_level,
        license_status=claim.license_status,
        recency_weight=breakdown.recency_factor,
        embedding_similarity=None,
        claim_type=claim.claim_type,
        provenance_type=claim.provenance_type,
        validation_status=claim.validation_status,
        score_breakdown=breakdown,
        sources=sources,
        review_status="approved" if claim.approved else "pending",
    )


def retrieve_and_rank(
    session: Session,
    dna: ProblemDNA,
    llm: LLMClient,
    limit: int = 20,
    allow_unknown_license: bool = False,
    candidate_pool: int = 50,
) -> List[RankedClaim]:
    """Pull candidates, deterministic-rank them, optionally LLM-rerank top-K.

    Returns top `limit` RankedClaim sorted by final_score.
    """
    # 1. Candidate retrieval (broad recall by embedding).
    from ..config import get_settings

    settings = get_settings()
    embedder = Embedder(llm, settings=settings)
    retriever = HybridRetriever(llm, embedder, settings=settings)
    raw = retriever.retrieve_candidates(dna, session, limit=candidate_pool)

    # 2. Hard filters (license / approval only).
    candidates: list[Claim] = [c for c, _ in raw if _passes_hard_filters(c, allow_unknown_license)]

    if not candidates:
        return []

    # 3. Deterministic scoring (the primary ranking).
    breakdowns: dict[int, ScoreBreakdown] = {
        c.id: compute_deterministic_score(c, dna) for c in candidates if c.id is not None
    }

    # 4. Optional LLM rerank on top-K (bounded ±0.10).
    ranked = retriever.rerank_optional(
        dna=dna,
        candidates=candidates,
        breakdowns=breakdowns,
        top_n=min(limit * 2, len(candidates)),
    )

    # 5. Final sort by final_score and trim.
    ranked.sort(key=lambda x: x.score, reverse=True)
    return ranked[:limit]


def rank_claims(
    claims: List[Claim],
    dna: ProblemDNA,
    llm: Optional[LLMClient] = None,
    allow_unknown_license: bool = False,
) -> List[RankedClaim]:
    """Pure function: rank a given list of claims against a DNA.

    Useful for tests and for the golden-case evaluator (no DB needed).
    Works with both persisted claims (id != None) and non-persisted
    in-memory claim objects (id is None).
    """
    filtered = [c for c in claims if _passes_hard_filters(c, allow_unknown_license)]
    breakdowns: list[tuple[Claim, ScoreBreakdown]] = [
        (c, compute_deterministic_score(c, dna)) for c in filtered
    ]
    ranked: list[RankedClaim] = [_to_ranked(c, dna, bd) for c, bd in breakdowns]
    ranked.sort(key=lambda x: x.score, reverse=True)
    return ranked
