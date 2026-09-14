"""Executes the 14-Step Data Rescue Pipeline from CLI."""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_raw_data, save_cleaned_data
from src.data.cleaner import StudentDataCleaner
from src.data.quality_report import QualityReport
from src.config.settings import settings

def run_clean_pipeline():
    print("==================================================")
    print("      STUDENTIQ -- DATA RESCUE PIPELINE           ")
    print("==================================================")
    
    raw_df = load_raw_data()
    cleaner = StudentDataCleaner()
    cleaned_df, report = cleaner.clean(raw_df)
    
    # Save cleaned data
    save_cleaned_data(cleaned_df)
    
    # Save quality report
    cleaner.report.save()
    
    print("")
    print("--- DATA RESCUE QUALITY REPORT ---")
    print(f"Rows Before:               {report['rows_before']}")
    print(f"Rows After:                {report['rows_after']}")
    print(f"Duplicates Removed:        {report['duplicates_removed']}")
    print(f"Missing Values Imputed:    {report['missing_values_imputed']}")
    print(f"Invalid CGPA Repaired:     {report['invalid_cgpa_fixed']}")
    print(f"Attendance Converted:      {report['attendance_normalized']}")
    print(f"Departments Standardized:  {report['department_standardized']}")
    print(f"Suspicious Records:        {report['suspicious_records_detected']}")
    print(f"Data Quality Score:        {report['data_quality_score']}/100")
    print("==================================================")
    print(f"Cleaned dataset saved to: {settings.CLEANED_DATA_PATH}")
    print(f"Quality report saved to:  {settings.QUALITY_REPORT_PATH}")
    print("==================================================")

if __name__ == "__main__":
    run_clean_pipeline()