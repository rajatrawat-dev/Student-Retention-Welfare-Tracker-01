"""Builds the DuckDB analytical database from cleaned student records."""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import settings
from src.analytics.database import db_manager
from src.data.loader import load_cleaned_data

def build_analytics_db():
    print("==================================================")
    print("      STUDENTIQ -- DUCKDB ANALYTICS BUILDER       ")
    print("==================================================")
    
    cleaned_df = load_cleaned_data()
    db_manager.init_database(cleaned_df)
    
    # Verify tables and row counts
    count_df = db_manager.execute_query("SELECT COUNT(*) as count FROM students;")
    dept_df = db_manager.execute_query("SELECT COUNT(*) as depts FROM department_summary;")
    
    print(f"Successfully populated DuckDB at: {settings.DUCKDB_PATH}")
    print(f"Verified Records in students:     {count_df.iloc[0]['count']}")
    print(f"Verified Analytical Views:        department_summary ({dept_df.iloc[0]['depts']} depts), risk_summary")
    print("==================================================")

if __name__ == "__main__":
    build_analytics_db()