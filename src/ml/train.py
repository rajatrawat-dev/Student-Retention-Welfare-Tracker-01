"""Trains and evaluates the Student Retention Risk Machine Learning Model."""

from typing import Dict, Any
import pandas as pd
from sklearn.model_selection import train_test_split
from src.config.settings import settings
from src.data.loader import load_cleaned_data
from src.ml.features import prepare_xy
from src.ml.model import StudentRiskPipeline
from src.utils.logging import get_logger

logger = get_logger("TrainModel")

def train_and_save_model() -> Dict[str, Any]:
    """Orchestrates end-to-end training and artifact saving."""
    logger.info("Loading cleaned student dataset for ML training...")
    df = load_cleaned_data()
    
    X, y = prepare_xy(df)
    
    # Split stratified by risk level if sufficient samples
    min_class_count = y.value_counts().min()
    if min_class_count >= 2 and len(df) >= 30:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        X_train, X_test, y_train, y_test = X, None, y, None

    model_pipeline = StudentRiskPipeline()
    metrics = model_pipeline.train(X_train, y_train, X_test, y_test)
    model_pipeline.save(settings.MODEL_PATH)
    
    return metrics

if __name__ == "__main__":
    results = train_and_save_model()
    print("Training Results:", results)
