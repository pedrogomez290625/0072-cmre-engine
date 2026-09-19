"""Embedder service.

Wraps the LLMClient.embed() interface to embed Problem DNA, claims, and
artifacts in a consistent way. Caches results in-process for repeat calls
within a single run.
"""

from __future__ import annotations

import hashlib
from typing import Dict, List, Optional

import structlog

from ..agents.base import LLMClient
from ..config import Settings, get_settings
from ..schemas import ArtifactCandidate, ProblemDNA

log = structlog.get_logger("cmre.services.embedder")


class Embedder:
    def __init__(self, llm: LLMClient, settings: Optional[Settings] = None):
        self.llm = llm
        self.settings = settings or get_settings()
        self._cache: Dict[str, List[float]] = {}
        self.dim = self.settings.embedding_dim

    # --- Public API ------------------------------------------------------

    def embed_problem_dna(self, dna: ProblemDNA) -> List[float]:
        parts = [
            dna.title,
            dna.platform,
            dna.task_type,
            dna.modality,
            dna.metric,
            dna.metric_family,
            "temporal" if dna.has_temporal_component else "",
            "group_structure" if dna.has_group_structure else "",
            "iid" if dna.is_iid else "non_iid",
            "imbalance:" + dna.class_imbalance,
            "label_noise:" + dna.label_noise_risk,
            "distribution_shift:" + dna.distribution_shift_risk,
            "compute:" + dna.compute_constraint,
            "interpretability" if dna.interpretability_required else "",
            " ".join(dna.leak_risks),
            " ".join(dna.risk_flags),
            " ".join(dna.validation_recommendations),
            " ".join(dna.anti_patterns),
        ]
        return self._embed(" ".join(p for p in parts if p))

    def embed_claim(
        self,
        statement: str,
        applicable_when: Optional[List[str]] = None,
        not_recommended_when: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ) -> List[float]:
        bits = [statement]
        if applicable_when:
            bits.append("APPLIES WHEN: " + " | ".join(applicable_when))
        if not_recommended_when:
            bits.append("NOT WHEN: " + " | ".join(not_recommended_when))
        if tags:
            bits.append("TAGS: " + " ".join(tags))
        return self._embed(" ".join(bits))

    def embed_artifact(self, candidate: ArtifactCandidate) -> List[float]:
        bits = [
            candidate.title or "",
            candidate.source_type,
            candidate.platform,
            (candidate.metadata.get("abstract") or "")[:300],
            (candidate.metadata.get("description") or "")[:300],
            " ".join(candidate.metadata.get("topics") or []) if isinstance(candidate.metadata.get("topics"), list) else "",
        ]
        return self._embed(" ".join(b for b in bits if b))

    # --- Internals -------------------------------------------------------

    def _embed(self, text: str) -> List[float]:
        if not text:
            text = " "
        key = hashlib.sha1(text.encode("utf-8")).hexdigest()
        if key in self._cache:
            return self._cache[key]
        try:
            vecs = self.llm.embed([text])
        except Exception as exc:
            log.warning("embed_failed_fallback_hash", error=str(exc))
            vecs = [self._hash_embedding(text)]
        vec = self._normalize_shape(vecs[0] if vecs else [])
        # If the LLM gave us a zero vector (mock or broken), use hash fallback
        # so retrieval still produces meaningful similarity.
        if all(v == 0.0 for v in vec):
            vec = self._hash_embedding(text)
            vec = self._normalize_shape(vec)
        self._cache[key] = vec
        return vec

    def _hash_embedding(self, text: str) -> List[float]:
        # Deterministic pseudo-embedding for offline tests.
        # NOT crypto-grade; only used for cosine sim within a single run.
        out = []
        seed = text.encode("utf-8")
        for i in range(self.dim):
            digest = hashlib.sha1(seed + i.to_bytes(2, "big")).digest()
            out.append((digest[0] - 128) / 128.0)
        return out

    def _normalize_shape(self, vec: List[float]) -> List[float]:
        if not vec:
            return [0.0] * self.dim
        if len(vec) >= self.dim:
            return vec[: self.dim]
        return vec + [0.0] * (self.dim - len(vec))


def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    n = min(len(a), len(b))
    dot = sum(a[i] * b[i] for i in range(n))
    na = sum(a[i] * a[i] for i in range(n)) ** 0.5
    nb = sum(b[i] * b[i] for i in range(n)) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)
