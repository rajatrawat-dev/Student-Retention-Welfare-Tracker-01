"""Utility helper functions for data formatting and serializing."""

import json
from typing import Any
import numpy as np
import pandas as pd

class SafeJSONEncoder(json.JSONEncoder):
    """Encodes NumPy, Pandas, and Path objects safely into JSON."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (pd.Timestamp, pd.DatetimeIndex)):
            return obj.isoformat()
        if hasattr(obj, "__fspath__"):
            return str(obj)
        return super().default(obj)

def safe_json_dumps(data: Any, indent: int = 2) -> str:
    """Serializes data to a JSON string using SafeJSONEncoder."""
    return json.dumps(data, cls=SafeJSONEncoder, indent=indent)

def safe_round(value: Any, decimals: int = 2) -> float:
    """Safely rounds float values, returning 0.0 for invalid/null input."""
    try:
        if pd.isna(value) or value is None:
            return 0.0
        return round(float(value), decimals)
    except (ValueError, TypeError):
        return 0.0

def format_percentage(value: Any) -> str:
    """Formats a numeric value as a clean percentage string."""
    rounded = safe_round(value, 1)
    return f"{rounded:.1f}%"
