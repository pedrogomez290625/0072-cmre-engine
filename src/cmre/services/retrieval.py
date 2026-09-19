"""Hybrid retrieval: embeddings + (later) optional LLM rerank.

v0.3.0: LLM rerank is BOUNDED. It contributes at most ±0.10 to the final
score. The base ranking is always deterministic (from services.scoring).

The deterministic base ranking is what makes the system:
- reproducible (same DNA + same KB → same ranking)
- auditable (breakdown explains the score)
- testable (no flaky LLM assertions)
"""

from __future__ import annotations

from typing import List, Optional, Tuple

import structlog
from sqlmodel import Session, select

from ..agents.base import LLMClient
from ..config import Settings, get_settings
from ..models import Claim
from ..schemas import ProblemDNA, RankedClaim, ScoreBreakdown
from .embedder import Embedder, cosine_similarity
from .scoring import apply_llm_delta

log = structlog.get_logger("cmre.services.retrieval")


class HybridRetriever:
    def __init__(self, llm: LLMClient, embedder: Embedder, settings: Optional[Settings] = None):
        self.llm = llm
        self.embedder = embedder
        self.settings = settings or get_settings()

    def retrieve_candidates(
        self,
        dna: ProblemDNA,
        session: Session,
        limit: int = 50,
    ) -> List[Tuple[Claim, float]]:
        """Broad recall by embedding cosine similarity.

        Hard filters (license / approval) are NOT applied here — the reasoner
        applies them centrally so the breakdown is consistent.
        """
        claims = session.exec(select(Claim).where(Claim.approved == True)).all()  # noqa: E712
        if not claims:
            return []

        dna_vec = self.embedder.embed_problem_dna(dna)
        scored: list[Tuple[Claim, float]] = []
        for c in claims:
            if c.license_status == "forbidden":
                continue
            text = self.embedder.embed_claim(
                c.statement,
                c.applicable_when,
                c.not_recommended_when,
                c.tags,
            )
            sim = cosine_similarity(dna_vec, text)
            scored.append((c, sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:limit]

    def rerank_optional(
        self,
        dna: ProblemDNA,
        candidates: List[Claim],
        breakdowns: dict[int, ScoreBreakdown] | None = None,
        top_n: int = 20,
    ) -> List[RankedClaim]:
        """Apply optional LLM rerank as a bounded delta over deterministic ranking.

        `breakdowns` is optional; if not provided, deterministic scores are
        computed here (one extra call per candidate, fine for small pools).
        Returns top `top_n` RankedClaim.
        """
        from ..services.scoring import compute_deterministic_score
        from .reasoner import _to_ranked

        if not candidates:
            return []

        # Compute or reuse deterministic scores.
        scored: list[tuple[Claim, ScoreBreakdown]] = []
        for c in candidates:
            if breakdowns is not None and c.id in breakdowns:
                scored.append((c, breakdowns[c.id]))
            else:
                scored.append((c, compute_deterministic_score(c, dna)))

        # Order by deterministic score first.
        scored.sort(key=lambda x: x[1].final_score, reverse=True)

        # Build ranked claims with deterministic scores.
        ranked: list[RankedClaim] = [_to_ranked(c, dna, bd) for c, bd in scored]

        # Optionally apply LLM rerank on top-K.
        llm_judgments = self._judge_top_k(dna, ranked[:top_n])
        for rc, j in zip(ranked[:top_n], llm_judgments):
            if j is None:
                continue
            new_breakdown = apply_llm_delta(rc.score_breakdown, j.get("score", 50))
            rc.score_breakdown = new_breakdown
            rc.score = new_breakdown.final_score
            if j.get("reason"):
                rc.reasons.append(f"LLM: {j['reason']}")
            if j.get("contraindication"):
                rc.warnings.append(f"LLM: {j['contraindication']}")

        ranked.sort(key=lambda x: x.score, reverse=True)
        return ranked[:top_n]

    def _judge_top_k(self, dna: ProblemDNA, ranked: List[RankedClaim]) -> List[Optional[dict]]:
        """Ask LLM to judge top-K. Returns judgments aligned to ranked.

        Failures degrade gracefully — None means "no judgment, keep deterministic".
        """
        if not ranked:
            return []
        try:
            judgments = self._judge_batch(dna, ranked)
        except Exception as exc:
            log.warning("llm_rerank_failed_skip", error=str(exc))
            return [None] * len(ranked)

        if not isinstance(judgments, list) or len(judgments) != len(ranked):
            return [None] * len(ranked)
        return [j if isinstance(j, dict) else None for j in judgments]

    def _judge_batch(self, dna: ProblemDNA, ranked: List[RankedClaim]) -> List[Optional[dict]]:
        """Ask the LLM to score each candidate. Cached by DNA+claim-set hash."""
        cache_key = self._cache_key(dna, ranked)
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached

        system_prompt = (
            "You are an expert evaluating whether conditional ML claims apply to a "
            "competition. Return JSON: {\"judgments\": [{score: 0-100, reason: str, "
            "contraindication: str|null}]} aligned to indices. Be conservative."
        )
        user_prompt = (
            f"Problem DNA:\n"
            f"- Title: {dna.title}\n"
            f"- Modality: {dna.modality}\n"
            f"- Task: {dna.task_type}\n"
            f"- Metric: {dna.metric} ({dna.metric_family})\n"
            f"- Class imbalance: {dna.class_imbalance}\n"
            f"- Label noise: {dna.label_noise_risk}\n"
            f"- Distribution shift: {dna.distribution_shift_risk}\n"
            f"- Compute: {dna.compute_constraint}\n"
            f"- Risk flags: {', '.join(dna.risk_flags) or 'none'}\n\n"
            "Claims (index, mechanism, statement):\n"
        )
        for i, rc in enumerate(ranked):
            user_prompt += (
                f"\n[{i}] {rc.mechanism_slug or '?'} :: {rc.statement}\n"
            )
        user_prompt += '\nReturn JSON: {"judgments": [...]}.'

        payload = self.llm.complete_json(system_prompt, user_prompt, schema_name="ClaimJudgments")
        if not isinstance(payload, dict):
            out: list[Optional[dict]] = [None] * len(ranked)
        else:
            judgments = payload.get("judgments") or payload.get("results") or []
            if not isinstance(judgments, list) or len(judgments) != len(ranked):
                out = [None] * len(ranked)
            else:
                out = [j if isinstance(j, dict) else None for j in judgments]

        self._cache_set(cache_key, out)
        return out

    # --- LLM judgment cache --------------------------------------------------

    _cache: dict[str, list] = {}

    def _cache_key(self, dna: ProblemDNA, ranked: List[RankedClaim]) -> str:
        import hashlib
        dna_blob = f"{dna.title}|{dna.modality}|{dna.task_type}|{dna.metric}|{','.join(sorted(dna.risk_flags))}"
        claims_blob = "|".join(f"{rc.claim_id}:{rc.statement}" for rc in ranked)
        return hashlib.sha1((dna_blob + "::" + claims_blob).encode("utf-8")).hexdigest()

    def _cache_get(self, key: str):
        return self._cache.get(key)

    def _cache_set(self, key: str, value: list) -> None:
        if len(self._cache) > 256:  # bound the cache
            self._cache.clear()
        self._cache[key] = value


# --- Legacy exports preserved for backward compatibility ---------------------

class LLMReranker:
    """Legacy class kept for compatibility; new code should use
    HybridRetriever.rerank_optional().
    """

    def __init__(self, llm: LLMClient, settings: Optional[Settings] = None):
        self.llm = llm
        self.settings = settings or get_settings()

    def rerank(self, dna: ProblemDNA, candidates: List[Tuple[Claim, float]], top_n: int = 20):
        # Just return top_n by similarity, no LLM.
        return [
            RankedClaim(
                claim_id=c.id,
                statement=c.statement,
                mechanism_slug=c.mechanism_slug,
                technique_slug=c.technique_slug,
                score=sim,
                reasons=["legacy rerank (no LLM)"],
                evidence_level=c.evidence_level,
                license_status=c.license_status,
            )
            for c, sim in candidates[:top_n]
        ]
