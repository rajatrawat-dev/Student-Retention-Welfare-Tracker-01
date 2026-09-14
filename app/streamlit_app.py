"""StudentIQ - Student Retention & Welfare Intelligence
TransOrg GraphIQ Datathon | Education & EdTech Track
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.kpi_cards import render_kpi_card
from src.analytics.queries import get_kpis
from src.analytics.insights import generate_executive_insights
from src.data.quality_report import QualityReport

st.set_page_config(
    page_title="StudentIQ | Retention & Welfare Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic Dark Theme Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #0A0E17;
        color: #F8FAFC;
    }
    
    /* Header hero styling */
    .hero-container {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.08) 0%, rgba(124, 77, 255, 0.08) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2.2rem 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #00E5FF 0%, #7C4DFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        max-width: 800px;
        line-height: 1.6;
    }
    
    /* Card container */
    .glass-card {
        background: rgba(18, 24, 38, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Render Sidebar
render_sidebar()

# Hero Section
st.markdown("""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <div class="hero-title">StudentIQ</div>
            <div style="font-size: 0.95rem; font-weight: 600; color: #00E5FF; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.6rem;">
                Student Retention & Welfare Intelligence
            </div>
            <div class="hero-subtitle">
                Turn messy student data into actionable retention and welfare insights. 
                Powered by a 14-step Data Rescue engine, DuckDB analytics, predictive ML risk models, and an AI Analyst copilot.
            </div>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(0, 229, 255, 0.12); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3); padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">
                HACKATHON BUILD v1.0
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Operational KPIs
kpis = get_kpis()
q_report = QualityReport.load()

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card("Total Students", f"{kpis.get('total_students', 0):,}", "Active registered student cohort", accent_color="#00E5FF")
with col2:
    render_kpi_card("Average CGPA", f"{kpis.get('avg_cgpa', 0.0):.2f}", "Scale: 0.0 - 10.0 scale", accent_color="#7C4DFF")
with col3:
    render_kpi_card("Average Attendance", f"{kpis.get('avg_attendance', 0.0):.1f}%", "Overall institutional average", accent_color="#00E676")
with col4:
    at_risk = kpis.get('at_risk_students', 0)
    pct = kpis.get('at_risk_percentage', 0.0)
    render_kpi_card("At-Risk Students", f"{at_risk}", f"{pct}% of student body flagged", delta=f"{kpis.get('critical_risk_count', 0)} Critical", delta_color="negative", accent_color="#FF1744")

# Data Rescue Story Summary Banner
if q_report:
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, rgba(0, 230, 118, 0.08) 0%, rgba(0, 229, 255, 0.05) 100%); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 0.8rem; font-weight: 700; color: #00E676; text-transform: uppercase; letter-spacing: 0.08em;">Layer 1: Data Rescue Provenance</span>
                <h4 style="color: #F8FAFC; margin: 0.25rem 0 0.4rem 0;">From Messy Data to Verified Ground Truth</h4>
                <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">
                    Raw input resolved: <b>{q_report.get('duplicates_removed', 0)}</b> duplicates dropped, 
                    <b>{q_report.get('missing_values_imputed', 0)}</b> missing entries imputed, 
                    <b>{q_report.get('invalid_values_repaired', 0)}</b> invalid values corrected, 
                    <b>{q_report.get('suspicious_records_detected', 0)}</b> anomalies flagged. 
                    Calculated Data Quality Score: <b>{q_report.get('data_quality_score', 0)}/100</b>.
                </p>
            </div>
            <div style="text-align: right; min-width: 140px;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #00E676;">{q_report.get('data_quality_score', 0)}<span style="font-size: 1rem; color: #94A3B8;">/100</span></div>
                <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase;">Quality Score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Dynamic Executive Insights
insights = generate_executive_insights()
st.subheader("Executive Intelligence Summary")
insight_cols = st.columns(len(insights) if insights else 1)

type_colors = {
    "SUCCESS": ("#00E676", "rgba(0, 230, 118, 0.1)"),
    "WARNING": ("#FF9100", "rgba(255, 145, 0, 0.1)"),
    "INFO": ("#00E5FF", "rgba(0, 229, 255, 0.1)"),
    "CRITICAL": ("#FF1744", "rgba(255, 23, 68, 0.1)"),
}

for i, ins in enumerate(insights):
    color, bg = type_colors.get(ins.get("type", "INFO"), ("#00E5FF", "rgba(0, 229, 255, 0.1)"))
    with insight_cols[i]:
        st.markdown(f"""
        <div style="background: {bg}; border: 1px solid {color}44; border-top: 3px solid {color}; border-radius: 10px; padding: 1rem; height: 100%;">
            <div style="font-size: 0.75rem; font-weight: 700; color: {color}; text-transform: uppercase; letter-spacing: 0.05em;">
                {ins.get('title')}
            </div>
            <div style="font-size: 0.85rem; color: #E2E8F0; margin-top: 0.5rem; line-height: 1.45;">
                {ins.get('text')}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Cards
st.subheader("Platform Architecture & Modules")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="color: #00E5FF; font-weight: 700; font-size: 0.9rem;">01. Executive Dashboard</div>
        <p style="color: #94A3B8; font-size: 0.8rem; margin-top: 0.5rem;">
            Institutional KPI radar, department comparisons, retention risk breakdown, and student distributions.
        </p>
    </div>
    """, unsafe_allow_html=True)
with m2:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="color: #00E676; font-weight: 700; font-size: 0.9rem;">02. Data Quality</div>
        <p style="color: #94A3B8; font-size: 0.8rem; margin-top: 0.5rem;">
            Full 14-step Data Rescue telemetry, before vs after metrics, anomaly logs, and data quality scoring.
        </p>
    </div>
    """, unsafe_allow_html=True)
with m3:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="color: #FF9100; font-weight: 700; font-size: 0.9rem;">03. Risk Analysis</div>
        <p style="color: #94A3B8; font-size: 0.8rem; margin-top: 0.5rem;">
            Predictive ML retention model, risk score rankings, factor explanations, and welfare priority queue.
        </p>
    </div>
    """, unsafe_allow_html=True)
with m4:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="color: #7C4DFF; font-weight: 700; font-size: 0.9rem;">04. AI Analyst Copilot</div>
        <p style="color: #94A3B8; font-size: 0.8rem; margin-top: 0.5rem;">
            Natural language queries with AI safety validation, automated DuckDB SQL generation, and dynamic charts.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.info("Use the sidebar on the left to navigate through all specialized analytical intelligence pages.")