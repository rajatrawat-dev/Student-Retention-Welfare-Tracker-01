"""Chart recommendation engine based on analytical intent and data topology."""

from typing import Dict, Any, Optional
import pandas as pd

def recommend_chart_type(intent: str, df: pd.DataFrame) -> str:
    """Selects the most suitable Plotly visualization type:
    - Comparison -> 'bar'
    - Trend / Time -> 'line'
    - Continuous Distribution -> 'histogram'
    - Numeric Relationship -> 'scatter'
    - Ranking -> 'horizontal_bar'
    - Composition / Proportion -> 'donut'
    - Single Scalar -> 'kpi_card'
    - Tabular Detail -> 'table'
    """
    if df.empty:
        return "table"
        
    num_rows, num_cols = df.shape
    
    if num_rows == 1 and num_cols <= 3:
        return "kpi_card"
        
    if intent == "CORRELATION_QUERY" or ("attendance" in df.columns and "cgpa" in df.columns and num_rows > 10):
        return "scatter"
        
    if intent == "TOP_PERFORMERS" or (num_rows <= 15 and "name" in df.columns and "cgpa" in df.columns):
        return "horizontal_bar"
        
    if intent == "DISTRIBUTION_QUERY" or (num_cols == 1 and pd.api.types.is_numeric_dtype(df.iloc[:, 0])):
        return "histogram"
        
    if "risk_level" in df.columns and ("count" in df.columns or "student_count" in df.columns):
        return "donut"
        
    if "department" in df.columns and any("avg" in c or "count" in c for c in df.columns):
        return "bar"
        
    if num_cols >= 4:
        return "table"
        
    return "bar"
