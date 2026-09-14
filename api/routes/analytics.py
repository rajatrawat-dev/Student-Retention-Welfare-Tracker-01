"""Aggregated analytical endpoints for executive decision support."""

from typing import Dict, Any, List
from fastapi import APIRouter
from src.analytics.queries import (
    get_kpis,
    get_department_metrics,
    get_risk_distribution,
    get_cgpa_distribution,
    get_attendance_vs_cgpa
)
from src.analytics.insights import generate_executive_insights

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
def get_summary_kpis() -> Dict[str, Any]:
    """Returns top-level executive KPIs and dynamic narrative insights."""
    kpis = get_kpis()
    insights = generate_executive_insights()
    return {
        "kpis": kpis,
        "executive_insights": insights
    }

@router.get("/departments")
def get_departments_breakdown() -> List[Dict[str, Any]]:
    """Returns aggregated academic and attendance metrics per department."""
    df = get_department_metrics()
    return df.to_dict(orient="records")

@router.get("/risk")
def get_risk_breakdown() -> List[Dict[str, Any]]:
    """Returns retention risk tier distribution."""
    df = get_risk_distribution()
    return df.to_dict(orient="records")