"""Calculates core statistical and retention metrics."""

from typing import Dict, Any
import pandas as pd
import numpy as np
from src.config.settings import settings
from src.utils.helpers import safe_round

def compute_overall_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculates top-level operational KPIs from DataFrame."""
    if df.empty:
        return {
            "total_students": 0,
            "avg_cgpa": 0.0,
            "avg_attendance": 0.0,
            "at_risk_students": 0,
            "at_risk_percentage": 0.0,
            "critical_risk_count": 0,
            "departments_count": 0,
        }
        
    total = len(df)
    at_risk = int((df["risk_level"].isin(["HIGH", "CRITICAL"])).sum())
    critical = int((df["risk_level"] == "CRITICAL").sum())
    
    return {
        "total_students": total,
        "avg_cgpa": safe_round(df["cgpa"].mean(), 2),
        "avg_attendance": safe_round(df["attendance"].mean(), 2),
        "at_risk_students": at_risk,
        "at_risk_percentage": safe_round((at_risk / total) * 100.0, 1),
        "critical_risk_count": critical,
        "departments_count": int(df["department"].nunique()),
    }

def compute_retention_risk_index(df: pd.DataFrame) -> float:
    """Computes an institutional retention risk index (0 - 100)."""
    if df.empty:
        return 0.0
    # Weighted calculation
    critical_w = (df["risk_level"] == "CRITICAL").mean() * 100.0 * 1.5
    high_w = (df["risk_level"] == "HIGH").mean() * 100.0 * 1.0
    med_w = (df["risk_level"] == "MEDIUM").mean() * 100.0 * 0.4
    index = min(100.0, critical_w + high_w + med_w)
    return safe_round(index, 1)

def compute_attendance_cgpa_correlation(df: pd.DataFrame) -> float:
    """Calculates Pearson correlation between attendance and CGPA."""
    if df.empty or len(df) < 2:
        return 0.0
    corr = df["attendance"].corr(df["cgpa"])
    return safe_round(corr, 3)
