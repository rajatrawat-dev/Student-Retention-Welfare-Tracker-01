"""Validation logic and data quality assessment for student records."""

from typing import Any, Dict, List, Tuple
import pandas as pd
import numpy as np
from src.config.settings import settings

REQUIRED_COLUMNS = ["student_id", "name", "department", "gender", "cgpa", "attendance", "enrollment_date"]

def validate_schema(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Checks if DataFrame satisfies the canonical schema requirements."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return len(missing) == 0, missing

def check_value_ranges(df: pd.DataFrame) -> Dict[str, int]:
    """Counts out-of-bound academic indicators."""
    issues = {
        "cgpa_out_of_bounds": int(((df["cgpa"] < 0) | (df["cgpa"] > 10)).sum()) if "cgpa" in df else 0,
        "attendance_out_of_bounds": int(((df["attendance"] < 0) | (df["attendance"] > 100)).sum()) if "attendance" in df else 0,
        "invalid_departments": int((~df["department"].isin(settings.VALID_DEPARTMENTS)).sum()) if "department" in df else 0,
    }
    return issues

def detect_suspicious_records(df: pd.DataFrame) -> pd.DataFrame:
    """Flags anomalies such as extreme CGPA (>9.5) with critical attendance (<30%)."""
    suspicious_mask = pd.Series(False, index=df.index)
    
    if "cgpa" in df and "attendance" in df:
        # Extreme divergence: top-tier marks with virtually zero attendance
        mask1 = (df["cgpa"] >= 9.5) & (df["attendance"] < 30.0)
        # Suspiciously high attendance (100%) with failing CGPA (<2.5)
        mask2 = (df["attendance"] >= 98.0) & (df["cgpa"] < 2.5)
        suspicious_mask = mask1 | mask2
        
    return df[suspicious_mask]

def calculate_quality_score(metrics: Dict[str, Any]) -> float:
    """Computes an overarching Data Quality Score (0-100) based on:
    - Completeness (missing rate)
    - Uniqueness (duplicate rate)
    - Validity (range adherence)
    - Consistency (successful normalization)
    """
    rows_before = max(1, metrics.get("rows_before", 1))
    duplicates = metrics.get("duplicates_removed", 0)
    missing = metrics.get("missing_imputed", 0)
    invalid = metrics.get("invalid_values_repaired", 0)
    suspicious = metrics.get("suspicious_records_detected", 0)
    
    # Penalties
    dup_penalty = min(25.0, (duplicates / rows_before) * 100.0 * 2.0)
    missing_penalty = min(30.0, (missing / (rows_before * 7)) * 100.0 * 1.5)
    invalid_penalty = min(25.0, (invalid / rows_before) * 100.0 * 2.0)
    suspicious_penalty = min(10.0, (suspicious / rows_before) * 100.0 * 2.0)
    
    score = 100.0 - (dup_penalty + missing_penalty + invalid_penalty + suspicious_penalty)
    return max(10.0, min(100.0, round(score, 1)))
