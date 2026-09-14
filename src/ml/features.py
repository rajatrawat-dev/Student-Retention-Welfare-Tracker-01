"""Feature engineering and preprocessing for student retention risk."""

from typing import Tuple, List
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

NUMERICAL_FEATURES = ["cgpa", "attendance"]
CATEGORICAL_FEATURES = ["department", "gender"]

def build_preprocessor() -> ColumnTransformer:
    """Builds scikit-learn column transformer for numeric and categorical features."""
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ],
        remainder="drop"
    )

def prepare_xy(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Extracts features X and target y (risk_level) from cleaned student dataframe."""
    required_cols = NUMERICAL_FEATURES + CATEGORICAL_FEATURES + ["risk_level"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame is missing columns required for ML: {missing}")

    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES].copy()
    y = df["risk_level"].copy()
    return X, y
