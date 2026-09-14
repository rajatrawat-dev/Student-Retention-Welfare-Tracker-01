"""Tests for Metrics and Analytical Computations."""

import pytest
import pandas as pd
from src.analytics.metrics import compute_overall_kpis, compute_retention_risk_index, compute_attendance_cgpa_correlation

def test_overall_kpis():
    df = pd.DataFrame([
        {"student_id": "STU-1", "cgpa": 8.0, "attendance": 85.0, "risk_level": "LOW", "department": "CSE"},
        {"student_id": "STU-2", "cgpa": 5.0, "attendance": 55.0, "risk_level": "CRITICAL", "department": "MECH"},
    ])
    kpis = compute_overall_kpis(df)
    assert kpis["total_students"] == 2
    assert kpis["avg_cgpa"] == 6.5
    assert kpis["avg_attendance"] == 70.0
    assert kpis["critical_risk_count"] == 1
    assert kpis["at_risk_students"] == 1

def test_correlation_computation():
    df = pd.DataFrame({
        "attendance": [50.0, 60.0, 70.0, 80.0, 90.0],
        "cgpa": [5.0, 6.0, 7.0, 8.0, 9.0]
    })
    corr = compute_attendance_cgpa_correlation(df)
    assert corr == 1.0