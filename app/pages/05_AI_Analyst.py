"""Page 5: Ask StudentIQ - Controlled AI Analyst Copilot."""

import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.agent_chat import render_agent_interface

st.set_page_config(page_title="AI Analyst | StudentIQ", page_icon="🤖", layout="wide")
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <h1 style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">AI Analyst — Ask StudentIQ</h1>
    <p style="color: #94A3B8; font-size: 0.95rem;">Ask natural language questions to analyze student retention, department comparisons, and welfare priorities.</p>
</div>
""", unsafe_allow_html=True)

# Render full interactive copilot
render_agent_interface()