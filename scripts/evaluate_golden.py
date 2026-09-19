"""Evaluate CMRE against a set of golden cases.

For each case in data/golden_cases/, run the full reasoning pipeline against
the embedded competition_input, then compare the resulting DNA + ranked
claims against the expected assertions. Prints a metrics summary.

Usage:
    python scripts/evaluate_golden.py
    python scripts/evaluate_golden.py --case fraud_temporal_leak_001
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List

# Override DB URL BEFORE importing cmre (it reads settings on import).
os.environ["CMRE_DATABASE_URL"] = "sqlite:///:memory:"

# Ensure we can import cmre from src/.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sqlmodel import Session, SQLModel, create_engine

# Import cmre.models FIRST so metadata is populated, THEN create_all.
from cmre.agents.base import MockLLMClient
from cmre.models import Claim
from cmre.schemas import CompetitionInput, GoldenCase
from cmre.services.problem_profiler import build_dna
from cmre.services.reasoner import rank_claims
from cmre.services.seeder_multimodal import seed

# Use SQLite in-memory for portability.
engine = create_engine("sqlite:///:memory:")
SQLModel.metadata.create_all(engine)

import cmre.db as cmre_db
cmre_db.engine = engine

from sqlmodel import select


def load_golden_cases(golden_dir: Path) -> list[GoldenCase]:
    cases: list[GoldenCase] = []
    for fp in sorted(golden_dir.glob("*.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        cases.append(GoldenCase.model_validate(data))
    return cases


def _normalize(s: str) -> str:
    return (s or "").lower().replace("-", "_").replace(" ", "_")


def _overlap(predicted: list[str], expected: list[str]) -> tuple[int, int, int]:
    """Return (true_positives, predicted_count, expected_count) using substring matching."""
    pred_norm = [_normalize(p) for p in predicted]
    exp_norm = [_normalize(e) for e in expected]
    tp = 0
    for e in exp_norm:
        for p in pred_norm:
            if e and (e in p or p in e):
                tp += 1
                break
    return tp, len(pred_norm), len(exp_norm)


def _safe_ratio(num: int, denom: int) -> float:
    return round(num / denom, 4) if denom > 0 else 0.0


def evaluate_case(case: GoldenCase, session: Session) -> dict:
    inp = CompetitionInput.model_validate(case.competition_input)
    dna = build_dna(inp, llm=None)
    ranked = rank_claims(session.exec(select(Claim)).all(), dna, llm=MockLLMClient())

    # Risk-flag recall: how many expected flags were detected?
    flag_tp, flag_pred_n, flag_exp_n = _overlap(dna.risk_flags, case.expected_dna_flags)

    # Validation recommendations accuracy: how many expected validation
    # recommendations did the system surface?
    val_tp, _, val_exp_n = _overlap(dna.validation_recommendations, case.expected_validation_recommendations)

    # Anti-pattern detection rate: how many expected anti-patterns were flagged?
    ap_tp, _, ap_exp_n = _overlap(dna.anti_patterns, case.expected_anti_patterns)

    # Mechanism precision@10: how many expected top-mechanisms appear in top-10?
    top10_mechanisms = [rc.mechanism_slug for rc in ranked[:10] if rc.mechanism_slug]
    mech_tp, _, mech_exp_n = _overlap(top10_mechanisms, case.expected_top_mechanisms)

    # Forbidden recommendations: any of them in top-K? (lower is better)
    forbidden_hits: list[str] = []
    for forbidden in case.forbidden_recommendations:
        f_norm = _normalize(forbidden)
        for rc in ranked[:10]:
            if f_norm and f_norm in _normalize(rc.statement):
                forbidden_hits.append(rc.statement)
                break

    return {
        "case_id": case.case_id,
        "risk_flag_recall": _safe_ratio(flag_tp, flag_exp_n),
        "validation_recall": _safe_ratio(val_tp, val_exp_n),
        "anti_pattern_recall": _safe_ratio(ap_tp, ap_exp_n),
        "mechanism_precision_at_10": _safe_ratio(mech_tp, mech_exp_n),
        "forbidden_hits": forbidden_hits,
        "expected_outcome": case.known_outcome,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden-dir", default=str(ROOT / "data" / "golden_cases"))
    parser.add_argument("--case", default=None, help="Run only this case id.")
    args = parser.parse_args()

    # Seed once.
    with Session(engine) as session:
        seed(session)

    cases = load_golden_cases(Path(args.golden_dir))
    if args.case:
        cases = [c for c in cases if c.case_id == args.case]
        if not cases:
            print(f"No case with id={args.case} in {args.golden_dir}")
            sys.exit(1)

    results: list[dict] = []
    with Session(engine) as session:
        for case in cases:
            r = evaluate_case(case, session)
            results.append(r)

    # Print per-case
    for r in results:
        print("\n---")
        print(f"case: {r['case_id']}")
        print(f"  risk_flag_recall:      {r['risk_flag_recall']:.2f}")
        print(f"  validation_recall:     {r['validation_recall']:.2f}")
        print(f"  anti_pattern_recall:   {r['anti_pattern_recall']:.2f}")
        print(f"  mechanism_p@10:        {r['mechanism_precision_at_10']:.2f}")
        if r["forbidden_hits"]:
            print(f"  FORBIDDEN HITS: {r['forbidden_hits']}")
        if r["expected_outcome"]:
            print(f"  outcome: {r['expected_outcome']}")

    # Aggregate
    if len(results) > 1:
        avg = lambda k: round(sum(r[k] for r in results) / len(results), 4)
        print("\n=== aggregate ===")
        print(f"  avg risk_flag_recall:    {avg('risk_flag_recall')}")
        print(f"  avg validation_recall:   {avg('validation_recall')}")
        print(f"  avg anti_pattern_recall: {avg('anti_pattern_recall')}")
        print(f"  avg mechanism_p@10:      {avg('mechanism_precision_at_10')}")
        total_forbidden = sum(len(r["forbidden_hits"]) for r in results)
        print(f"  total forbidden hits:    {total_forbidden}")


if __name__ == "__main__":
    main()
