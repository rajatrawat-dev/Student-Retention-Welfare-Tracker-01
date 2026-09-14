"""Page 2: Data Quality & Data Rescue Provenance."""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.kpi_cards import render_kpi_card
from app.components.charts import apply_base_layout
from src.data.quality_report import QualityReport
from src.data.loader import load_raw_data, load_cleaned_data

st.set_page_config(page_title="Data Quality | StudentIQ", page_icon="🛡️", layout="wide")
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <h1 style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">Data Quality & Data Rescue</h1>
    <p style="color: #94A3B8; font-size: 0.95rem;">Transparent audit trail showing the 14-step normalization of noisy institutional records into canonical ground truth.</p>
</div>
""", unsafe_allow_html=True)

report = QualityReport.load()
if not report:
    st.warning("No quality report found. Please run the cleaning pipeline first: `python scripts/clean_data.py`")
    st.stop()

# Quality KPIs
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Data Quality Score", f"{report.get('data_quality_score', 0):.1f}/100", "Composite integrity benchmark", accent_color="#00E676")
with c2:
    render_kpi_card("Duplicates Dropped", f"{report.get('duplicates_removed', 0)}", "Exact and ID collision rows", accent_color="#00E5FF")
with c3:
    render_kpi_card("Missing Imputed", f"{report.get('missing_values_imputed', 0)}", "Department-median strategy", accent_color="#FFD600")
with c4:
    render_kpi_card("Anomalies Flagged", f"{report.get('suspicious_records_detected', 0)}", "Academic dissonance records", accent_color="#FF1744")

# Pipeline Funnel / Before vs After Comparison
st.subheader("Data Rescue Pipeline Transformation")
comp_df = pd.DataFrame([
    {"Stage": "Raw Input Records", "Count": report.get("rows_before", 0)},
    {"Stage": "Cleaned Validated Cohort", "Count": report.get("rows_after", 0)},
])
fig = px.bar(
    comp_df,
    x="Stage",
    y="Count",
    text="Count",
    color="Stage",
    color_discrete_sequence=["#FF1744", "#00E676"]
)
fig.update_traces(textposition="outside")
st.plotly_chart(apply_base_layout(fig, "Record Volume Funnel: Raw vs Cleaned"), use_container_width=True)

# Quality Breakdown Table
st.subheader("14-Step Normalization Audit Log")
audit_data = [
    {"Step #": "Step 1 & 2", "Operation": "Load & Column Alias Normalization", "Impact": "Unified diverse header naming to canonical schema", "Count": report.get("rows_before", 0)},
    {"Step #": "Step 3 & 4", "Operation": "Row Deduplication & ID Standardization", "Impact": "Resolved case-insensitive ID collisions into STU-XXXX", "Count": report.get("duplicates_removed", 0)},
    {"Step #": "Step 5 & 6", "Operation": "Name Casing & Department Mapping", "Impact": "Mapped slang aliases (cse, mech, ece) to canonical names", "Count": report.get("department_standardized", 0)},
    {"Step #": "Step 7", "Operation": "Gender Representation Standardization", "Impact": "Unified M/F/Other variations into clean taxonomy", "Count": report.get("gender_normalized", 0)},
    {"Step #": "Step 8", "Operation": "Attendance Representation Conversion", "Impact": "Converted fractions, % signs, strings to 0-100 float scale", "Count": report.get("attendance_normalized", 0)},
    {"Step #": "Step 9", "Operation": "CGPA Validation & Bound Enforcement", "Impact": "Repaired comma decimals and rejected out-of-bounds numbers", "Count": report.get("invalid_cgpa_fixed", 0)},
    {"Step #": "Step 10", "Operation": "Date Parsing & ISO Normalization", "Impact": "Standardized multi-format dates to YYYY-MM-DD", "Count": report.get("dates_repaired", 0)},
    {"Step #": "Step 11", "Operation": "Department Median Imputation", "Impact": "Filled missing CGPA & attendance with cohort medians", "Count": report.get("missing_values_imputed", 0)},
    {"Step #": "Step 12", "Operation": "Suspicious Outlier Detection", "Impact": "Flagged impossible academic combinations for review", "Count": report.get("suspicious_records_detected", 0)},
    {"Step #": "Step 13 & 14", "Operation": "Derived Risk Feature Engineering & Scoring", "Impact": "Generated continuous risk score and support priority", "Count": report.get("rows_after", 0)},
]
st.dataframe(pd.DataFrame(audit_data), use_container_width=True, hide_index=True)

# Interactive Inspect Raw vs Cleaned
with st.expander("Compare Raw vs Cleaned Dataset Samples"):
    t1, t2 = st.tabs(["Cleaned Canonical Data (Current)", "Raw Messy Data (Source)"])
    with t1:
        st.dataframe(load_cleaned_data().head(20), use_container_width=True)
    with t2:
        try:
            st.dataframe(load_raw_data().head(20), use_container_width=True)
        except Exception as e:
            st.info(f"Raw data preview unavailable: {e}")