"""Unit tests for ARC JSON and Multi-label Submission Validation.

Tests validate_arc_json, Anti-Identity violation detection (FAIL_11),
and validate_multilabel_schema (e.g. RSNA Knee 12-class).

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import json
import pytest
from cmre.services.submission_validator import SubmissionIntegrityValidator


def test_validate_arc_json_valid():
    validator = SubmissionIntegrityValidator()

    sub_data = {
        "task_001": {
            "attempt_1": [[1, 2], [3, 4]],
            "attempt_2": [[4, 3], [2, 1]],
        },
        "task_002": [
            {
                "attempt_1": [[0, 5], [5, 0]],
                "attempt_2": [[5, 0], [0, 5]],
            }
        ],
    }

    ref_tasks = {
        "task_001": {"test": [{"input": [[0, 0], [0, 0]]}]},
        "task_002": {"test": [{"input": [[9, 9], [9, 9]]}]},
    }

    report = validator.validate_arc_json(sub_data, reference_tasks=ref_tasks)

    assert report.is_valid is True
    assert report.errors_count == 0
    assert report.row_count == 2
    assert len(report.sha256) == 64


def test_validate_arc_json_anti_identity_violation():
    validator = SubmissionIntegrityValidator()

    input_grid = [[1, 2], [3, 4]]
    # Submission returns identical input grid (FAIL_11)
    sub_data = {
        "task_001": {
            "attempt_1": input_grid,
            "attempt_2": [[9, 9], [9, 9]],
        }
    }

    ref_tasks = {
        "task_001": {"test": [{"input": input_grid}]}
    }

    report = validator.validate_arc_json(sub_data, reference_tasks=ref_tasks)

    assert report.is_valid is False
    assert report.errors_count >= 1
    checks = [i.check for i in report.issues]
    assert "anti_identity_collapse" in checks


def test_validate_multilabel_schema_rsna_knee():
    validator = SubmissionIntegrityValidator()

    from cmre.solvers.rsna_knee_solver import KNEE_ABNORMALITIES_12

    # Valid table dictionary
    table = {
        "study_id": ["S001", "S002"],
    }
    for col in KNEE_ABNORMALITIES_12:
        table[col] = [0.12, 0.85]

    report = validator.validate_multilabel_schema(
        df=table,
        id_col="study_id",
        expected_target_cols=KNEE_ABNORMALITIES_12,
        expected_rows=2,
    )

    assert report.is_valid is True
    assert report.errors_count == 0
    assert report.column_count == 13
