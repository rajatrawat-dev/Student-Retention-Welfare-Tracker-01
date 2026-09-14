"""Sidebar navigation and live telemetry status panel."""

import streamlit as st
import requests
from src.config.settings import settings
from src.analytics.database import db_manager

def render_sidebar():
    """Renders the dark futuristic sidebar with system telemetry."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1.2rem 0.5rem; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.08);">
            <div style="font-size: 1.7rem; font-weight: 800; letter-spacing: -0.02em; background: linear-gradient(135deg, #00E5FF 0%, #7C4DFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                STUDENTIQ
            </div>
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.12em; color: #94A3B8; margin-top: 0.3rem;">
                Retention & Welfare Intelligence
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # System Health & Connectivity Telemetry
        st.markdown("<p style='font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;'>System Health</p>", unsafe_allow_html=True)
        
        # Check DuckDB
        duckdb_status = "Connected"
        try:
            db_manager.execute_query("SELECT 1;")
            st.markdown("""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.45rem 0.75rem; background: rgba(0, 229, 255, 0.05); border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 8px; margin-bottom: 0.4rem;">
                <span style="font-size: 0.8rem; color: #CBD5E1;">DuckDB Engine</span>
                <span style="font-size: 0.72rem; background: #00E5FF22; color: #00E5FF; padding: 2px 8px; border-radius: 12px; font-weight: 600;">ACTIVE</span>
            </div>
            """, unsafe_allow_html=True)
        except Exception:
            st.markdown("""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.45rem 0.75rem; background: rgba(255, 23, 68, 0.05); border: 1px solid rgba(255, 23, 68, 0.2); border-radius: 8px; margin-bottom: 0.4rem;">
                <span style="font-size: 0.8rem; color: #CBD5E1;">DuckDB Engine</span>
                <span style="font-size: 0.72rem; background: #FF174422; color: #FF1744; padding: 2px 8px; border-radius: 12px; font-weight: 600;">OFFLINE</span>
            </div>
            """, unsafe_allow_html=True)
            
        # Check ML Model
        model_ready = settings.MODEL_PATH.exists()
        model_badge = "READY" if model_ready else "FALLBACK"
        model_color = "#00E676" if model_ready else "#FFD600"
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.45rem 0.75rem; background: rgba(0, 230, 118, 0.05); border: 1px solid rgba(0, 230, 118, 0.2); border-radius: 8px; margin-bottom: 0.4rem;">
            <span style="font-size: 0.8rem; color: #CBD5E1;">ML Risk Model</span>
            <span style="font-size: 0.72rem; background: {model_color}22; color: {model_color}; padding: 2px 8px; border-radius: 12px; font-weight: 600;">{model_badge}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Check Ollama status
        ollama_online = False
        try:
            r = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=1)
            if r.status_code == 200:
                ollama_online = True
        except Exception:
            pass
            
        ollama_text = "ONLINE" if ollama_online else "RULE FALLBACK"
        ollama_color = "#7C4DFF" if ollama_online else "#94A3B8"
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.45rem 0.75rem; background: rgba(124, 77, 255, 0.05); border: 1px solid rgba(124, 77, 255, 0.2); border-radius: 8px; margin-bottom: 1.5rem;">
            <span style="font-size: 0.8rem; color: #CBD5E1;">AI Copilot LLM</span>
            <span style="font-size: 0.72rem; background: {ollama_color}22; color: {ollama_color}; padding: 2px 8px; border-radius: 12px; font-weight: 600;">{ollama_text}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.75rem; color: #64748B; line-height: 1.5;">
            <b>Track:</b> Education & EdTech<br>
            <b>Datathon:</b> TransOrg GraphIQ<br>
            <b>Theme:</b> Messy Data to Agentic Insights
        </div>
        """, unsafe_allow_html=True)