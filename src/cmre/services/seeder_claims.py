"""Seeder for Forensic, Methodological, and HPC Claims.

Ingests claims from:
1. claims_cmre.json (Methodological rules C01-C30)
2. cmre_claims_forensic_catalog.json (Forensic tournament cases FC01-FC14)
3. cmre_hpc_claims.json (High-performance computing claims HPC01-HPC10)

Idempotent and resilient to missing data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import structlog
from sqlmodel import Session, select

from ..models import Claim, Mechanism
from ..schemas import LicenseStatus
from .knowledge_base import upsert_mechanism

log = structlog.get_logger("cmre.services.seeder_claims")

DEFAULT_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "knowledge"


def _infer_modalities(tags: List[str], text: str) -> List[str]:
    """Infers compatible modalities from tags and textual statements."""
    joined = " ".join([t.lower() for t in tags] + [text.lower()])
    mods = set()
    
    if any(k in joined for k in ["dicom", "image", "mammography", "segmentation", "yolox", "convnext", "roi", "patch", "cnn"]):
        mods.add("image")
    if any(k in joined for k in ["tabular", "lightgbm", "xgboost", "catboost", "gbdt", "fraud", "categorical", "features"]):
        mods.add("tabular")
    if any(k in joined for k in ["time-series", "temporal", "walk-forward", "embargo", "trading", "dengue"]):
        mods.add("time_series")
    if any(k in joined for k in ["text", "nlp", "llm", "roberta", "deberta", "arena"]):
        mods.add("text")
    if any(k in joined for k in ["ms/ms", "chemistry", "rna", "protein", "dna", "scaffold", "molecular"]):
        mods.add("molecular")
    if any(k in joined for k in ["bitset", "popcount", "simd", "avx", "dsu", "hpc", "cuda", "beam-search"]):
        mods.add("hpc")

    return sorted(list(mods)) if mods else ["any"]


def _clean_str_or_list(val: Any) -> List[str]:
    """Converts a string or list to a list of strings."""
    if val is None:
        return []
    if isinstance(val, list):
        return [str(item) for item in val if item]
    if isinstance(val, str):
        return [val] if val.strip() else []
    return [str(val)]


def _normalize_dict_field(val: Any, default_key: str = "detail") -> Dict[str, Any]:
    """Normalizes string or dict field to dict."""
    if isinstance(val, dict):
        return val
    if isinstance(val, str) and val.strip():
        return {default_key: val}
    return {}


def load_claims_from_json(file_path: Path) -> List[Dict[str, Any]]:
    """Loads claims array from a JSON file."""
    if not file_path.exists():
        log.warning("Claims JSON file not found", path=str(file_path))
        return []
    try:
        content = json.loads(file_path.read_text(encoding="utf-8"))
        return content.get("claims", [])
    except Exception as e:
        log.error("Failed to read claims JSON", path=str(file_path), error=str(e))
        return []


def seed_forensic_and_hpc_claims(
    session: Session,
    data_dir: Optional[Path | str] = None,
) -> int:
    """Ingests all 54 claims from the knowledge catalogs into the database.
    
    Returns the total number of claims upserted.
    """
    knowledge_dir = Path(data_dir) if data_dir else DEFAULT_KNOWLEDGE_DIR
    log.info("Starting forensic claims seeding", knowledge_dir=str(knowledge_dir))

    json_targets = [
        ("claims_cmre.json", "methodological_rule", "cmre_canonical_catalog"),
        ("cmre_claims_forensic_catalog.json", "forensic_case", "kaggle_forensic_harvest"),
        ("cmre_hpc_claims.json", "hpc_microkernel", "hpc_algorithmia_catalog"),
    ]

    total_upserted = 0

    for filename, claim_type, provenance_type in json_targets:
        file_path = knowledge_dir / filename
        claims_data = load_claims_from_json(file_path)
        log.info("Processing claims file", file=filename, count=len(claims_data))

        for raw in claims_data:
            cid = raw.get("id", "UNKNOWN")
            statement = raw.get("statement", "").strip()
            if not statement:
                continue

            mech_slug = raw.get("mechanism_slug", "general-competitive-ml")
            mech_name = mech_slug.replace("-", " ").replace("_", " ").title()
            
            # Ensure mechanism exists
            upsert_mechanism(
                session=session,
                slug=mech_slug,
                name=mech_name,
                description=f"Mechanism associated with claim {cid} ({mech_name}).",
            )

            tags = _clean_str_or_list(raw.get("tags", []))
            applicable = _clean_str_or_list(raw.get("applicable_when"))
            not_recommended = _clean_str_or_list(raw.get("not_recommended_when"))
            
            modalities = _infer_modalities(tags, statement + " " + " ".join(applicable))

            expected_effect = _normalize_dict_field(raw.get("expected_effect"), default_key="description")
            cost = _normalize_dict_field(raw.get("cost"), default_key="level")
            risk = _normalize_dict_field(raw.get("risk"), default_key="detail")

            evidence_level = int(raw.get("evidence_level", 4))
            license_status = raw.get("license_status", LicenseStatus.allowed.value)

            citations = []
            if raw.get("github_url"):
                citations.append({"type": "github", "url": raw["github_url"]})
            if raw.get("paper_url"):
                citations.append({"type": "paper", "url": raw["paper_url"]})

            summary = f"[{cid}] {mech_name}"

            # Check for existing claim
            existing = session.exec(
                select(Claim).where(Claim.statement == statement)
            ).first()

            if not existing:
                # Also check by summary prefix
                existing = session.exec(
                    select(Claim).where(Claim.summary.like(f"[{cid}]%"))
                ).first()

            if existing:
                # Update metadata and tags
                existing.mechanism_slug = mech_slug
                existing.statement = statement
                existing.summary = summary
                existing.tags = list(set(existing.tags + tags))
                existing.modality_tags = list(set(existing.modality_tags + modalities))
                existing.compatible_modalities = list(set(existing.compatible_modalities + modalities))
                existing.applicable_when = applicable
                existing.not_recommended_when = not_recommended
                existing.expected_effect = expected_effect
                existing.cost = cost
                existing.risk = risk
                existing.evidence_level = evidence_level
                existing.claim_type = claim_type
                existing.provenance_type = provenance_type
                existing.validation_status = "validated"
                existing.approved = True
                existing.citations = citations
                session.add(existing)
            else:
                claim = Claim(
                    mechanism_slug=mech_slug,
                    statement=statement,
                    summary=summary,
                    tags=tags,
                    modality_tags=modalities,
                    compatible_modalities=modalities,
                    applicable_when=applicable,
                    not_recommended_when=not_recommended,
                    expected_effect=expected_effect,
                    cost=cost,
                    risk=risk,
                    evidence_level=evidence_level,
                    license_status=license_status,
                    approved=True,
                    claim_type=claim_type,
                    provenance_type=provenance_type,
                    validation_status="validated",
                    citations=citations,
                )
                session.add(claim)

            total_upserted += 1

    session.commit()
    log.info("Completed forensic claims seeding", total_upserted=total_upserted)
    return total_upserted
