"""Page 1: Executive Dashboard - Institutional Overview and Retention Telemetry."""

import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.kpi_cards import render_kpi_card
from app.components.charts import (
    plot_department_performance,
    plot_risk_distribution,
    plot_attendance_vs_cgpa,
    plot_cgpa_distribution
)
from src.analytics.queries import (
    get_kpis,
    get_department_metrics,
    get_risk_distribution,
    get_attendance_vs_cgpa,
    get_cgpa_distribution
)
from src.analytics.insights import generate_executive_insights

st.set_page_config(page_title="Executive Dashboard | StudentIQ", page_icon="📊", layout="wide")
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <h1 style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">Executive Dashboard</h1>
    <p style="color: #94A3B8; font-size: 0.95rem;">Institutional performance metrics, retention vulnerability distribution, and departmental benchmarks.</p>
</div>
""", unsafe_allow_html=True)

# Executive KPIs
kpis = get_kpis()
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Total Cohort", f"{kpis.get('total_students', 0):,}", "Enrolled active students", accent_color="#00E5FF")
with c2:
    render_kpi_card("Average CGPA", f"{kpis.get('avg_cgpa', 0.0):.2f}", "Academic quality benchmark", accent_color="#7C4DFF")
with c3:
    render_kpi_card("Average Attendance", f"{kpis.get('avg_attendance', 0.0):.1f}%", "Cohort engagement rate", accent_color="#00E676")
with c4:
    at_risk = kpis.get('at_risk_students', 0)
    pct = kpis.get('at_risk_percentage', 0.0)
    render_kpi_card("Retention Vulnerability", f"{at_risk}", f"{pct}% of students at risk", delta=f"{kpis.get('critical_risk_count', 0)} Critical", delta_color="negative", accent_color="#FF1744")

# Primary Visualizations Row
col_left, col_right = st.columns([6, 4])

with col_left:
    st.markdown("<div style='font-size: 1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;'>Department Comparative Performance</div>", unsafe_allow_html=True)
    dept_df = get_department_metrics()
    if not dept_df.empty:
        st.plotly_chart(plot_department_performance(dept_df), use_container_width=True)
    else:
        st.info("No department data available.")

with col_right:
    st.markdown("<div style='font-size: 1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;'>Retention Risk Breakdown</div>", unsafe_allow_html=True)
    risk_df = get_risk_distribution()
    if not risk_df.empty:
        st.plotly_chart(plot_risk_distribution(risk_df), use_container_width=True)
    else:
        st.info("No risk distribution data available.")

# Secondary Visualizations Row
col_s1, col_s2 = st.columns(2)

with col_s1:
    st.markdown("<div style='font-size: 1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;'>Attendance vs CGPA Correlation Matrix</div>", unsafe_allow_html=True)
    scatter_df = get_attendance_vs_cgpa()
    if not scatter_df.empty:
        st.plotly_chart(plot_attendance_vs_cgpa(scatter_df), use_container_width=True)
    else:
        st.info("No correlation data available.")

with col_s2:
    st.markdown("<div style='font-size: 1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;'>Grade Point Band Distribution</div>", unsafe_allow_html=True)
    cgpa_dist_df = get_cgpa_distribution()
    if not cgpa_dist_df.empty:
        st.plotly_chart(plot_cgpa_distribution(cgpa_dist_df), use_container_width=True)
    else:
        st.info("No CGPA distribution data available.")