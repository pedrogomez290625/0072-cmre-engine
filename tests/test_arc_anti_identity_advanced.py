"""Unit tests for Advanced Anti-Identity Guard (CMRE-15).

Tests the AntiIdentityGuard and its integration in validate_arc_json.
Autor: Perez, Ernesto Rafael ("Rafa")
"""

import pytest
from cmre.services.submission_validator import SubmissionIntegrityValidator, AntiIdentityGuard

def test_calculate_similarity():
    grid1 = [[1, 2], [3, 4]]
    grid2 = [[1, 2], [3, 4]]
    assert AntiIdentityGuard.calculate_similarity(grid1, grid2) == 1.0

    grid3 = [[1, 2], [9, 4]]
    assert AntiIdentityGuard.calculate_similarity(grid1, grid3) == 0.75

    grid_diff_size = [[1, 2, 3], [4, 5, 6]]
    assert AntiIdentityGuard.calculate_similarity(grid1, grid_diff_size) == 0.0

def test_apply_d8_transform():
    grid = [[1, 2, 3], [4, 5, 6]]
    expected = [[1, 4], [2, 5], [3, 6]]
    assert AntiIdentityGuard.apply_d8_transform(grid) == expected

def test_apply_chromatic_shift():
    grid = [[0, 1, 9], [2, 0, 8]]
    expected = [[0, 2, 1], [3, 0, 9]]
    assert AntiIdentityGuard.apply_chromatic_shift(grid) == expected

def test_enforce():
    grid = [[1, 2], [3, 4]]
    # Since similarity is 1.0 (>= 0.99), it should apply D8 then Chromatic
    # D8: [[1, 3], [2, 4]]
    # Chromatic: [[2, 4], [3, 5]]
    expected = [[4, 2], [5, 3]]
    assert AntiIdentityGuard.enforce(grid, grid) == expected

    grid_diff = [[9, 9], [9, 9]]
    # Similarity is 0.0, so should return original grid
    assert AntiIdentityGuard.enforce(grid_diff, grid) == grid_diff

def test_validate_arc_json_autofix_warning():
    validator = SubmissionIntegrityValidator()
    input_grid = [[1, 2], [3, 4]]
    sub_data = {
        "task_001": {
            "attempt_1": input_grid, # Identical, should be fixed
            "attempt_2": [[9, 9], [9, 9]]
        }
    }
    ref_tasks = {
        "task_001": {"test": [{"input": input_grid}]}
    }

    report = validator.validate_arc_json(sub_data, reference_tasks=ref_tasks, auto_fix=True)

    # Autofix should turn the ERROR into a WARNING, so it is valid
    assert report.is_valid is True
    assert report.errors_count == 0
    assert report.warnings_count >= 1
    checks = [i.check for i in report.issues]
    assert "anti_identity_collapse_fixed" in checks

    # Check if dict was updated
    assert sub_data["task_001"]["attempt_1"] == [[4, 2], [5, 3]]

def test_validate_arc_json_no_autofix_error():
    validator = SubmissionIntegrityValidator()
    input_grid = [[1, 2], [3, 4]]
    sub_data = {
        "task_001": {
            "attempt_1": input_grid, # Identical, should error
            "attempt_2": [[9, 9], [9, 9]]
        }
    }
    ref_tasks = {
        "task_001": {"test": [{"input": input_grid}]}
    }

    report = validator.validate_arc_json(sub_data, reference_tasks=ref_tasks, auto_fix=False)

    assert report.is_valid is False
    assert report.errors_count >= 1
    checks = [i.check for i in report.issues]
    assert "anti_identity_collapse" in checks
