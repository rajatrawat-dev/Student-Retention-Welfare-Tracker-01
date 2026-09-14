"""Tests for DuckDB database execution and queries."""

import pytest
import pandas as pd
from src.analytics.database import db_manager
from src.analytics.queries import get_kpis, get_department_metrics, get_risk_distribution

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    test_df = pd.DataFrame([
        {"student_id": "STU-101", "name": "Alice", "department": "Computer Science & Engineering", "gender": "Female", "cgpa": 8.5, "attendance": 90.0, "enrollment_date": "2023-08-01", "attendance_percentage": 90.0, "academic_risk_score": 13.0, "risk_level": "LOW", "support_priority": "Routine"},
        {"student_id": "STU-102", "name": "Bob", "department": "Mechanical Engineering", "gender": "Male", "cgpa": 4.5, "attendance": 52.0, "enrollment_date": "2023-08-01", "attendance_percentage": 52.0, "academic_risk_score": 52.2, "risk_level": "CRITICAL", "support_priority": "Immediate Intervention"},
        {"student_id": "STU-103", "name": "Charlie", "department": "Computer Science & Engineering", "gender": "Male", "cgpa": 6.8, "attendance": 78.0, "enrollment_date": "2023-08-01", "attendance_percentage": 78.0, "academic_risk_score": 28.0, "risk_level": "MEDIUM", "support_priority": "Monitor"},
    ])
    db_manager.init_database(test_df)

def test_get_kpis_query():
    kpis = get_kpis()
    assert kpis["total_students"] == 3
    assert kpis["critical_risk_count"] == 1
    assert kpis["departments_count"] == 2

def test_get_department_metrics_query():
    df = get_department_metrics()
    assert len(df) == 2
    assert "avg_cgpa" in df.columns

def test_get_risk_distribution_query():
    df = get_risk_distribution()
    assert len(df) >= 2
    assert "risk_level" in df.columns