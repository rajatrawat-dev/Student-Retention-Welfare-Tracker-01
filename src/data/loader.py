"""Data loader for raw and processed datasets."""

from pathlib import Path
from typing import Optional
import pandas as pd
from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger("DataLoader")

def load_raw_data(file_path: Optional[Path] = None) -> pd.DataFrame:
    """Loads raw messy student CSV with tolerant encoding."""
    path = file_path or settings.RAW_DATA_PATH
    if not path.exists():
        logger.warning(f"Raw data file not found at {path}")
        raise FileNotFoundError(f"Raw data file not found at: {path}")
        
    try:
        # Load with fallback encodings
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin1")
        
    logger.info(f"Loaded raw dataset from {path} with {len(df)} rows and {len(df.columns)} columns.")
    return df

def load_cleaned_data(file_path: Optional[Path] = None) -> pd.DataFrame:
    """Loads canonical cleaned student data."""
    path = file_path or settings.CLEANED_DATA_PATH
    if not path.exists():
        logger.warning(f"Cleaned data file not found at {path}")
        raise FileNotFoundError(f"Cleaned dataset not found at: {path}. Run cleaning pipeline first.")
        
    df = pd.read_csv(path, encoding="utf-8")
    logger.info(f"Loaded cleaned dataset with {len(df)} records.")
    return df

def save_cleaned_data(df: pd.DataFrame, file_path: Optional[Path] = None) -> Path:
    """Saves standardized DataFrame to target CSV."""
    path = file_path or settings.CLEANED_DATA_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
    logger.info(f"Successfully saved cleaned dataset to {path}")
    return path
