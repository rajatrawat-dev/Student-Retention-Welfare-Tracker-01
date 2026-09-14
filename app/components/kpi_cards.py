"""Reusable futuristic glassmorphism KPI cards."""

import streamlit as st
from typing import Optional

def render_kpi_card(
    title: str, 
    value: str, 
    subtitle: str = "", 
    delta: Optional[str] = None, 
    delta_color: str = "normal", 
    accent_color: str = "#00E5FF"
):
    """Renders a modern glassmorphic KPI card with glowing accent."""
    delta_html = ""
    if delta:
        d_color = "#00E676" if delta_color == "positive" else "#FF1744" if delta_color == "negative" else "#94A3B8"
        delta_html = f"<div style='font-size: 0.78rem; font-weight: 600; color: {d_color}; margin-top: 0.35rem;'>{delta}</div>"
        
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, rgba(18, 24, 38, 0.8) 0%, rgba(13, 17, 27, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 2px solid {accent_color};
        border-radius: 12px;
        padding: 1.25rem 1.1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    ">
        <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94A3B8;">
            {title}
        </div>
        <div style="font-size: 1.95rem; font-weight: 800; color: #F8FAFC; margin-top: 0.4rem; letter-spacing: -0.02em;">
            {value}
        </div>
        {delta_html}
        <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.25rem;">
            {subtitle}
        </div>
    </div>
    """, unsafe_allow_html=True)