"""Central configuration for StudentIQ.
Uses pathlib for absolute portability across Windows, Linux, and macOS.
"""

from dataclasses import dataclass
from pathlib import Path
import os
from typing import List

# Determine Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

@dataclass(frozen=True)
class Settings:
    # Project Paths
    ROOT_DIR: Path = PROJECT_ROOT
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_PATH: Path = PROJECT_ROOT / "data" / "raw" / "messy_students.csv"
    CLEANED_DATA_PATH: Path = PROJECT_ROOT / "data" / "processed" / "cleaned_students.csv"
    DUCKDB_PATH: Path = PROJECT_ROOT / "data" / "processed" / "analytics.duckdb"
    MODEL_PATH: Path = PROJECT_ROOT / "data" / "processed" / "risk_model.joblib"
    QUALITY_REPORT_PATH: Path = PROJECT_ROOT / "data" / "processed" / "quality_report.json"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"

    # Canonical Schema
    CANONICAL_COLUMNS: List[str] = (
        "student_id",
        "name",
        "department",
        "gender",
        "cgpa",
        "attendance",
        "enrollment_date",
        "attendance_percentage",
        "academic_risk_score",
        "risk_level",
        "support_priority",
    )

    # Risk & Evaluation Thresholds
    ATTENDANCE_RISK_THRESHOLD: float = float(os.getenv("ATTENDANCE_RISK_THRESHOLD", "75.0"))
    ATTENDANCE_CRITICAL_THRESHOLD: float = float(os.getenv("ATTENDANCE_CRITICAL_THRESHOLD", "60.0"))
    CGPA_RISK_THRESHOLD: float = float(os.getenv("CGPA_RISK_THRESHOLD", "6.0"))
    CGPA_CRITICAL_THRESHOLD: float = float(os.getenv("CGPA_CRITICAL_THRESHOLD", "4.5"))

    # Canonical Department Names
    VALID_DEPARTMENTS: List[str] = (
        "Computer Science & Engineering",
        "Electronics & Communication Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Information Technology",
        "Electrical Engineering",
    )

    # Risk Levels
    RISK_LEVELS: List[str] = ("LOW", "MEDIUM", "HIGH", "CRITICAL")
    SUPPORT_PRIORITIES: List[str] = ("Routine", "Monitor", "Advisory", "Immediate Intervention")

    # Ollama Settings
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_TIMEOUT_SECONDS: int = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "5"))

    # App Environment
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
