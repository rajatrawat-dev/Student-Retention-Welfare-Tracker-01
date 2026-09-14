"""Machine learning model architecture and rule-based fallback."""

from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, f1_score
import joblib
from src.ml.features import build_preprocessor
from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger("RiskModel")

class RuleBasedRiskClassifier:
    """Transparent deterministic fallback classifier for risk assessment."""
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        preds = []
        for _, row in X.iterrows():
            cgpa = float(row.get("cgpa", 7.0))
            att = float(row.get("attendance", 75.0))
            
            # Continuous risk formula: (10 - CGPA)*6 + (100 - Attendance)*0.4
            score = (10.0 - min(10.0, max(0.0, cgpa))) * 6.0 + (100.0 - min(100.0, max(0.0, att))) * 0.4
            
            if score >= 55.0 or att < settings.ATTENDANCE_CRITICAL_THRESHOLD or cgpa < settings.CGPA_CRITICAL_THRESHOLD:
                preds.append("CRITICAL")
            elif score >= 40.0 or att < settings.ATTENDANCE_RISK_THRESHOLD or cgpa < settings.CGPA_RISK_THRESHOLD:
                preds.append("HIGH")
            elif score >= 25.0:
                preds.append("MEDIUM")
            else:
                preds.append("LOW")
        return np.array(preds)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        # Generate pseudo-probabilities based on distance to boundaries
        preds = self.predict(X)
        probs = []
        mapping = {
            "CRITICAL": [0.05, 0.10, 0.15, 0.70],
            "HIGH":     [0.10, 0.15, 0.65, 0.10],
            "MEDIUM":   [0.15, 0.65, 0.15, 0.05],
            "LOW":      [0.70, 0.20, 0.08, 0.02],
        }
        for p in preds:
            probs.append(mapping[p])
        return np.array(probs)

class StudentRiskPipeline:
    """Encapsulates ML training, evaluation, persistence, and safe fallback."""

    def __init__(self):
        self.pipeline: Optional[Pipeline] = None
        self.fallback = RuleBasedRiskClassifier()
        self.is_trained = False
        self.metrics: Dict[str, Any] = {}
        self.classes_ = np.array(["LOW", "MEDIUM", "HIGH", "CRITICAL"])

    def train(self, X_train: pd.DataFrame, y_train: pd.Series, X_test: Optional[pd.DataFrame] = None, y_test: Optional[pd.Series] = None) -> Dict[str, Any]:
        """Trains RandomForest risk classifier or flags statistical unreliability."""
        n_samples = len(X_train)
        
        # Check dataset size requirement
        if n_samples < 40 or (y_test is not None and len(y_test) < 10):
            logger.warning("Dataset too small for statistically reliable model evaluation.")
            self.metrics = {
                "status": "DATASET_TOO_SMALL",
                "message": "Dataset too small for statistically reliable model evaluation.",
                "accuracy": None,
                "f1_macro": None,
                "n_samples": n_samples,
                "using_fallback": True,
            }
            self.is_trained = True
            return self.metrics

        # Build pipeline
        preprocessor = build_preprocessor()
        clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42, class_weight="balanced")
        
        self.pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        
        self.pipeline.fit(X_train, y_train)
        self.classes_ = self.pipeline.named_steps["classifier"].classes_
        self.is_trained = True
        
        # Evaluation
        if X_test is not None and y_test is not None and len(y_test) > 0:
            y_pred = self.pipeline.predict(X_test)
            acc = round(float(accuracy_score(y_test, y_pred)), 3)
            f1 = round(float(f1_score(y_test, y_pred, average="macro", zero_division=0)), 3)
            report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
            
            self.metrics = {
                "status": "TRAINED",
                "message": "Scikit-learn RandomForest trained and evaluated successfully.",
                "accuracy": acc,
                "f1_macro": f1,
                "report": report,
                "n_train": len(X_train),
                "n_test": len(X_test),
                "using_fallback": False,
            }
        else:
            self.metrics = {
                "status": "TRAINED_NO_TEST",
                "message": "Trained on entire dataset without test split.",
                "accuracy": None,
                "n_train": len(X_train),
                "using_fallback": False,
            }
            
        logger.info(f"Model training finished: {self.metrics.get('message')}")
        return self.metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predicts risk tier, defaulting to rule-based fallback if model is untrained."""
        if self.pipeline is not None and self.is_trained:
            try:
                return self.pipeline.predict(X)
            except Exception as e:
                logger.warning(f"Pipeline prediction failed ({e}), using rule-based fallback.")
                return self.fallback.predict(X)
        return self.fallback.predict(X)

    def save(self, path = settings.MODEL_PATH):
        """Serializes model pipeline to disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"pipeline": self.pipeline, "metrics": self.metrics, "classes": self.classes_}, path)
        logger.info(f"Model persisted to {path}")

    def load(self, path = settings.MODEL_PATH) -> bool:
        """Loads serialized model pipeline if exists."""
        if not path.exists():
            logger.info("No saved model found, using rule-based engine.")
            return False
        try:
            data = joblib.load(path)
            self.pipeline = data.get("pipeline")
            self.metrics = data.get("metrics", {})
            self.classes_ = data.get("classes", np.array(["LOW", "MEDIUM", "HIGH", "CRITICAL"]))
            self.is_trained = True
            logger.info(f"Model loaded successfully from {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load model from {path}: {e}")
            return False
