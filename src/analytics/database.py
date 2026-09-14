"""DuckDB database connection manager and schema initialization."""

import duckdb
from pathlib import Path
from typing import Optional, Any
import pandas as pd
from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger("DatabaseManager")

class DatabaseManager:
    """Manages embedded DuckDB analytical database."""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or settings.DUCKDB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = None

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        """Returns active DuckDB connection."""
        if self._conn is None:
            # Connect in read-write mode or in-memory if file lock occurs
            try:
                self._conn = duckdb.connect(database=str(self.db_path), read_only=False)
            except Exception as e:
                logger.warning(f"Could not open file-based DuckDB ({e}), falling back to in-memory.")
                self._conn = duckdb.connect(database=":memory:")
        return self._conn

    def init_database(self, df: Optional[pd.DataFrame] = None) -> None:
        """Initializes tables and analytical views from cleaned student data."""
        conn = self.get_connection()
        if df is None:
            if settings.CLEANED_DATA_PATH.exists():
                df = pd.read_csv(settings.CLEANED_DATA_PATH)
            else:
                logger.warning("No data provided or found to initialize DuckDB.")
                return

        # Register or replace students table
        conn.register("df_students_temp", df)
        conn.execute("CREATE OR REPLACE TABLE students AS SELECT * FROM df_students_temp;")
        conn.unregister("df_students_temp")

        # Create department summary analytical view
        conn.execute("""
            CREATE OR REPLACE VIEW department_summary AS
            SELECT 
                department,
                COUNT(*) as student_count,
                ROUND(AVG(cgpa), 2) as avg_cgpa,
                ROUND(AVG(attendance), 2) as avg_attendance,
                ROUND(AVG(academic_risk_score), 2) as avg_risk_score,
                SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as at_risk_count,
                ROUND(SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as at_risk_percentage
            FROM students
            GROUP BY department;
        """)

        # Create risk distribution view
        conn.execute("""
            CREATE OR REPLACE VIEW risk_summary AS
            SELECT 
                risk_level,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students), 1) as percentage,
                ROUND(AVG(cgpa), 2) as avg_cgpa,
                ROUND(AVG(attendance), 2) as avg_attendance
            FROM students
            GROUP BY risk_level;
        """)

        logger.info(f"DuckDB initialized successfully with {len(df)} records in table 'students'.")

    def execute_query(self, query: str, params: Optional[Any] = None) -> pd.DataFrame:
        """Executes a safe read query and returns results as pandas DataFrame."""
        conn = self.get_connection()
        try:
            if params:
                result = conn.execute(query, params).df()
            else:
                result = conn.execute(query).df()
            return result
        except Exception as e:
            logger.error(f"Query execution error: {e} | Query: {query}")
            raise

    def close(self):
        """Closes DuckDB connection."""
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None

# Global DB Singleton
db_manager = DatabaseManager()
