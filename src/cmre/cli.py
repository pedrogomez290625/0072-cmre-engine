"""Typer CLI for CMRE."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
import yaml
from rich.console import Console
from sqlmodel import Session

from .agents.base import MockLLMClient, get_llm_client
from .config import get_settings
from .db import engine, init_db
from .services.knowledge_base import approve_claim, reject_claim
from .services.planner import generate_plan
from .services.problem_profiler import build_dna
from .services.reasoner import retrieve_and_rank
from .services.reporter import render_markdown
from .services.seeder_multimodal import seed as run_seed

app = typer.Typer(add_completion=False, help="CMRE: competition-agnostic reasoning engine.")
console = Console()


@app.command("init-db")
def cmd_init_db() -> None:
    """Initialize the database (Postgres + pgvector)."""
    init_db()
    console.print("[green]Database initialized.[/green]")


@app.command("seed")
def cmd_seed() -> None:
    """Seed the multi-modal knowledge base and forensic claims (idempotent)."""
    from .services.seeder_claims import seed_forensic_and_hpc_claims

    init_db()
    with Session(engine) as session:
        n_seed = run_seed(session)
        n_forensic = seed_forensic_and_hpc_claims(session)
    console.print(f"[green]Seed complete. Inserted {n_seed} multimodal seeds and {n_forensic} forensic/HPC claims.[/green]")


@app.command("report")
def cmd_report(
    input: str = typer.Option(..., "--input", "-i", help="Path to a CompetitionInput JSON."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Where to write the markdown report."),
    use_llm: bool = typer.Option(False, "--use-llm", help="Enable LLM enrichment of DNA and claim re-ranking."),
    allow_unknown_license: bool = typer.Option(False, help="Allow claims with unknown license."),
) -> None:
    """Generate a full competition report from a JSON input."""
    init_db()
    data = json.loads(Path(input).read_text(encoding="utf-8"))
    from .schemas import CompetitionInput

    inp = CompetitionInput.model_validate(data)
    settings = get_settings()

    llm = get_llm_client(settings) if use_llm else MockLLMClient()
    dna = build_dna(inp, llm=llm if use_llm else None)

    with Session(engine) as session:
        ranked = retrieve_and_rank(
            session,
            dna,
            llm=llm,
            limit=settings.max_claims_per_report,
            allow_unknown_license=allow_unknown_license,
        )
    plan = generate_plan(dna, ranked, max_techniques=min(10, len(ranked)))
    md = render_markdown(dna, plan, ranked)

    if output:
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        console.print(f"[green]Report saved to {output}[/green]")
    else:
        console.print(md)


@app.command("approve-claim")
def cmd_approve(claim_id: int = typer.Argument(..., help="Claim ID to approve.")) -> None:
    init_db()
    with Session(engine) as session:
        approve_claim(session, claim_id)
    console.print(f"[green]Claim {claim_id} approved.[/green]")


@app.command("reject-claim")
def cmd_reject(
    claim_id: int = typer.Argument(..., help="Claim ID to reject."),
    note: str = typer.Option("", help="Rejection note."),
) -> None:
    init_db()
    with Session(engine) as session:
        reject_claim(session, claim_id, note=note)
    console.print(f"[yellow]Claim {claim_id} rejected.[/yellow]")


@app.command("jules-sync")
def cmd_jules_sync(
    tasks_file: str = typer.Option(".jules/tasks.yaml", help="Path to tasks YAML."),
    outbox_file: str = typer.Option(".jules/outbox.jsonl", help="Outbox file path."),
    repo: Optional[str] = typer.Option(None, help="Source repo (defaults to CMRE_GITHUB_REPO)."),
) -> None:
    """Dispatch tasks from YAML to Jules cloud agent (requires API key)."""
    from .agents.jules_outbox import dispatch_from_yaml

    settings = get_settings()
    repo = repo or settings.github_repo
    records = dispatch_from_yaml(tasks_file, outbox_file, repo, settings)
    console.print(f"[green]Dispatched {len(records)} tasks. See {outbox_file}.[/green]")


@app.command("ingest")
def cmd_ingest(
    query: str = typer.Option(..., help="Research query."),
    platforms: str = typer.Option("huggingface,semantic_scholar,arxiv,github", help="Comma-separated."),
    limit: int = typer.Option(15, help="Max artifacts per connector."),
) -> None:
    """Discover public artifacts across connectors and persist them."""
    from .connectors import get_connectors
    from .services.knowledge_base import upsert_artifact

    init_db()
    platform_set = {p.strip() for p in platforms.split(",") if p.strip()}
    connectors = [c for c in get_connectors() if c.name in platform_set]
    total = 0
    with Session(engine) as session:
        for c in connectors:
            candidates = c.discover(query, limit=limit)
            for cand in candidates:
                upsert_artifact(session, cand)
                total += 1
    console.print(f"[green]Imported {total} candidates.[/green]")


@app.command("version")
def cmd_version() -> None:
    """Show CMRE version."""
    s = get_settings()
    console.print(f"CMRE v{s.version}")


@app.command("evaluate-golden")
def cmd_evaluate_golden(
    golden_dir: str = typer.Option("data/golden_cases", help="Directory of golden case JSONs."),
    case: Optional[str] = typer.Option(None, help="Run a single case by id."),
) -> None:
    """Evaluate CMRE against golden cases (deterministic, no LLM)."""
    import subprocess
    import sys
    cmd = [sys.executable, "scripts/evaluate_golden.py", "--golden-dir", golden_dir]
    if case:
        cmd.extend(["--case", case])
    raise SystemExit(subprocess.call(cmd, cwd="."))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
