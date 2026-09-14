"""Pre-built analytical query abstractions executed via DuckDB."""

from typing import Dict, Any, Optional, List
import pandas as pd
from src.analytics.database import db_manager
from src.config.settings import settings

def get_kpis() -> Dict[str, Any]:
    """Retrieves high-level summary KPIs via DuckDB."""
    query = """
    SELECT 
        COUNT(*) as total_students,
        ROUND(AVG(cgpa), 2) as avg_cgpa,
        ROUND(AVG(attendance), 2) as avg_attendance,
        SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as at_risk_count,
        ROUND(SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as at_risk_percentage,
        SUM(CASE WHEN risk_level = 'CRITICAL' THEN 1 ELSE 0 END) as critical_count,
        COUNT(DISTINCT department) as department_count
    FROM students;
    """
    df = db_manager.execute_query(query)
    if df.empty:
        return {}
    row = df.iloc[0]
    return {
        "total_students": int(row["total_students"]),
        "avg_cgpa": float(row["avg_cgpa"] or 0.0),
        "avg_attendance": float(row["avg_attendance"] or 0.0),
        "at_risk_students": int(row["at_risk_count"] or 0),
        "at_risk_percentage": float(row["at_risk_percentage"] or 0.0),
        "critical_risk_count": int(row["critical_count"] or 0),
        "departments_count": int(row["department_count"] or 0),
    }

def get_department_metrics() -> pd.DataFrame:
    """Returns department aggregations."""
    query = """
    SELECT 
        department,
        COUNT(*) as student_count,
        ROUND(AVG(cgpa), 2) as avg_cgpa,
        ROUND(AVG(attendance), 2) as avg_attendance,
        ROUND(AVG(academic_risk_score), 2) as avg_risk_score,
        SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as at_risk_count,
        ROUND(SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as at_risk_percentage
    FROM students
    GROUP BY department
    ORDER BY avg_cgpa DESC;
    """
    return db_manager.execute_query(query)

def get_risk_distribution() -> pd.DataFrame:
    """Returns risk level breakdown."""
    query = """
    SELECT 
        risk_level,
        COUNT(*) as student_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students), 1) as percentage,
        ROUND(AVG(cgpa), 2) as avg_cgpa,
        ROUND(AVG(attendance), 2) as avg_attendance
    FROM students
    GROUP BY risk_level
    ORDER BY 
        CASE risk_level 
            WHEN 'CRITICAL' THEN 1 
            WHEN 'HIGH' THEN 2 
            WHEN 'MEDIUM' THEN 3 
            ELSE 4 
        END;
    """
    return db_manager.execute_query(query)

def get_cgpa_distribution() -> pd.DataFrame:
    """Returns CGPA grouped by grade brackets."""
    query = """
    SELECT 
        CASE 
            WHEN cgpa >= 9.0 THEN '9.0 - 10.0 (Outstanding)'
            WHEN cgpa >= 8.0 THEN '8.0 - 8.9 (Very Good)'
            WHEN cgpa >= 7.0 THEN '7.0 - 7.9 (Good)'
            WHEN cgpa >= 6.0 THEN '6.0 - 6.9 (Average)'
            WHEN cgpa >= 5.0 THEN '5.0 - 5.9 (Pass)'
            ELSE 'Below 5.0 (Critical)'
        END as cgpa_bracket,
        COUNT(*) as count
    FROM students
    GROUP BY cgpa_bracket
    ORDER BY MIN(cgpa) DESC;
    """
    return db_manager.execute_query(query)

def get_attendance_vs_cgpa() -> pd.DataFrame:
    """Returns attendance and CGPA points for scatter/correlation analysis."""
    query = """
    SELECT 
        student_id,
        name,
        department,
        attendance,
        cgpa,
        risk_level,
        support_priority
    FROM students;
    """
    return db_manager.execute_query(query)

def get_top_performers(limit: int = 10) -> pd.DataFrame:
    """Fetches top students by CGPA."""
    query = f"""
    SELECT 
        student_id,
        name,
        department,
        cgpa,
        attendance,
        risk_level
    FROM students
    ORDER BY cgpa DESC, attendance DESC
    LIMIT {limit};
    """
    return db_manager.execute_query(query)

def get_students_requiring_support(limit: int = 25) -> pd.DataFrame:
    """Fetches critical and high risk students requiring immediate academic support."""
    query = f"""
    SELECT 
        student_id,
        name,
        department,
        cgpa,
        attendance,
        academic_risk_score,
        risk_level,
        support_priority
    FROM students
    WHERE risk_level IN ('CRITICAL', 'HIGH')
    ORDER BY academic_risk_score DESC, attendance ASC
    LIMIT {limit};
    """
    return db_manager.execute_query(query)

def filter_students(
    department: Optional[str] = None,
    gender: Optional[str] = None,
    min_cgpa: Optional[float] = None,
    max_cgpa: Optional[float] = None,
    min_attendance: Optional[float] = None,
    max_attendance: Optional[float] = None,
    risk_level: Optional[str] = None,
    search_term: Optional[str] = None,
    limit: int = 200,
) -> pd.DataFrame:
    """Dynamic multi-criteria search and filter."""
    conditions = ["1=1"]
    params: List[Any] = []

    if department and department != "All":
        conditions.append("department = ?")
        params.append(department)
    if gender and gender != "All":
        conditions.append("gender = ?")
        params.append(gender)
    if min_cgpa is not None:
        conditions.append("cgpa >= ?")
        params.append(min_cgpa)
    if max_cgpa is not None:
        conditions.append("cgpa <= ?")
        params.append(max_cgpa)
    if min_attendance is not None:
        conditions.append("attendance >= ?")
        params.append(min_attendance)
    if max_attendance is not None:
        conditions.append("attendance <= ?")
        params.append(max_attendance)
    if risk_level and risk_level != "All":
        conditions.append("risk_level = ?")
        params.append(risk_level)
    if search_term:
        conditions.append("(LOWER(name) LIKE ? OR LOWER(student_id) LIKE ?)")
        term = f"%{search_term.lower()}%"
        params.extend([term, term])

    where_clause = " AND ".join(conditions)
    query = f"""
    SELECT 
        student_id,
        name,
        department,
        gender,
        cgpa,
        attendance,
        enrollment_date,
        academic_risk_score,
        risk_level,
        support_priority
    FROM students
    WHERE {where_clause}
    ORDER BY academic_risk_score DESC
    LIMIT {limit};
    """
    return db_manager.execute_query(query, params)
