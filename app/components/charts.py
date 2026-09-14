"""Reusable Plotly charts with consistent dark futuristic styling."""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

THEME_BG = "#0B0F19"
CARD_BG = "rgba(18, 24, 38, 0.7)"
ACCENT_CYAN = "#00E5FF"
ACCENT_PURPLE = "#7C4DFF"
ACCENT_GREEN = "#00E676"
ACCENT_AMBER = "#FFD600"
ACCENT_RED = "#FF1744"

RISK_COLOR_MAP = {
    "CRITICAL": "#FF1744",
    "HIGH": "#FF9100",
    "MEDIUM": "#FFD600",
    "LOW": "#00E676"
}

def apply_base_layout(fig: go.Figure, title: str = "", height: int = 380) -> go.Figure:
    """Applies common futuristic styling to Plotly figures."""
    fig.update_layout(
        title={
            "text": title,
            "font": {"size": 15, "color": "#F8FAFC", "family": "Inter, sans-serif"},
            "x": 0.02,
            "y": 0.95
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#94A3B8", "family": "Inter, sans-serif"},
        height=height,
        margin={"l": 40, "r": 25, "t": 45, "b": 40},
        legend={"orientation": "h", "y": -0.2, "font": {"size": 11}},
        xaxis={"gridcolor": "rgba(255, 255, 255, 0.06)", "zerolinecolor": "rgba(255, 255, 255, 0.1)"},
        yaxis={"gridcolor": "rgba(255, 255, 255, 0.06)", "zerolinecolor": "rgba(255, 255, 255, 0.1)"},
    )
    return fig

def plot_department_performance(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart for department average CGPA and attendance."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["department"],
        y=df["avg_cgpa"],
        name="Avg CGPA (Scale 10)",
        marker_color=ACCENT_CYAN,
        yaxis="y1"
    ))
    fig.add_trace(go.Scatter(
        x=df["department"],
        y=df["avg_attendance"],
        name="Avg Attendance %",
        marker_color=ACCENT_PURPLE,
        mode="lines+markers",
        yaxis="y2"
    ))
    fig.update_layout(
        yaxis={"title": "Average CGPA", "side": "left", "range": [0, 10]},
        yaxis2={"title": "Attendance %", "side": "right", "overlaying": "y", "range": [0, 100]},
    )
    return apply_base_layout(fig, "Department Academic & Attendance Comparison")

def plot_risk_distribution(df: pd.DataFrame) -> go.Figure:
    """Donut chart for student retention risk levels."""
    colors = [RISK_COLOR_MAP.get(str(r).upper(), "#94A3B8") for r in df["risk_level"]]
    count_col = "count" if "count" in df.columns else "student_count"
    fig = go.Figure(data=[go.Pie(
        labels=df["risk_level"],
        values=df[count_col],
        hole=0.55,
        marker={"colors": colors, "line": {"color": "#0B0F19", "width": 2}},
        textinfo="label+percent"
    )])
    return apply_base_layout(fig, "Student Retention Risk Breakdown")

def plot_attendance_vs_cgpa(df: pd.DataFrame) -> go.Figure:
    """Scatter plot illustrating correlation between attendance and CGPA."""
    fig = px.scatter(
        df,
        x="attendance",
        y="cgpa",
        color="risk_level",
        color_discrete_map=RISK_COLOR_MAP,
        hover_data=["student_id", "name", "department"],
        labels={"attendance": "Attendance (%)", "cgpa": "Cumulative GPA"}
    )
    return apply_base_layout(fig, "Attendance vs. Cumulative GPA Correlation")

def plot_cgpa_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram or bar of CGPA performance."""
    if "cgpa_bracket" in df.columns:
        fig = px.bar(
            df,
            x="cgpa_bracket",
            y="count",
            color_discrete_sequence=[ACCENT_CYAN],
            labels={"cgpa_bracket": "Grade Band", "count": "Student Count"}
        )
    else:
        fig = px.histogram(
            df,
            x="cgpa",
            nbins=20,
            color_discrete_sequence=[ACCENT_CYAN],
            labels={"cgpa": "CGPA"}
        )
    return apply_base_layout(fig, "CGPA Distribution Across Student Cohort")

def plot_horizontal_ranking(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Horizontal bar chart for top performers or department rankings."""
    fig = px.bar(
        df.sort_values(by=x_col, ascending=True),
        x=x_col,
        y=y_col,
        orientation="h",
        color=x_col,
        color_continuous_scale="Viridis",
    )
    fig.update_layout(coloraxis_showscale=False)
    return apply_base_layout(fig, title)