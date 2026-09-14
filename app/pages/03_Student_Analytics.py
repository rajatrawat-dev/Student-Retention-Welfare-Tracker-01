"""Page 3: Student Analytics - Deep Interactive Directory & Filtering."""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.tables import render_styled_dataframe
from src.analytics.queries import filter_students, get_top_performers, get_students_requiring_support
from src.config.settings import settings

st.set_page_config(page_title="Student Analytics | StudentIQ", page_icon="🎓", layout="wide")
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <h1 style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">Student Analytics & Directory</h1>
    <p style="color: #94A3B8; font-size: 0.95rem;">Multi-criteria filtering, student cohort exploration, top performers, and exportable intelligence.</p>
</div>
""", unsafe_allow_html=True)

# Tabs for Explorer vs Specialized Cohorts
tab1, tab2, tab3 = st.tabs(["Search & Multi-Filter Directory", "Top Academic Performers", "Immediate Support Queue"])

with tab1:
    # Filter Controls
    with st.expander("Filter & Search Controls", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            selected_dept = st.selectbox("Department", ["All"] + list(settings.VALID_DEPARTMENTS))
            search_query = st.text_input("Search Name or Student ID", placeholder="e.g. STU-1005 or Sharma")
        with f2:
            selected_gender = st.selectbox("Gender", ["All", "Male", "Female", "Other"])
            selected_risk = st.selectbox("Risk Level", ["All"] + list(settings.RISK_LEVELS))
        with f3:
            cgpa_range = st.slider("CGPA Range", 0.0, 10.0, (0.0, 10.0), 0.1)
            att_range = st.slider("Attendance % Range", 0.0, 100.0, (0.0, 100.0), 1.0)

    # Fetch Filtered Data
    filtered_df = filter_students(
        department=selected_dept if selected_dept != "All" else None,
        gender=selected_gender if selected_gender != "All" else None,
        min_cgpa=cgpa_range[0],
        max_cgpa=cgpa_range[1],
        min_attendance=att_range[0],
        max_attendance=att_range[1],
        risk_level=selected_risk if selected_risk != "All" else None,
        search_term=search_query if search_query.strip() else None,
        limit=500
    )

    st.markdown(f"**Showing {len(filtered_df)} student records** matching active filters.")
    render_styled_dataframe(filtered_df, height=450)

    # CSV Download Button
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Cohort as CSV",
        data=csv_bytes,
        file_name="studentiq_filtered_cohort.csv",
        mime="text/csv",
        type="primary"
    )

with tab2:
    st.subheader("Top 15 Academic Performers by Cumulative GPA")
    top_df = get_top_performers(15)
    render_styled_dataframe(top_df, height=400)

with tab3:
    st.subheader("Students Requiring Support (Priority Welfare Queue)")
    support_df = get_students_requiring_support(25)
    render_styled_dataframe(support_df, height=400)