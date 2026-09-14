"""SQL query generator supporting both Ollama LLM and deterministic rule-based engine."""

import re
import json
import requests
from typing import Tuple, Dict, Any
from src.config.settings import settings
from src.agent.prompts import SYSTEM_PROMPT
from src.agent.intent import detect_intent
from src.utils.logging import get_logger

logger = get_logger("QueryGenerator")

def generate_sql_via_rules(question: str, intent: str, params: Dict[str, Any]) -> str:
    """Deterministic, robust fallback SQL generator that handles all hackathon queries without any LLM."""
    q = question.lower()
    
    # 1. Attendance queries e.g. "Show students with attendance below 60%"
    if intent == "ATTENDANCE_QUERY":
        threshold = params.get("threshold", 75.0)
        return f"""
SELECT student_id, name, department, attendance, cgpa, risk_level 
FROM students 
WHERE attendance < {threshold} 
ORDER BY attendance ASC 
LIMIT 20;
""".strip()

    # 2. Lowest/Highest department average CGPA e.g. "Which departments have the lowest average CGPA?"
    if "lowest" in q and ("cgpa" in q or "average" in q):
        return """
SELECT department, ROUND(AVG(cgpa), 2) as avg_cgpa, COUNT(*) as student_count 
FROM students 
GROUP BY department 
ORDER BY avg_cgpa ASC;
""".strip()

    if "highest" in q and ("cgpa" in q or "average" in q):
        return """
SELECT department, ROUND(AVG(cgpa), 2) as avg_cgpa, COUNT(*) as student_count 
FROM students 
GROUP BY department 
ORDER BY avg_cgpa DESC;
""".strip()

    # 3. Department comparisons e.g. "Compare CSE, ECE and IT" or "Compare departments"
    if intent == "DEPARTMENT_QUERY":
        return """
SELECT 
    department, 
    COUNT(*) as student_count, 
    ROUND(AVG(cgpa), 2) as avg_cgpa, 
    ROUND(AVG(attendance), 2) as avg_attendance,
    SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as at_risk_students
FROM students 
GROUP BY department 
ORDER BY avg_cgpa DESC;
""".strip()

    # 4. Attendance vs CGPA relationship e.g. "Show the relationship between attendance and CGPA"
    if intent == "CORRELATION_QUERY":
        return """
SELECT student_id, name, department, attendance, cgpa, risk_level 
FROM students 
ORDER BY cgpa DESC 
LIMIT 100;
""".strip()

    # 5. High risk students e.g. "Which students are at high risk?"
    if "high risk" in q or "critical" in q or intent == "RISK_QUERY":
        return """
SELECT student_id, name, department, cgpa, attendance, academic_risk_score, risk_level, support_priority 
FROM students 
WHERE risk_level IN ('HIGH', 'CRITICAL') 
ORDER BY academic_risk_score DESC 
LIMIT 25;
""".strip()

    # 6. Risk distribution e.g. "Show the distribution of student risk"
    if "distribution" in q and "risk" in q:
        return """
SELECT 
    risk_level, 
    COUNT(*) as student_count, 
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students), 1) as percentage 
FROM students 
GROUP BY risk_level 
ORDER BY student_count DESC;
""".strip()

    # 7. Department needing most academic support e.g. "Which department needs the most academic support?"
    if "support" in q and "department" in q:
        return """
SELECT 
    department, 
    SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as at_risk_count,
    ROUND(SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as at_risk_percentage,
    ROUND(AVG(academic_risk_score), 2) as avg_risk_score
FROM students 
GROUP BY department 
ORDER BY at_risk_count DESC;
""".strip()

    # 8. Top 10 students by CGPA e.g. "Show top 10 students by CGPA"
    if intent == "TOP_PERFORMERS":
        limit = params.get("limit", 10)
        return f"""
SELECT student_id, name, department, cgpa, attendance, risk_level 
FROM students 
ORDER BY cgpa DESC, attendance DESC 
LIMIT {limit};
""".strip()

    # Default fallback query
    return """
SELECT student_id, name, department, cgpa, attendance, risk_level 
FROM students 
ORDER BY academic_risk_score DESC 
LIMIT 15;
""".strip()

def generate_sql_via_ollama(question: str) -> Tuple[bool, str]:
    """Attempts to query local Ollama instance if active."""
    url = f"{settings.OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": f"{SYSTEM_PROMPT}\nUser Question: {question}\nSQL Query:",
        "stream": False,
    }
    try:
        resp = requests.post(url, json=payload, timeout=settings.OLLAMA_TIMEOUT_SECONDS)
        if resp.status_code == 200:
            raw_text = resp.json().get("response", "")
            # Extract SQL between markdown blocks
            sql_match = re.search(r'```(?:sql)?(.*?)```', raw_text, re.DOTALL)
            if sql_match:
                return True, sql_match.group(1).strip()
            return True, raw_text.strip()
    except Exception:
        pass
    return False, ""
