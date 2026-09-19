"""Smoke tests for the schema validation across modalities."""

import json
from pathlib import Path

from cmre.schemas import CompetitionInput, ProblemDNA


DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "examples"


def test_all_example_files_are_valid_competitioninput():
    files = sorted(DATA_DIR.glob("competition_*.json"))
    assert len(files) >= 5, f"expected >= 5 example files, got {len(files)}"
    for fp in files:
        data = json.loads(fp.read_text(encoding="utf-8"))
        ci = CompetitionInput.model_validate(data)
        assert ci.title
        assert ci.modality in {"tabular", "text", "image", "video", "audio", "time_series", "graph", "multimodal"}
        assert ci.task_type
        assert ci.metric


def test_problem_dna_construction_from_each_example():
    from cmre.services.problem_profiler import build_dna

    for fp in sorted(DATA_DIR.glob("competition_*.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        ci = CompetitionInput.model_validate(data)
        dna = build_dna(ci)
        assert isinstance(dna, ProblemDNA)
        assert dna.modality == ci.modality or dna.modality == "tabular"  # fallback only for invalid
