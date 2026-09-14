"""Inference service for assessing student retention risk and providing explanations."""

from typing import Dict, Any, List
import pandas as pd
from src.ml.model import StudentRiskPipeline
from src.config.settings import settings

# Cached singleton
_model_instance: StudentRiskPipeline = None

def get_risk_model() -> StudentRiskPipeline:
    global _model_instance
    if _model_instance is None:
        _model_instance = StudentRiskPipeline()
        _model_instance.load(settings.MODEL_PATH)
    return _model_instance

def predict_single_student(student_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Generates risk prediction and academic explanation for a single student.
    Note: Clearly framed as academic support intelligence, NOT a medical/psychological diagnosis.
    """
    model = get_risk_model()
    df_single = pd.DataFrame([student_dict])
    
    pred_level = model.predict(df_single)[0]
    
    cgpa = float(student_dict.get("cgpa", 7.0))
    attendance = float(student_dict.get("attendance", 75.0))
    dept = student_dict.get("department", "Unknown")
    
    # Generate transparent explanation factors
    factors: List[str] = []
    if attendance < settings.ATTENDANCE_CRITICAL_THRESHOLD:
        factors.append(f"Critical attendance ({attendance}% < {settings.ATTENDANCE_CRITICAL_THRESHOLD}%) poses severe retention risk.")
    elif attendance < settings.ATTENDANCE_RISK_THRESHOLD:
        factors.append(f"Low attendance ({attendance}% < {settings.ATTENDANCE_RISK_THRESHOLD}%) requires early attendance warning.")
        
    if cgpa < settings.CGPA_CRITICAL_THRESHOLD:
        factors.append(f"Critical CGPA ({cgpa} < {settings.CGPA_CRITICAL_THRESHOLD}) triggers mandatory academic remedial intervention.")
    elif cgpa < settings.CGPA_RISK_THRESHOLD:
        factors.append(f"Marginal CGPA ({cgpa} < {settings.CGPA_RISK_THRESHOLD}) warrants targeted tutoring support.")
        
    if not factors:
        factors.append("Academic progress and attendance adhere to standard institutional benchmarks.")
        
    priority_map = {
        "CRITICAL": "Immediate Intervention",
        "HIGH": "Advisory",
        "MEDIUM": "Monitor",
        "LOW": "Routine"
    }
    
    return {
        "student_id": student_dict.get("student_id", "Unknown"),
        "predicted_risk_level": pred_level,
        "support_priority": priority_map.get(pred_level, "Routine"),
        "key_factors": factors,
        "disclaimer": "Academic-support analytics indicator only. Not a medical or psychological diagnosis.",
        "model_type": "Scikit-Learn Random Forest" if (model.pipeline and not model.metrics.get("using_fallback")) else "Rule-Based Academic Risk Engine"
    }
