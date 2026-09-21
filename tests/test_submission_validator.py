"""Tests for Universal Submission Integrity Validator (Pre-Submission Gatekeeper).

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import pytest
from cmre.services.submission_validator import (
    SubmissionIntegrityValidator,
    ValidationIssue,
    ValidationReport,
)


@pytest.fixture
def validator() -> SubmissionIntegrityValidator:
    return SubmissionIntegrityValidator()


def test_valid_probability_submission(validator: SubmissionIntegrityValidator) -> None:
    sample_sub = [
        {"prediction_id": "10008_L", "cancer": 0.5},
        {"prediction_id": "10008_R", "cancer": 0.5},
        {"prediction_id": "10011_L", "cancer": 0.5},
    ]
    my_sub = [
        {"prediction_id": "10008_L", "cancer": 0.012},
        {"prediction_id": "10008_R", "cancer": 0.045},
        {"prediction_id": "10011_L", "cancer": 0.003},
    ]
    report = validator.validate(
        df=my_sub,
        sample_df=sample_sub,
        id_col="prediction_id",
        domain_type="probability",
    )
    assert report.is_valid
    assert report.errors_count == 0
    assert len(report.sha256) == 64
    assert report.row_count == 3


def test_nan_and_inf_detection(validator: SubmissionIntegrityValidator) -> None:
    sub_with_nans = [
        {"prediction_id": "1", "target": 0.1},
        {"prediction_id": "2", "target": ""},
        {"prediction_id": "3", "target": 0.5},
    ]
    report = validator.validate(df=sub_with_nans, domain_type="probability")
    assert not report.is_valid
    assert any(i.check == "null_and_nan_check" for i in report.issues)


def test_out_of_bounds_probability(validator: SubmissionIntegrityValidator) -> None:
    sub_out_of_bounds = [
        {"prediction_id": "1", "target": -0.05},
        {"prediction_id": "2", "target": 0.5},
        {"prediction_id": "3", "target": 1.25},
    ]
    report = validator.validate(df=sub_out_of_bounds, domain_type="probability")
    assert not report.is_valid
    assert any(i.check == "range_and_domain_check" for i in report.issues)


def test_disordered_ids_alignment_error(validator: SubmissionIntegrityValidator) -> None:
    test_ref = [
        {"isic_id": "ISIC_001"},
        {"isic_id": "ISIC_002"},
        {"isic_id": "ISIC_003"},
    ]
    # Sub has same IDs but order was scrambled by an unsorted merge
    my_scrambled_sub = [
        {"isic_id": "ISIC_003", "target": 0.1},
        {"isic_id": "ISIC_001", "target": 0.2},
        {"isic_id": "ISIC_002", "target": 0.3},
    ]
    report = validator.validate(
        df=my_scrambled_sub,
        test_df=test_ref,
        id_col="isic_id",
        domain_type="probability",
    )
    assert not report.is_valid
    assert any(i.check == "cardinality_and_alignment_check" for i in report.issues)
    alignment_error = next(i for i in report.issues if i.check == "cardinality_and_alignment_check")
    assert "CRITICAL ALIGNMENT ERROR" in alignment_error.message


def test_discrete_classes_validation(validator: SubmissionIntegrityValidator) -> None:
    # Richter's Predictor allows {1, 2, 3}
    valid_sub = [
        {"building_id": 101, "damage_grade": 1},
        {"building_id": 102, "damage_grade": 2},
        {"building_id": 103, "damage_grade": 3},
    ]
    report = validator.validate(
        df=valid_sub,
        id_col="building_id",
        domain_type="discrete",
        valid_classes=[1, 2, 3],
    )
    assert report.is_valid

    invalid_sub = [
        {"building_id": 101, "damage_grade": 1},
        {"building_id": 102, "damage_grade": 4},  # 4 is invalid
        {"building_id": 103, "damage_grade": 2},
    ]
    report_invalid = validator.validate(
        df=invalid_sub,
        id_col="building_id",
        domain_type="discrete",
        valid_classes=[1, 2, 3],
    )
    assert not report_invalid.is_valid
    assert any(i.check == "range_and_domain_check" for i in report_invalid.issues)


def test_continuous_nonneg_validation(validator: SubmissionIntegrityValidator) -> None:
    valid_airqo = [
        {"ID": "A1", "target": 42.5},
        {"ID": "A2", "target": 0.0},
    ]
    report = validator.validate(
        df=valid_airqo,
        id_col="ID",
        domain_type="continuous_nonneg",
    )
    assert report.is_valid

    invalid_airqo = [
        {"ID": "A1", "target": 42.5},
        {"ID": "A2", "target": -5.2},
    ]
    report_invalid = validator.validate(
        df=invalid_airqo,
        id_col="ID",
        domain_type="continuous_nonneg",
    )
    assert not report_invalid.is_valid


def test_ranking_validation(validator: SubmissionIntegrityValidator) -> None:
    valid_casmi = [
        {"molecular_id": "M1", "rank": 1, "score": 0.9},
        {"molecular_id": "M1", "rank": 2, "score": 0.5},
        {"molecular_id": "M2", "rank": 1, "score": 0.8},
        {"molecular_id": "M2", "rank": 2, "score": 0.7},
    ]
    report = validator.validate(
        df=valid_casmi,
        id_col="molecular_id",
        domain_type="ranking",
        top_k_ranking=2,
    )
    assert report.is_valid


def test_schema_column_mismatch(validator: SubmissionIntegrityValidator) -> None:
    expected_cols = ["prediction_id", "cancer"]
    bad_cols_sub = [
        {"id": "10008_L", "prob": 0.05}
    ]
    report = validator.validate(
        df=bad_cols_sub,
        expected_columns=expected_cols,
    )
    assert not report.is_valid
    assert any(i.check == "schema_check" for i in report.issues)
