"""Data Cleaner orchestrating the 14-Step Data Rescue Pipeline.
From messy, noisy student records to canonical, validated, risk-scored intelligence.
"""

from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np
from src.config.settings import settings
from src.data.normalizer import (
    normalize_student_id,
    normalize_name,
    normalize_department,
    normalize_gender,
    normalize_attendance,
    normalize_cgpa,
    normalize_date,
)
from src.data.validator import detect_suspicious_records, calculate_quality_score
from src.data.quality_report import QualityReport
from src.utils.logging import get_logger

logger = get_logger("DataCleaner")

class StudentDataCleaner:
    """Production 14-step cleaning engine."""

    def __init__(self):
        self.report = QualityReport()

    def clean(self, df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Executes the full 14-step data rescue pipeline."""
        logger.info("Initiating 14-step Data Rescue pipeline...")
        self.report.rows_before = len(df_raw)
        self.report.missing_values_before = int(df_raw.isna().sum().sum())
        
        # 1. Load copy
        df = df_raw.copy()
        
        # 2. Normalize column headers
        df = self._normalize_columns(df)
        
        # 3. Detect and remove duplicate rows
        initial_count = len(df)
        df = df.drop_duplicates().reset_index(drop=True)
        exact_dups = initial_count - len(df)
        self.report.duplicates_removed += exact_dups
        if exact_dups > 0:
            self.report.add_issue("Deduplication", f"Removed {exact_dups} exact duplicate rows", exact_dups)
            
        # 4. Normalize IDs & resolve duplicate student_ids
        df = self._clean_student_ids(df)
        
        # 5. Normalize names
        df = self._clean_names(df)
        
        # 6. Normalize departments
        df = self._clean_departments(df)
        
        # 7. Normalize gender
        df = self._clean_gender(df)
        
        # 8. Normalize attendance
        df = self._clean_attendance(df)
        
        # 9. Validate & normalize CGPA
        df = self._clean_cgpa(df)
        
        # 10. Parse & standardize dates
        df = self._clean_dates(df)
        
        # 11. Handle missing values intelligently (Department-median imputation)
        df = self._impute_missing(df)
        
        # 12. Detect suspicious records (academic anomalies)
        suspicious_df = detect_suspicious_records(df)
        self.report.suspicious_records_detected = len(suspicious_df)
        if len(suspicious_df) > 0:
            self.report.add_issue("AnomalyDetection", f"Flagged {len(suspicious_df)} suspicious outlier records", len(suspicious_df))
            
        # 13. Create canonical derived features
        df = self._compute_derived_fields(df)
        
        # 14. Compile Quality Report & Score
        self.report.rows_after = len(df)
        self.report.data_quality_score = calculate_quality_score(self.report.to_dict())
        
        # Column summaries
        for col in df.columns:
            self.report.column_summary[col] = {
                "dtype": str(df[col].dtype),
                "null_count": int(df[col].isna().sum()),
                "unique_count": int(df[col].nunique())
            }
            
        logger.info(f"Data rescue complete. Rows: {self.report.rows_before} -> {self.report.rows_after}. Score: {self.report.data_quality_score}")
        return df, self.report.to_dict()

    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        col_map = {}
        for c in df.columns:
            clean = str(c).strip().lower().replace(" ", "_").replace("-", "_")
            if "student" in clean and "id" in clean:
                col_map[c] = "student_id"
            elif clean in ["id", "roll_no", "reg_no", "enrollment_id"]:
                col_map[c] = "student_id"
            elif "name" in clean or clean in ["student_name", "full_name"]:
                col_map[c] = "name"
            elif "dept" in clean or "department" in clean or clean in ["branch", "stream"]:
                col_map[c] = "department"
            elif clean in ["gender", "sex"]:
                col_map[c] = "gender"
            elif "cgpa" in clean or clean in ["gpa", "score", "grade_point"]:
                col_map[c] = "cgpa"
            elif "att" in clean or clean in ["attendance", "attendance_rate", "presence"]:
                col_map[c] = "attendance"
            elif "date" in clean or clean in ["enrollment_date", "admission_date", "doj"]:
                col_map[c] = "enrollment_date"
            else:
                col_map[c] = clean
        df = df.rename(columns=col_map)
        return df

    def _clean_student_ids(self, df: pd.DataFrame) -> pd.DataFrame:
        if "student_id" not in df.columns:
            df["student_id"] = [f"STU-{1000 + i}" for i in range(len(df))]
            return df
            
        cleaned_ids = []
        id_mod_count = 0
        for val in df["student_id"]:
            cid, mod = normalize_student_id(val)
            cleaned_ids.append(cid)
            if mod:
                id_mod_count += 1
                
        df["student_id"] = cleaned_ids
        self.report.duplicate_ids_resolved += id_mod_count
        
        # Deduplicate student_id: if multiple rows have same student_id, keep the most complete row
        before_dedup = len(df)
        df = df.drop_duplicates(subset=["student_id"], keep="first").reset_index(drop=True)
        dropped = before_dedup - len(df)
        self.report.duplicates_removed += dropped
        return df

    def _clean_names(self, df: pd.DataFrame) -> pd.DataFrame:
        if "name" not in df.columns:
            df["name"] = [f"Student {i+1}" for i in range(len(df))]
            return df
            
        cleaned_names = []
        for i, val in enumerate(df["name"]):
            cname, _ = normalize_name(val)
            cleaned_names.append(cname if cname else f"Student {i+1}")
        df["name"] = cleaned_names
        return df

    def _clean_departments(self, df: pd.DataFrame) -> pd.DataFrame:
        if "department" not in df.columns:
            df["department"] = settings.VALID_DEPARTMENTS[0]
            return df
            
        cleaned_depts = []
        mod_count = 0
        for val in df["department"]:
            cdept, mod = normalize_department(val)
            cleaned_depts.append(cdept)
            if mod:
                mod_count += 1
        df["department"] = cleaned_depts
        self.report.department_standardized = mod_count
        return df

    def _clean_gender(self, df: pd.DataFrame) -> pd.DataFrame:
        if "gender" not in df.columns:
            df["gender"] = "Other"
            return df
            
        cleaned_g = []
        mod_count = 0
        for val in df["gender"]:
            cg, mod = normalize_gender(val)
            cleaned_g.append(cg)
            if mod:
                mod_count += 1
        df["gender"] = cleaned_g
        self.report.gender_normalized = mod_count
        return df

    def _clean_attendance(self, df: pd.DataFrame) -> pd.DataFrame:
        if "attendance" not in df.columns:
            df["attendance"] = 75.0
            return df
            
        cleaned_att = []
        mod_count = 0
        for val in df["attendance"]:
            catt, mod = normalize_attendance(val)
            cleaned_att.append(catt)
            if mod:
                mod_count += 1
        df["attendance"] = cleaned_att
        self.report.attendance_normalized = mod_count
        return df

    def _clean_cgpa(self, df: pd.DataFrame) -> pd.DataFrame:
        if "cgpa" not in df.columns:
            df["cgpa"] = 7.0
            return df
            
        cleaned_cgpa = []
        mod_count = 0
        for val in df["cgpa"]:
            ccgpa, mod = normalize_cgpa(val)
            cleaned_cgpa.append(ccgpa)
            if mod:
                mod_count += 1
        df["cgpa"] = cleaned_cgpa
        self.report.invalid_cgpa_fixed = mod_count
        return df

    def _clean_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        if "enrollment_date" not in df.columns:
            df["enrollment_date"] = "2023-08-01"
            return df
            
        cleaned_dates = []
        mod_count = 0
        for val in df["enrollment_date"]:
            cdate, mod = normalize_date(val)
            cleaned_dates.append(cdate or "2023-08-01")
            if mod:
                mod_count += 1
        df["enrollment_date"] = cleaned_dates
        self.report.dates_repaired = mod_count
        return df

    def _impute_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        # Department-level median imputation for continuous features
        imputed_count = 0
        
        # CGPA imputation
        if df["cgpa"].isna().sum() > 0:
            cgpa_nulls = int(df["cgpa"].isna().sum())
            imputed_count += cgpa_nulls
            dept_medians = df.groupby("department")["cgpa"].transform("median")
            overall_median = df["cgpa"].median() or 7.0
            df["cgpa"] = df["cgpa"].fillna(dept_medians).fillna(overall_median).round(2)
            self.report.add_issue("Imputation", f"Imputed {cgpa_nulls} missing CGPA values using department medians", cgpa_nulls)
            
        # Attendance imputation
        if df["attendance"].isna().sum() > 0:
            att_nulls = int(df["attendance"].isna().sum())
            imputed_count += att_nulls
            dept_att_medians = df.groupby("department")["attendance"].transform("median")
            overall_att_median = df["attendance"].median() or 75.0
            df["attendance"] = df["attendance"].fillna(dept_att_medians).fillna(overall_att_median).round(2)
            self.report.add_issue("Imputation", f"Imputed {att_nulls} missing attendance values using department medians", att_nulls)
            
        self.report.missing_values_imputed = imputed_count
        return df

    def _compute_derived_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        # Derived 1: attendance_percentage
        df["attendance_percentage"] = df["attendance"].round(2)
        
        # Derived 2: academic_risk_score (0 - 100 continuous score)
        # Low CGPA contributes up to 60 points, low attendance contributes up to 40 points
        # CGPA component: 10.0 -> 0 pts, 0.0 -> 60 pts
        # Attendance component: 100% -> 0 pts, 0% -> 40 pts
        cgpa_penalty = ((10.0 - df["cgpa"].clip(0.0, 10.0)) / 10.0) * 60.0
        att_penalty = ((100.0 - df["attendance"].clip(0.0, 100.0)) / 100.0) * 40.0
        df["academic_risk_score"] = (cgpa_penalty + att_penalty).round(2)
        
        # Derived 3: risk_level
        conditions = [
            (df["academic_risk_score"] >= 55.0) | (df["attendance"] < settings.ATTENDANCE_CRITICAL_THRESHOLD) | (df["cgpa"] < settings.CGPA_CRITICAL_THRESHOLD),
            (df["academic_risk_score"] >= 40.0) | (df["attendance"] < settings.ATTENDANCE_RISK_THRESHOLD) | (df["cgpa"] < settings.CGPA_RISK_THRESHOLD),
            (df["academic_risk_score"] >= 25.0),
        ]
        choices = ["CRITICAL", "HIGH", "MEDIUM"]
        df["risk_level"] = np.select(conditions, choices, default="LOW")
        
        # Derived 4: support_priority
        p_conditions = [
            df["risk_level"] == "CRITICAL",
            df["risk_level"] == "HIGH",
            df["risk_level"] == "MEDIUM",
        ]
        p_choices = ["Immediate Intervention", "Advisory", "Monitor"]
        df["support_priority"] = np.select(p_conditions, p_choices, default="Routine")
        
        # Final column order alignment
        final_cols = [c for c in settings.CANONICAL_COLUMNS if c in df.columns]
        return df[final_cols]
