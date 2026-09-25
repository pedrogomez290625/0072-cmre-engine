"""Universal Submission Integrity Validator (Pre-Submission Gatekeeper).

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
Fecha: Septiembre de 2026
Ecosistema: 0072-cmre-engine

Universal validator verifying prediction submission files against platform schemas,
preventing silent zero-scores, null leaks, ID misalignments, and out-of-domain predictions.
Works seamlessly with pure Python standard library (csv) and numpy, with optional pandas support.
"""

from __future__ import annotations

import csv
import hashlib
import io
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

import numpy as np

try:
    import pandas as pd
except ImportError:
    pd = None


@dataclass
class ValidationIssue:
    """Represents a finding or violation during submission auditing."""

    level: str  # "ERROR", "WARNING", "INFO"
    check: str
    message: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class ValidationReport:
    """Comprehensive submission audit report."""

    is_valid: bool
    sha256: str
    row_count: int
    column_count: int
    issues: List[ValidationIssue] = field(default_factory=list)
    errors_count: int = 0
    warnings_count: int = 0

    @property
    def summary(self) -> str:
        status_icon = "PASS" if self.is_valid else "FAIL"
        lines = [
            f"[{status_icon}] Submission Audit Result: {self.errors_count} errors, {self.warnings_count} warnings.",
            f"  • SHA-256 Fingerprint: {self.sha256}",
            f"  • Shape: {self.row_count} rows x {self.column_count} columns",
        ]
        if self.issues:
            lines.append("  • Issues:")
            for issue in self.issues:
                prefix = f"    [{issue.level}] {issue.check}: {issue.message}"
                lines.append(prefix)
        return "\n".join(lines)


