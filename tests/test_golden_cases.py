"""Tests for the golden-case evaluator.

Smoke test: confirms the script runs end-to-end against the 3 golden cases
shipped in data/golden_cases/ and reports metrics.
"""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_evaluate_golden_script_runs():
    proc = subprocess.run(
        [sys.executable, "scripts/evaluate_golden.py"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, f"stderr: {proc.stderr}"
    assert "case:" in proc.stdout
    assert "aggregate" in proc.stdout
    # At least 3 cases
    assert proc.stdout.count("case:") >= 3


def test_evaluate_golden_single_case():
    proc = subprocess.run(
        [sys.executable, "scripts/evaluate_golden.py", "--case", "fraud_temporal_leak_001"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, f"stderr: {proc.stderr}"
    assert "fraud_temporal_leak_001" in proc.stdout


def test_all_golden_cases_are_valid_json():
    golden_dir = ROOT / "data" / "golden_cases"
    files = list(golden_dir.glob("*.json"))
    assert len(files) >= 3
    for fp in files:
        data = json.loads(fp.read_text(encoding="utf-8"))
        assert "case_id" in data
        assert "competition_input" in data
        assert "expected_dna_flags" in data
        assert "known_outcome" in data
