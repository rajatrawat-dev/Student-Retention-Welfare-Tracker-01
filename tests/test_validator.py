"""Tests for Schema Validation and Data Quality Scoring."""

import pytest
import pandas as pd
from src.data.validator import validate_schema, check_value_ranges, detect_suspicious_records, calculate_quality_score

def test_validate_schema_valid():
    df = pd.DataFrame(columns=["student_id", "name", "department", "gender", "cgpa", "attendance", "enrollment_date"])
    is_valid, missing = validate_schema(df)
    assert is_valid is True
    assert len(missing) == 0

def test_validate_schema_missing_column():
    df = pd.DataFrame(columns=["student_id", "name"])
    is_valid, missing = validate_schema(df)
    assert is_valid is False
    assert "cgpa" in missing

def test_detect_suspicious_records():
    df = pd.DataFrame([
        {"student_id": "STU-1", "name": "Suspicious A", "cgpa": 9.9, "attendance": 15.0},
        {"student_id": "STU-2", "name": "Normal B", "cgpa": 7.5, "attendance": 80.0},
    ])
    suspicious = detect_suspicious_records(df)
    assert len(suspicious) == 1
    assert suspicious.iloc[0]["student_id"] == "STU-1"

def test_quality_score_calculation():
    metrics = {
        "rows_before": 100,
        "duplicates_removed": 5,
        "missing_imputed": 10,
        "invalid_values_repaired": 4,
        "suspicious_records_detected": 1
    }
    score = calculate_quality_score(metrics)
    assert 0.0 <= score <= 100.0
    assert score > 60.0 # Expected reasonable score