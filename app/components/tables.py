"""Styled tables and risk badges."""

import streamlit as st
import pandas as pd

def render_risk_badge(level: str) -> str:
    """Generates an HTML badge for risk tier."""
    colors = {
        "CRITICAL": ("#FF1744", "rgba(255, 23, 68, 0.15)"),
        "HIGH": ("#FF9100", "rgba(255, 145, 0, 0.15)"),
        "MEDIUM": ("#FFD600", "rgba(255, 214, 0, 0.15)"),
        "LOW": ("#00E676", "rgba(0, 230, 118, 0.15)"),
    }
    fg, bg = colors.get(str(level).upper(), ("#94A3B8", "rgba(148, 163, 184, 0.15)"))
    return f"""<span style="background-color: {bg}; color: {fg}; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; border: 1px solid {fg}44;">{level}</span>"""

def render_styled_dataframe(df: pd.DataFrame, height: int = 400):
    """Renders an interactive and responsive dataframe with theme styling."""
    st.dataframe(
        df,
        use_container_width=True,
        height=height,
        hide_index=True
    )