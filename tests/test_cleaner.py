"""Tests for Data Cleaner and Normalizers."""

import pytest
import pandas as pd
from src.data.normalizer import (
    normalize_attendance,
    normalize_cgpa,
    normalize_department,
    normalize_gender,
    normalize_student_id
)
from src.data.cleaner import StudentDataCleaner

def test_attendance_normalization():
    # Percentage string
    val, mod = normalize_attendance("85%")
    assert val == 85.0
    assert mod is True

    # Decimal ratio
    val, mod = normalize_attendance(0.85)
    assert val == 85.0
    assert mod is True

    # Out of bounds typo (850 -> 85.0)
    val, mod = normalize_attendance(850)
    assert val == 85.0
    assert mod is True

    # Whitespace
    val, mod = normalize_attendance("  72 %  ")
    assert val == 72.0

def test_cgpa_normalization():
    # Comma format
    val, mod = normalize_cgpa("7,85")
    assert val == 7.85
    assert mod is True

    # Out of bounds (>10)
    val, mod = normalize_cgpa(14.5)
    assert val is None

    # Negative
    val, mod = normalize_cgpa(-2.0)
    assert val is None

def test_department_normalization():
    val, _ = normalize_department("cse")
    assert val == "Computer Science & Engineering"

    val, _ = normalize_department("mech")
    assert val == "Mechanical Engineering"

    val, _ = normalize_department("ece")
    assert val == "Electronics & Communication Engineering"

def test_gender_normalization():
    val, _ = normalize_gender("m")
    assert val == "Male"
    val, _ = normalize_gender("girl")
    assert val == "Female"

def test_student_id_normalization():
    val, mod = normalize_student_id("stu_1005")
    assert val == "STU-1005"
    assert mod is True

def test_full_cleaning_pipeline():
    cleaner = StudentDataCleaner()
    messy_data = pd.DataFrame([
        {"student_id": "STU-1001", "name": "Aditya Sharma", "department": "cse", "gender": "m", "cgpa": "8.5", "attendance": "85%", "enrollment_date": "2023-08-01"},
        {"student_id": "STU-1001", "name": "Aditya Sharma", "department": "cse", "gender": "m", "cgpa": "8.5", "attendance": "85%", "enrollment_date": "2023-08-01"}, # Duplicate
        {"student_id": "stu_1002", "name": "Pooja Patel", "department": "mech", "gender": "female", "cgpa": "14.0", "attendance": "0.55", "enrollment_date": "15/08/2023"}, # Out of bounds CGPA
    ])
    cleaned_df, report = cleaner.clean(messy_data)
    assert len(cleaned_df) == 2
    assert report["duplicates_removed"] >= 1
    assert "academic_risk_score" in cleaned_df.columns
    assert "risk_level" in cleaned_df.columns