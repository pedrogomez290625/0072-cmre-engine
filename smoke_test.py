"""End-to-end smoke test that runs the full pipeline with SQLite (no Postgres required)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

# Use a temp file SQLite DB so we can also run the system end-to-end.
os.environ.setdefault("CMRE_DATABASE_URL", "sqlite:///:memory:")

from sqlmodel import Session, SQLModel, create_engine

# Build an isolated SQLite engine before cmre.config touches anything.
engine = create_engine("sqlite:///:memory:")
SQLModel.metadata.create_all(engine)

import cmre.db as db
db.engine = engine

from cmre.services.seeder_multimodal import seed
from cmre.services.problem_profiler import build_dna
from cmre.services.reasoner import retrieve_and_rank
from cmre.services.planner import generate_plan
from cmre.services.reporter import render_markdown
from cmre.agents.base import MockLLMClient
from cmre.schemas import CompetitionInput


def main():
    # Re-create tables on our engine to ensure claims table exists.
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        n = seed(session)
        print(f"[seed] inserted {n} claims")

    examples = sorted(Path("data/examples").glob("competition_*.json"))
    print(f"[examples] found {len(examples)}")

    llm = MockLLMClient()
    out_dir = Path("reports")
    out_dir.mkdir(exist_ok=True)

    for fp in examples:
        data = json.loads(fp.read_text(encoding="utf-8"))
        ci = CompetitionInput.model_validate(data)
        dna = build_dna(ci, llm=None)
        with Session(engine) as session:
            ranked = retrieve_and_rank(session, dna, llm=llm, limit=8, allow_unknown_license=False)
        plan = generate_plan(dna, ranked)
        md = render_markdown(dna, plan, ranked)
        target = out_dir / (fp.stem + ".md")
        target.write_text(md, encoding="utf-8")
        print(f"[report] {fp.stem:50s} -> {target.name} ({len(md)} chars, {len(ranked)} ranked claims)")

    print("\n[done] all examples processed.")


if __name__ == "__main__":
    main()
