"""StudentIQ AI Analyst - The Controlled Natural Language Analytics Copilot."""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import pandas as pd
from src.agent.intent import detect_intent
from src.agent.query_generator import generate_sql_via_rules, generate_sql_via_ollama
from src.agent.query_validator import validate_query
from src.agent.chart_selector import recommend_chart_type
from src.analytics.database import db_manager
from src.utils.logging import get_logger

logger = get_logger("AIAgent")

@dataclass
class AgentResponse:
    question: str
    intent: str
    sql: str
    is_safe: bool
    safety_message: str
    execution_success: bool
    data: Optional[pd.DataFrame]
    chart_type: str
    explanation: str
    engine_used: str

class StudentIQAnalyst:
    """Orchestrates end-to-end question answering with safety validations and data insights."""

    def ask(self, question: str) -> AgentResponse:
        logger.info(f"Processing query: '{question}'")
        
        # 1. Intent Detection
        intent, params = detect_intent(question)
        
        # 2. Query Generation (Ollama with automatic Rule-based fallback)
        engine_used = "Rule-Based Natural Language Engine"
        sql = ""
        ollama_success, ollama_sql = generate_sql_via_ollama(question)
        if ollama_success and ollama_sql:
            # Test if valid
            is_valid, _ = validate_query(ollama_sql)
            if is_valid:
                sql = ollama_sql
                engine_used = f"Ollama ({settings.OLLAMA_MODEL})"
                
        if not sql:
            sql = generate_sql_via_rules(question, intent, params)

        # 3. Query Validation (AI Safety layer)
        is_safe, safety_msg = validate_query(sql)
        if not is_safe:
            logger.warning(f"Unsafe query rejected: {safety_msg}")
            return AgentResponse(
                question=question,
                intent=intent,
                sql=sql,
                is_safe=False,
                safety_message=safety_msg,
                execution_success=False,
                data=None,
                chart_type="table",
                explanation=f"Query rejected by AI Safety Layer: {safety_msg}",
                engine_used=engine_used
            )

        # 4. DuckDB Execution
        try:
            df_result = db_manager.execute_query(sql)
            exec_success = True
        except Exception as e:
            logger.error(f"Execution failure: {e}")
            return AgentResponse(
                question=question,
                intent=intent,
                sql=sql,
                is_safe=True,
                safety_message=safety_msg,
                execution_success=False,
                data=None,
                chart_type="table",
                explanation=f"Database execution error: {str(e)}",
                engine_used=engine_used
            )

        # 5. Chart Selection
        chart_type = recommend_chart_type(intent, df_result)

        # 6. Natural Language Synthesis
        explanation = self._synthesize_explanation(question, intent, df_result)

        return AgentResponse(
            question=question,
            intent=intent,
            sql=sql,
            is_safe=True,
            safety_message=safety_msg,
            execution_success=exec_success,
            data=df_result,
            chart_type=chart_type,
            explanation=explanation,
            engine_used=engine_used
        )

    def _synthesize_explanation(self, question: str, intent: str, df: pd.DataFrame) -> str:
        if df.empty:
            return "No matching student records found for the specified criteria."
            
        row_count = len(df)
        if intent == "ATTENDANCE_QUERY":
            min_att = df["attendance"].min() if "attendance" in df else 0
            return f"Retrieved {row_count} student records with attendance below specified threshold. Lowest registered attendance is {min_att}%."
            
        if intent == "DEPARTMENT_QUERY":
            if "avg_cgpa" in df.columns:
                leader = df.iloc[0]["department"]
                high_cgpa = df.iloc[0]["avg_cgpa"]
                return f"Departmental breakdown across {row_count} academic disciplines. Leading department is '{leader}' with an average CGPA of {high_cgpa}."
            return f"Comparative breakdown across {row_count} academic disciplines generated successfully."
            
        if intent == "RISK_QUERY":
            return f"Identified {row_count} students positioned in Elevated Retention Risk categories (HIGH / CRITICAL) requiring prioritized academic counseling."
            
        if intent == "TOP_PERFORMERS":
            topper = df.iloc[0]["name"] if "name" in df else "Top Student"
            cgpa = df.iloc[0]["cgpa"] if "cgpa" in df else "N/A"
            return f"Displaying the top {row_count} academic performers. Highest ranking student is {topper} with a CGPA of {cgpa}."
            
        if intent == "CORRELATION_QUERY":
            return f"Analyzed {row_count} student performance datapoints illustrating the empirical relationship between attendance consistency and cumulative grade points."
            
        return f"Successfully queried and analyzed {row_count} student records adhering to canonical schema."

# Singleton Agent
student_iq_analyst = StudentIQAnalyst()
