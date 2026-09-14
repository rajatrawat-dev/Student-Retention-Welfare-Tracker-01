"""Interactive AI Analyst copilot component."""

import streamlit as st
import plotly.express as px
from src.agent.agent import student_iq_analyst
from app.components.charts import apply_base_layout, RISK_COLOR_MAP

def render_agent_interface():
    """Renders the Ask StudentIQ conversational copilot."""
    st.markdown("""
    <div style="background: rgba(124, 77, 255, 0.05); border: 1px solid rgba(124, 77, 255, 0.2); border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem;">
        <h3 style="color: #F8FAFC; margin: 0 0 0.4rem 0; font-size: 1.25rem;">Ask StudentIQ Copilot</h3>
        <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">
            Controlled analytical assistant executing schema-validated DuckDB queries with automated chart synthesis.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Suggested Demo Questions
    st.markdown("<p style='font-size: 0.8rem; font-weight: 600; color: #64748B;'>Suggested Analytical Prompts:</p>", unsafe_allow_html=True)
    cols = st.columns(4)
    q1 = cols[0].button("Attendance < 60%", use_container_width=True)
    q2 = cols[1].button("Lowest CGPA Depts", use_container_width=True)
    q3 = cols[2].button("Attendance vs CGPA", use_container_width=True)
    q4 = cols[3].button("Top 10 Performers", use_container_width=True)
    
    user_query = ""
    if q1:
        user_query = "Show students with attendance below 60%."
    elif q2:
        user_query = "Which departments have the lowest average CGPA?"
    elif q3:
        user_query = "Show the relationship between attendance and CGPA."
    elif q4:
        user_query = "Show top 10 students by CGPA."
        
    custom_input = st.text_input("Enter your question:", value=user_query, placeholder="e.g., Which students are at high risk?")
    
    submit = st.button("Analyze Query", type="primary", use_container_width=True)
    
    if (submit or user_query) and custom_input.strip():
        with st.spinner("Processing natural language query through safety and DuckDB layer..."):
            response = student_iq_analyst.ask(custom_input)
            
            # Status and telemetry badge
            engine_badge = f"<span style='background: #7C4DFF22; color: #7C4DFF; padding: 3px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 600;'>{response.engine_used}</span>"
            safety_badge = "<span style='background: #00E67622; color: #00E676; padding: 3px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 600;'>SAFE SELECT</span>" if response.is_safe else "<span style='background: #FF174422; color: #FF1744; padding: 3px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 600;'>REJECTED</span>"
            
            st.markdown(f"""
            <div style="display: flex; gap: 0.75rem; margin-top: 1rem; margin-bottom: 0.75rem;">
                {engine_badge}
                {safety_badge}
                <span style='background: #00E5FF22; color: #00E5FF; padding: 3px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 600;'>Intent: {response.intent}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # SQL Code block inside expander
            with st.expander("Generated DuckDB SQL (Click to inspect)", expanded=False):
                st.code(response.sql, language="sql")
                
            # Narrative Explanation
            st.info(response.explanation)
            
            # Result Visualization / Table
            if response.data is not None and not response.data.empty:
                df = response.data
                
                # Render chart if applicable
                if response.chart_type == "scatter" and "attendance" in df.columns and "cgpa" in df.columns:
                    fig = px.scatter(df, x="attendance", y="cgpa", color="risk_level" if "risk_level" in df.columns else None, color_discrete_map=RISK_COLOR_MAP)
                    st.plotly_chart(apply_base_layout(fig, "Attendance vs CGPA Distribution"), use_container_width=True)
                elif response.chart_type == "horizontal_bar" and "name" in df.columns and "cgpa" in df.columns:
                    fig = px.bar(df.sort_values(by="cgpa", ascending=True), x="cgpa", y="name", orientation="h", color="cgpa")
                    st.plotly_chart(apply_base_layout(fig, "Top Student Performers"), use_container_width=True)
                elif response.chart_type == "bar" and "department" in df.columns:
                    val_col = "avg_cgpa" if "avg_cgpa" in df.columns else "student_count" if "student_count" in df.columns else df.columns[1]
                    fig = px.bar(df, x="department", y=val_col, color=val_col)
                    st.plotly_chart(apply_base_layout(fig, f"Department Breakdown ({val_col})"), use_container_width=True)
                elif response.chart_type == "donut" and "risk_level" in df.columns:
                    count_col = "student_count" if "student_count" in df.columns else "percentage" if "percentage" in df.columns else df.columns[1]
                    fig = px.pie(df, names="risk_level", values=count_col, hole=0.5)
                    st.plotly_chart(apply_base_layout(fig, "Risk Distribution"), use_container_width=True)
                    
                # Render Data Table
                st.dataframe(df, use_container_width=True, hide_index=True)
            elif response.is_safe and response.execution_success:
                st.warning("Query executed successfully, but returned zero records.")