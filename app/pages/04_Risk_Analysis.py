"""Page 4: Retention Risk Analysis & Early Warning System."""

import streamlit as st
import sys
from pathlib import Path
import plotly.express as px

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.kpi_cards import render_kpi_card
from app.components.charts import apply_base_layout, RISK_COLOR_MAP
from app.components.tables import render_styled_dataframe
from src.analytics.queries import get_kpis, get_students_requiring_support, get_department_metrics
from src.analytics.database import db_manager
from src.ml.predict import predict_single_student

st.set_page_config(page_title="Risk Analysis | StudentIQ", page_icon="⚠️", layout="wide")
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <h1 style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">Retention Risk Analysis</h1>
    <p style="color: #94A3B8; font-size: 0.95rem;">Early-warning welfare analytics, institutional risk score distribution, and individualized academic risk explanations.</p>
</div>
""", unsafe_allow_html=True)

# Welfare Disclaimer Alert
st.markdown("""
<div style="background: rgba(0, 229, 255, 0.05); border-left: 4px solid #00E5FF; padding: 0.8rem 1.2rem; border-radius: 4px; margin-bottom: 1.5rem; font-size: 0.85rem; color: #CBD5E1;">
    <b>Institutional Analytics Notice:</b> StudentIQ evaluates retention and academic vulnerability based on verifiable empirical indicators (attendance regularity, cumulative grade trends). It serves strictly as an academic-support prioritization tool, <b>not</b> a medical, psychological, or behavioral diagnosis.
</div>
""", unsafe_allow_html=True)

kpis = get_kpis()
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Critical Risk Students", f"{kpis.get('critical_risk_count', 0)}", "Requiring immediate intervention", accent_color="#FF1744")
with c2:
    render_kpi_card("High Risk Students", f"{kpis.get('at_risk_students', 0) - kpis.get('critical_risk_count', 0)}", "Advisory alert tier", accent_color="#FF9100")
with c3:
    render_kpi_card("Attendance Threshold", "< 75.0%", "Institutional mandatory cutoff", accent_color="#FFD600")
with c4:
    render_kpi_card("CGPA Benchmark", "< 6.0", "Remedial tutoring cutoff", accent_color="#7C4DFF")

# Visualizations Row
col_v1, col_v2 = st.columns(2)

with col_v1:
    st.markdown("<div style='font-size: 1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;'>Academic Risk Score Distribution (0-100)</div>", unsafe_allow_html=True)
    score_df = db_manager.execute_query("SELECT academic_risk_score, risk_level FROM students;")
    fig = px.histogram(
        score_df,
        x="academic_risk_score",
        color="risk_level",
        nbins=25,
        color_discrete_map=RISK_COLOR_MAP,
        labels={"academic_risk_score": "Composite Risk Score (Higher = Greater Vulnerability)"}
    )
    st.plotly_chart(apply_base_layout(fig, "Cohort Risk Score Spread"), use_container_width=True)

with col_v2:
    st.markdown("<div style='font-size: 1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;'>Departmental Risk Concentration</div>", unsafe_allow_html=True)
    dept_df = get_department_metrics()
    fig2 = px.bar(
        dept_df.sort_values(by="at_risk_percentage", ascending=False),
        x="department",
        y="at_risk_percentage",
        color="at_risk_percentage",
        color_continuous_scale="Reds",
        labels={"at_risk_percentage": "At-Risk Student %"}
    )
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(apply_base_layout(fig2, "At-Risk Proportion by Department"), use_container_width=True)

# Individual Student Diagnostic Inspector
st.subheader("Individual Student Risk Diagnostic & Factor Analysis")
support_list = get_students_requiring_support(50)
selected_id = st.selectbox(
    "Select Student for Diagnostic Inspection:",
    options=support_list["student_id"].tolist(),
    format_func=lambda x: f"{x} - {support_list.loc[support_list['student_id'] == x, 'name'].values[0]} ({support_list.loc[support_list['student_id'] == x, 'risk_level'].values[0]} Risk)"
)

if selected_id:
    student_row = support_list[support_list["student_id"] == selected_id].iloc[0].to_dict()
    diag = predict_single_student(student_row)
    
    col_d1, col_d2 = st.columns([1, 2])
    with col_d1:
        st.markdown(f"""
        <div style="background: rgba(18, 24, 38, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 1.2rem;">
            <div style="font-size: 1.1rem; font-weight: 700; color: #F8FAFC;">{student_row['name']}</div>
            <div style="font-size: 0.85rem; color: #00E5FF; margin-bottom: 0.75rem;">{student_row['student_id']} | {student_row['department']}</div>
            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 0.5rem 0;">
            <div style="font-size: 0.85rem; color: #94A3B8;"><b>Cumulative GPA:</b> {student_row['cgpa']}</div>
            <div style="font-size: 0.85rem; color: #94A3B8;"><b>Attendance Rate:</b> {student_row['attendance']}%</div>
            <div style="font-size: 0.85rem; color: #94A3B8;"><b>Risk Score:</b> {student_row.get('academic_risk_score', 'N/A')}</div>
            <div style="font-size: 0.85rem; color: #FF1744; margin-top: 0.5rem;"><b>Priority:</b> {diag['support_priority']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_d2:
        st.markdown("<div style='font-size: 0.9rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;'>Key Underlying Risk Factors & Recommended Interventions:</div>", unsafe_allow_html=True)
        for factor in diag["key_factors"]:
            st.markdown(f"""
            <div style="background: rgba(255, 23, 68, 0.08); border: 1px solid rgba(255, 23, 68, 0.2); border-left: 4px solid #FF1744; border-radius: 6px; padding: 0.6rem 0.9rem; margin-bottom: 0.4rem; font-size: 0.85rem; color: #F1F5F9;">
                {factor}
            </div>
            """, unsafe_allow_html=True)
        st.caption(f"Model Diagnostic Engine: {diag['model_type']}")