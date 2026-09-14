"""Structures and generates comprehensive Data Rescue Quality Reports."""

import json
from pathlib import Path
from typing import Any, Dict
from src.config.settings import settings
from src.utils.helpers import safe_json_dumps
from src.utils.logging import get_logger

logger = get_logger("QualityReport")

class QualityReport:
    """Encapsulates metrics collected during the 14-step Data Rescue process."""
    
    def __init__(self):
        self.rows_before = 0
        self.rows_after = 0
        self.duplicates_removed = 0
        self.duplicate_ids_resolved = 0
        self.missing_values_before = 0
        self.missing_values_imputed = 0
        self.invalid_cgpa_fixed = 0
        self.attendance_normalized = 0
        self.department_standardized = 0
        self.gender_normalized = 0
        self.dates_repaired = 0
        self.suspicious_records_detected = 0
        self.cleaning_success_rate = 100.0
        self.data_quality_score = 0.0
        self.issues_log = []
        self.column_summary = {}

    def add_issue(self, step: str, description: str, count: int = 1):
        self.issues_log.append({
            "step": step,
            "description": description,
            "count": count
        })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rows_before": self.rows_before,
            "rows_after": self.rows_after,
            "duplicates_removed": self.duplicates_removed,
            "duplicate_ids_resolved": self.duplicate_ids_resolved,
            "missing_values_before": self.missing_values_before,
            "missing_values_imputed": self.missing_values_imputed,
            "invalid_values_repaired": self.invalid_cgpa_fixed + self.dates_repaired,
            "invalid_cgpa_fixed": self.invalid_cgpa_fixed,
            "attendance_normalized": self.attendance_normalized,
            "department_standardized": self.department_standardized,
            "gender_normalized": self.gender_normalized,
            "dates_repaired": self.dates_repaired,
            "suspicious_records_detected": self.suspicious_records_detected,
            "cleaning_success_rate": round(self.cleaning_success_rate, 2),
            "data_quality_score": round(self.data_quality_score, 1),
            "column_summary": self.column_summary,
            "issues_log": self.issues_log,
        }

    def save(self, file_path: Path = settings.QUALITY_REPORT_PATH):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(safe_json_dumps(self.to_dict()), encoding="utf-8")
        logger.info(f"Saved quality report to {file_path}")

    @classmethod
    def load(cls, file_path: Path = settings.QUALITY_REPORT_PATH) -> Dict[str, Any]:
        if not file_path.exists():
            return {}
        try:
            return json.loads(file_path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed to load quality report: {e}")
            return {}