class SubmissionIntegrityValidator:
    """Pre-submission gatekeeper auditing format, bounds, cardinality and alignment."""

    def __init__(self, tolerance: float = 1e-6) -> None:
        self.tolerance = tolerance

    @staticmethod
    def compute_sha256_bytes(content: bytes) -> str:
        """Compute SHA-256 checksum from bytes."""
        hasher = hashlib.sha256()
        hasher.update(content)
        return hasher.hexdigest()

    @staticmethod
    def compute_sha256_file(filepath: Union[str, Path]) -> str:
        """Compute SHA-256 checksum from a file path."""
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    @classmethod
    def _read_table(cls, obj: Any) -> tuple[List[str], List[Dict[str, Any]], bytes]:
        """Convert various table inputs (DataFrame, path, csv string, list of dicts) to canonical records."""
        if pd is not None and isinstance(obj, pd.DataFrame):
            cols = list(obj.columns)
            records = obj.to_dict(orient="records")
            csv_buf = io.StringIO()
            obj.to_csv(csv_buf, index=False)
            raw_bytes = csv_buf.getvalue().encode("utf-8")
            return cols, records, raw_bytes

        if isinstance(obj, (str, Path)):
            p = Path(obj)
            if p.is_file():
                raw_bytes = p.read_bytes()
                text = raw_bytes.decode("utf-8")
                reader = csv.DictReader(io.StringIO(text))
                cols = reader.fieldnames or []
                records = list(reader)
                return list(cols), records, raw_bytes
            else:
                # Interpret as raw CSV text
                raw_bytes = obj.encode("utf-8")
                reader = csv.DictReader(io.StringIO(obj))
                cols = reader.fieldnames or []
                records = list(reader)
                return list(cols), records, raw_bytes

        if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], dict):
            cols = list(obj[0].keys())
            buf = io.StringIO()
            writer = csv.DictWriter(buf, fieldnames=cols)
            writer.writeheader()
            writer.writerows(obj)
            raw_bytes = buf.getvalue().encode("utf-8")
            return cols, obj, raw_bytes

        if isinstance(obj, dict) and all(isinstance(v, list) for v in obj.values()):
            cols = list(obj.keys())
            n = len(next(iter(obj.values())))
            records = [{col: obj[col][i] for col in cols} for i in range(n)]
            buf = io.StringIO()
            writer = csv.DictWriter(buf, fieldnames=cols)
            writer.writeheader()
            writer.writerows(records)
            raw_bytes = buf.getvalue().encode("utf-8")
            return cols, records, raw_bytes

        return [], [], b""

    def validate(
        self,
        df: Any,
        sample_df: Optional[Any] = None,
        test_df: Optional[Any] = None,
        id_col: Optional[str] = None,
        target_cols: Optional[List[str]] = None,
        domain_type: str = "probability",
        valid_classes: Optional[Sequence[Any]] = None,
        expected_columns: Optional[List[str]] = None,
        expected_rows: Optional[int] = None,
        top_k_ranking: Optional[int] = None,
    ) -> ValidationReport:
        """Validate a submission against platform requirements and reference datasets."""
        issues: List[ValidationIssue] = []

        sub_cols, sub_records, sub_bytes = self._read_table(df)

        # 0. Check empty DataFrame / table
        if not sub_records:
            issues.append(
                ValidationIssue(
                    level="ERROR",
                    check="empty_dataframe",
                    message="The submission table is empty (0 rows).",
                )
            )
            return ValidationReport(
                is_valid=False,
                sha256="0" * 64,
                row_count=0,
                column_count=len(sub_cols),
                issues=issues,
                errors_count=1,
                warnings_count=0,
            )

        sha256 = self.compute_sha256_bytes(sub_bytes)

        # 1. Schema Check: Columns and positional order
        ref_cols: Optional[List[str]] = None
        sample_records: List[Dict[str, Any]] = []
        if sample_df is not None:
            ref_cols, sample_records, _ = self._read_table(sample_df)
        elif expected_columns is not None:
            ref_cols = list(expected_columns)

        if ref_cols is not None:
            if sub_cols != ref_cols:
                missing = [c for c in ref_cols if c not in sub_cols]
                extra = [c for c in sub_cols if c not in ref_cols]
                if missing or extra:
                    issues.append(
                        ValidationIssue(
                            level="ERROR",
                            check="schema_check",
                            message=f"Column mismatch. Missing: {missing}, Unexpected: {extra}.",
                            details={"expected": ref_cols, "actual": sub_cols},
                        )
                    )
                else:
                    issues.append(
                        ValidationIssue(
                            level="ERROR",
                            check="schema_check",
                            message=f"Column order mismatch. Expected {ref_cols}, got {sub_cols}.",
                        )
                    )

        # Determine id_col and target_cols if not explicitly supplied
        inferred_id = id_col
        if inferred_id is None and len(sub_cols) >= 2:
            inferred_id = sub_cols[0]

        inferred_targets = target_cols
        if inferred_targets is None:
            if inferred_id is not None and inferred_id in sub_cols:
                inferred_targets = [c for c in sub_cols if c != inferred_id]
            else:
                inferred_targets = list(sub_cols[1:]) if len(sub_cols) > 1 else list(sub_cols)

        # 2. Null, NaN and Inf Check
        null_counts: Dict[str, int] = {c: 0 for c in sub_cols}
        inf_counts: Dict[str, int] = {c: 0 for c in sub_cols}

        for row in sub_records:
            for c in sub_cols:
                val = row.get(c)
                if val is None or val == "" or (isinstance(val, float) and math.isnan(val)):
                    null_counts[c] += 1
                elif isinstance(val, (int, float)) and math.isinf(val):
                    inf_counts[c] += 1
                elif isinstance(val, str) and val.strip().lower() in ("nan", "null", "none", ""):
                    null_counts[c] += 1
                elif isinstance(val, str) and val.strip().lower() in ("inf", "-inf", "+inf"):
                    inf_counts[c] += 1

        bad_nulls = {k: v for k, v in null_counts.items() if v > 0}
        if bad_nulls:
            issues.append(
                ValidationIssue(
                    level="ERROR",
                    check="null_and_nan_check",
                    message=f"NaN/Null values detected in columns: {bad_nulls}.",
                    details=bad_nulls,
                )
            )

        bad_infs = {k: v for k, v in inf_counts.items() if v > 0}
        if bad_infs:
            issues.append(
                ValidationIssue(
                    level="ERROR",
                    check="null_and_nan_check",
                    message=f"Infinite values (+/-inf) detected: {bad_infs}.",
                    details=bad_infs,
                )
            )

        # 3. Cardinality and Positional Alignment Check
        target_rows = expected_rows
        test_cols: List[str] = []
        test_records: List[Dict[str, Any]] = []
        if test_df is not None:
            test_cols, test_records, _ = self._read_table(test_df)

        if target_rows is None:
            if sample_records:
                target_rows = len(sample_records)
            elif test_records:
                if domain_type == "ranking" and top_k_ranking is not None:
                    target_rows = len(test_records) * top_k_ranking
                else:
                    target_rows = len(test_records)

        if target_rows is not None and len(sub_records) != target_rows:
            issues.append(
                ValidationIssue(
                    level="ERROR",
                    check="cardinality_check",
                    message=f"Row count mismatch. Expected {target_rows}, found {len(sub_records)}.",
                    details={"expected": target_rows, "actual": len(sub_records)},
                )
            )

        # Positional alignment of IDs
        ref_records = sample_records if sample_records else test_records
        if ref_records and inferred_id and inferred_id in sub_cols:
            if domain_type != "ranking":
                sub_ids = [str(r.get(inferred_id)) for r in sub_records]
                ref_ids = [str(r.get(inferred_id)) for r in ref_records]

                if len(sub_ids) == len(ref_ids):
                    mismatches = sum(1 for s, r in zip(sub_ids, ref_ids) if s != r)
                    if mismatches > 0:
                        issues.append(
                            ValidationIssue(
                                level="ERROR",
                                check="cardinality_and_alignment_check",
                                message=(
                                    f"CRITICAL ALIGNMENT ERROR: {mismatches} IDs differ in positional order from the reference set. "
                                    "A merge/join altered the row order without sorting!"
                                ),
                                details={"mismatched_positions": mismatches},
                            )
                        )
                else:
                    sub_set = set(sub_ids)
                    ref_set = set(ref_ids)
                    diff_missing = ref_set - sub_set
                    diff_extra = sub_set - ref_set
                    if diff_missing or diff_extra:
                        issues.append(
                            ValidationIssue(
                                level="ERROR",
                                check="cardinality_and_alignment_check",
                                message=f"ID set discrepancy. Missing IDs: {len(diff_missing)}, Extra IDs: {len(diff_extra)}.",
                            )
                        )

        # 4. Domain and Value Range Checks
        for col in inferred_targets:
            if col not in sub_cols:
                continue

            raw_vals = [r.get(col) for r in sub_records]

            if domain_type == "probability":
                numeric_vals = []
                non_num_count = 0
                for v in raw_vals:
                    try:
                        numeric_vals.append(float(v))
                    except (ValueError, TypeError):
                        non_num_count += 1

                if non_num_count > 0:
                    issues.append(
                        ValidationIssue(
                            level="ERROR",
                            check="range_and_domain_check",
                            message=f"Probability column '{col}' has {non_num_count} non-numeric values.",
                        )
                    )
                elif numeric_vals:
                    arr = np.array(numeric_vals, dtype=np.float64)
                    min_val = float(np.min(arr))
                    max_val = float(np.max(arr))
                    if min_val < 0.0 - self.tolerance or max_val > 1.0 + self.tolerance:
                        issues.append(
                            ValidationIssue(
                                level="ERROR",
                                check="range_and_domain_check",
                                message=f"Probability column '{col}' values outside [0, 1]. Min: {min_val:.5f}, Max: {max_val:.5f}.",
                            )
                        )
                    if len(arr) > 10 and float(np.std(arr)) < 1e-7:
                        issues.append(
                            ValidationIssue(
                                level="WARNING",
                                check="variance_collapse",
                                message=f"Column '{col}' has near-zero standard deviation ({float(np.std(arr)):.2e}). Predictions may have collapsed.",
                            )
                        )

            elif domain_type == "discrete":
                if valid_classes is not None:
                    allowed_set = {str(c) for c in valid_classes}
                    actual_set = {str(v) for v in raw_vals if v is not None and v != ""}
                    unauthorized = actual_set - allowed_set
                    if unauthorized:
                        issues.append(
                            ValidationIssue(
                                level="ERROR",
                                check="range_and_domain_check",
                                message=f"Discrete column '{col}' contains invalid classes: {sorted(list(unauthorized))}. Allowed: {sorted(list(allowed_set))}.",
                            )
                        )
                else:
                    issues.append(
                        ValidationIssue(
                            level="WARNING",
                            check="discrete_classes_unspecified",
                            message=f"Domain type is 'discrete' but valid_classes was not provided for column '{col}'.",
                        )
                    )

            elif domain_type == "continuous_nonneg":
                numeric_vals = []
                non_num_count = 0
                for v in raw_vals:
                    try:
                        numeric_vals.append(float(v))
                    except (ValueError, TypeError):
                        non_num_count += 1

                if non_num_count > 0:
                    issues.append(
                        ValidationIssue(
                            level="ERROR",
                            check="range_and_domain_check",
                            message=f"Continuous non-negative column '{col}' has {non_num_count} non-numeric values.",
                        )
                    )
                elif numeric_vals:
                    arr = np.array(numeric_vals, dtype=np.float64)
                    min_val = float(np.min(arr))
                    if min_val < 0.0 - self.tolerance:
                        issues.append(
                            ValidationIssue(
                                level="ERROR",
                                check="range_and_domain_check",
                                message=f"Continuous non-negative column '{col}' has negative values. Min: {min_val:.5f}.",
                            )
                        )

        # 5. Ranking checks (e.g. CASMI top-10)
        if domain_type == "ranking" and "rank" in sub_cols and inferred_id and inferred_id in sub_cols:
            groups: Dict[str, List[Dict[str, Any]]] = {}
            for r in sub_records:
                gid = str(r.get(inferred_id))
                groups.setdefault(gid, []).append(r)

            for gid, grp in groups.items():
                ranks = [int(x.get("rank")) for x in grp if str(x.get("rank", "")).isdigit()]
                expected_ranks = list(range(1, len(grp) + 1))
                if ranks != expected_ranks:
                    issues.append(
                        ValidationIssue(
                            level="ERROR",
                            check="ranking_integrity",
                            message=f"Ranks for group '{gid}' are not sequentially ordered 1..{len(grp)}: {ranks[:5]}.",
                        )
                    )
                    break

        errors_count = sum(1 for i in issues if i.level == "ERROR")
        warnings_count = sum(1 for i in issues if i.level == "WARNING")
        is_valid = errors_count == 0

        return ValidationReport(
            is_valid=is_valid,
            sha256=sha256,
            row_count=len(sub_records),
            column_count=len(sub_cols),
            issues=issues,
            errors_count=errors_count,
            warnings_count=warnings_count,
        )

    def validate_file(
        self,
        submission_path: Union[str, Path],
        sample_path: Optional[Union[str, Path]] = None,
        test_path: Optional[Union[str, Path]] = None,
        id_col: Optional[str] = None,
        target_cols: Optional[List[str]] = None,
        domain_type: str = "probability",
        valid_classes: Optional[Sequence[Any]] = None,
        expected_columns: Optional[List[str]] = None,
        expected_rows: Optional[int] = None,
    ) -> ValidationReport:
        """Validate a submission CSV file against reference CSV files."""
        return self.validate(
            df=submission_path,
            sample_df=sample_path,
            test_df=test_path,
            id_col=id_col,
            target_cols=target_cols,
            domain_type=domain_type,
            valid_classes=valid_classes,
            expected_columns=expected_columns,
            expected_rows=expected_rows,
        )

    def validate_arc_json(
        self,
        submission_data: Union[Dict[str, Any], str, Path],
        reference_tasks: Optional[Dict[str, Any]] = None,
    ) -> ValidationReport:
        """Audits ARC-AGI JSON submissions with strict Anti-Identity checks (Claim C40 / FAIL_11).
        
        Verifies:
        1. Valid dictionary structure with task IDs.
        2. Both attempt_1 and attempt_2 formatted as valid 2D grids (palette values 0-9).
        3. Non-empty grids with dimensions <= 30x30.
        4. Anti-Identity Guard: Flags errors if attempts are identical to input demonstration grids.
        """
        import json

        issues: List[ValidationIssue] = []
        raw_bytes = b""

        if isinstance(submission_data, (str, Path)):
            p = Path(submission_data)
            if p.is_file():
                raw_bytes = p.read_bytes()
                try:
                    data = json.loads(raw_bytes.decode("utf-8"))
                except Exception as e:
                    issues.append(
                        ValidationIssue(
                            level="ERROR",
                            check="json_syntax",
                            message=f"Corrupted or invalid JSON submission file: {e}",
                        )
                    )
                    return ValidationReport(
                        is_valid=False,
                        sha256="0" * 64,
                        row_count=0,
                        column_count=0,
                        issues=issues,
                        errors_count=1,
                        warnings_count=0,
                    )
            else:
                raw_bytes = str(submission_data).encode("utf-8")
                try:
                    data = json.loads(submission_data)
                except Exception as e:
                    issues.append(
                        ValidationIssue(
                            level="ERROR",
                            check="json_syntax",
                            message=f"Invalid JSON string: {e}",
                        )
                    )
                    return ValidationReport(
                        is_valid=False,
                        sha256="0" * 64,
                        row_count=0,
                        column_count=0,
                        issues=issues,
                        errors_count=1,
                        warnings_count=0,
                    )
        elif isinstance(submission_data, dict):
            data = submission_data
            raw_bytes = json.dumps(data).encode("utf-8")
        else:
            issues.append(
                ValidationIssue(
                    level="ERROR",
                    check="type_check",
                    message=f"Unsupported submission data type: {type(submission_data)}",
                )
            )
            return ValidationReport(
                is_valid=False,
                sha256="0" * 64,
                row_count=0,
                column_count=0,
                issues=issues,
                errors_count=1,
                warnings_count=0,
            )

        sha256 = self.compute_sha256_bytes(raw_bytes)

        if not data:
            issues.append(
                ValidationIssue(
                    level="ERROR",
                    check="empty_submission",
                    message="ARC submission dictionary is empty.",
                )
            )
            return ValidationReport(
                is_valid=False,
                sha256=sha256,
                row_count=0,
                column_count=0,
                issues=issues,
                errors_count=1,
                warnings_count=0,
            )

        # Audit expected task IDs if reference tasks supplied
        if reference_tasks is not None:
            expected_keys = set(reference_tasks.keys())
            actual_keys = set(data.keys())
            missing = expected_keys - actual_keys
            if missing:
                issues.append(
                    ValidationIssue(
                        level="ERROR",
                        check="task_coverage",
                        message=f"Missing {len(missing)} tasks in ARC submission: {list(missing)[:5]}...",
                    )
                )

        identity_violations = 0
        grid_format_violations = 0

        for task_id, attempts_entry in data.items():
            # Attempts can be a dict {'attempt_1': ..., 'attempt_2': ...} or a list of dicts
            item = attempts_entry[0] if isinstance(attempts_entry, list) and attempts_entry else attempts_entry

            if not isinstance(item, dict):
                issues.append(
                    ValidationIssue(
                        level="ERROR",
                        check="attempt_format",
                        message=f"Task '{task_id}' attempts must be a dict with attempt_1 and attempt_2.",
                    )
                )
                grid_format_violations += 1
                continue

            for attempt_key in ["attempt_1", "attempt_2"]:
                if attempt_key not in item:
                    issues.append(
                        ValidationIssue(
                            level="ERROR",
                            check="attempt_keys",
                            message=f"Task '{task_id}' is missing required key '{attempt_key}'.",
                        )
                    )
                    grid_format_violations += 1
                    continue

                grid = item[attempt_key]
                if not isinstance(grid, list) or len(grid) == 0 or not isinstance(grid[0], list):
                    issues.append(
                        ValidationIssue(
                            level="ERROR",
                            check="grid_dimensions",
                            message=f"Task '{task_id}' {attempt_key} is not a valid non-empty 2D list.",
                        )
                    )
                    grid_format_violations += 1
                    continue

                h, w = len(grid), len(grid[0])
                if h > 30 or w > 30:
                    issues.append(
                        ValidationIssue(
                            level="ERROR",
                            check="grid_bounds",
                            message=f"Task '{task_id}' {attempt_key} exceeds 30x30 limits ({h}x{w}).",
                        )
                    )

                # Check palette values
                for row in grid:
                    for val in row:
                        if not isinstance(val, int) or val < 0 or val > 9:
                            issues.append(
                                ValidationIssue(
                                    level="ERROR",
                                    check="palette_domain",
                                    message=f"Task '{task_id}' {attempt_key} contains invalid color value: {val}.",
                                )
                            )
                            grid_format_violations += 1
                            break

                # Anti-identity check against input grid if reference task is supplied
                if reference_tasks and task_id in reference_tasks:
                    ref_task = reference_tasks[task_id]
                    test_pair = ref_task.get("test", [{}])[0]
                    inp_grid = test_pair.get("input", [])
                    if grid == inp_grid:
                        identity_violations += 1
                        issues.append(
                            ValidationIssue(
                                level="ERROR",
                                check="anti_identity_collapse",
                                message=f"Task '{task_id}' {attempt_key} is IDENTICAL to input test grid (FAIL_11). Guarantees 0.00 score!",
                            )
                        )

        errors_count = sum(1 for i in issues if i.level == "ERROR")
        warnings_count = sum(1 for i in issues if i.level == "WARNING")

        return ValidationReport(
            is_valid=(errors_count == 0),
            sha256=sha256,
            row_count=len(data),
            column_count=2,  # attempt_1 and attempt_2
            issues=issues,
            errors_count=errors_count,
            warnings_count=warnings_count,
        )

    def validate_multilabel_schema(
        self,
        df: Any,
        id_col: str,
        expected_target_cols: List[str],
        expected_rows: Optional[int] = None,
    ) -> ValidationReport:
        """Convenience auditor for multi-label competitions (such as RSNA Knee 12-class)."""
        expected_columns = [id_col] + list(expected_target_cols)
        return self.validate(
            df=df,
            id_col=id_col,
            target_cols=expected_target_cols,
            domain_type="probability",
            expected_columns=expected_columns,
            expected_rows=expected_rows,
        )

