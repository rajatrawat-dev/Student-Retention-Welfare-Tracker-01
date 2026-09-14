"""Generates dynamic data-driven insights. Never hardcoded."""

from typing import List, Dict, Any
import pandas as pd
from src.analytics.queries import get_department_metrics, get_kpis
from src.analytics.metrics import compute_attendance_cgpa_correlation
from src.analytics.database import db_manager

def generate_executive_insights() -> List[Dict[str, str]]:
    """Synthesizes dynamic narrative findings from the underlying DuckDB data."""
    insights = []
    
    kpis = get_kpis()
    dept_df = get_department_metrics()
    
    if not kpis or dept_df.empty:
        return [{"type": "INFO", "title": "Awaiting Data", "text": "Run data rescue to view dynamic insights."}]
        
    # Insight 1: Department performance leader
    top_dept = dept_df.iloc[0]
    insights.append({
        "type": "SUCCESS",
        "title": "Academic Leadership",
        "text": f"{top_dept['department']} leads the institution with the highest average CGPA of {top_dept['avg_cgpa']} and an attendance rate of {top_dept['avg_attendance']}%."
    })
    
    # Insight 2: Department requiring support
    dept_sorted_by_risk = dept_df.sort_values(by="at_risk_percentage", ascending=False)
    highest_risk_dept = dept_sorted_by_risk.iloc[0]
    insights.append({
        "type": "WARNING",
        "title": "Welfare Attention Required",
        "text": f"{highest_risk_dept['department']} exhibits the greatest retention vulnerability, with {highest_risk_dept['at_risk_percentage']}% of its students flagged for academic or attendance risk."
    })
    
    # Insight 3: Correlation between attendance and performance
    corr_df = db_manager.execute_query("SELECT attendance, cgpa FROM students;")
    corr = compute_attendance_cgpa_correlation(corr_df)
    corr_str = "strong" if abs(corr) > 0.6 else "moderate" if abs(corr) > 0.3 else "mild"
    insights.append({
        "type": "INFO",
        "title": "Attendance & Retention Correlation",
        "text": f"Empirical correlation between attendance and CGPA stands at r = {corr} ({corr_str} positive association). Interventions boosting attendance directly safeguard student grade points."
    })
    
    # Insight 4: Critical students alert
    critical_count = kpis.get("critical_risk_count", 0)
    if critical_count > 0:
        insights.append({
            "type": "CRITICAL",
            "title": "Immediate Welfare Priority",
            "text": f"{critical_count} students fall under the 'CRITICAL' risk tier and have been queued for Immediate Welfare Advisory."
        })
    else:
        insights.append({
            "type": "SUCCESS",
            "title": "Stable Welfare Status",
            "text": "Zero students currently fulfill critical risk criteria. Standard academic monitoring applies."
        })
        
    return insights
