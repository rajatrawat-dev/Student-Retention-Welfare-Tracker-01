"""Tests for AI Analyst Agent and AI Safety Query Validator."""

import pytest
from src.agent.query_validator import validate_query
from src.agent.intent import detect_intent
from src.agent.chart_selector import recommend_chart_type
from src.agent.query_generator import generate_sql_via_rules
from src.agent.agent import student_iq_analyst
import pandas as pd

def test_ai_safety_rejection_drop():
    sql = "DROP TABLE students;"
    is_safe, msg = validate_query(sql)
    assert is_safe is False
    assert "DROP" in msg

def test_ai_safety_rejection_delete():
    sql = "DELETE FROM students WHERE cgpa < 4.0;"
    is_safe, msg = validate_query(sql)
    assert is_safe is False
    assert "DELETE" in msg

def test_ai_safety_rejection_insert():
    sql = "INSERT INTO students VALUES ('STU-999', 'Fake', 5.0);"
    is_safe, msg = validate_query(sql)
    assert is_safe is False

def test_ai_safety_rejection_multi_statement():
    sql = "SELECT * FROM students; DROP TABLE students;"
    is_safe, msg = validate_query(sql)
    assert is_safe is False
    assert "Multi-statement" in msg

def test_ai_safety_allowed_select():
    sql = "SELECT department, AVG(cgpa) FROM students GROUP BY department;"
    is_safe, _ = validate_query(sql)
    assert is_safe is True

def test_intent_detection():
    intent, params = detect_intent("Show students with attendance below 60%")
    assert intent == "ATTENDANCE_QUERY"
    assert params.get("threshold") == 60.0

    intent, _ = detect_intent("Which departments have the lowest average CGPA?")
    assert intent == "DEPARTMENT_QUERY"

    intent, _ = detect_intent("Show top 10 students by CGPA")
    assert intent == "TOP_PERFORMERS"

def test_chart_selector():
    # Comparison
    dept_df = pd.DataFrame({"department": ["CSE", "ECE"], "avg_cgpa": [8.5, 7.8]})
    chart = recommend_chart_type("DEPARTMENT_QUERY", dept_df)
    assert chart == "bar"

    # Scatter
    scatter_df = pd.DataFrame({"attendance": range(20), "cgpa": range(20)})
    chart = recommend_chart_type("CORRELATION_QUERY", scatter_df)
    assert chart == "scatter"

def test_agent_end_to_end():
    resp = student_iq_analyst.ask("Which departments have the lowest average CGPA?")
    assert resp.is_safe is True
    assert resp.execution_success is True
    assert resp.data is not None
    assert len(resp.data) > 0