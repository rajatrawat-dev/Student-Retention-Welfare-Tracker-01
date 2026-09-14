"""Intent classification for natural language queries."""

import re
from typing import Tuple, Dict, Any

INTENTS = {
    "ATTENDANCE_LOW": ["attendance below", "low attendance", "absent", "poor attendance", "attendance under", "less attendance"],
    "DEPT_COMPARISON": ["compare", "department", "departments", "highest cgpa", "lowest cgpa", "which department", "cse", "ece", "mech", "civil", "it"],
    "RISK_OVERVIEW": ["high risk", "at risk", "critical", "welfare", "retention risk", "academic risk", "need support", "requiring support"],
    "TOP_PERFORMERS": ["top", "best", "highest score", "rank", "topper", "leaderboard"],
    "CORRELATION": ["relationship", "correlation", "relate", "vs", "versus", "affect"],
    "DISTRIBUTION": ["distribution", "breakdown", "histogram", "spread"],
    "STUDENT_LOOKUP": ["student id", "stu-", "profile", "lookup", "who is"],
}

def detect_intent(question: str) -> Tuple[str, Dict[str, Any]]:
    """Detects user analytical intent and extracts parameters (e.g. thresholds, limits)."""
    q = question.lower()
    
    # Extract numeric threshold if present (e.g. 60%, 75, 10)
    number_match = re.search(r'(\d+(?:\.\d+)?)', q)
    extracted_num = float(number_match.group(1)) if number_match else None
    
    if any(k in q for k in INTENTS["ATTENDANCE_LOW"]):
        threshold = extracted_num if (extracted_num and extracted_num <= 100) else 75.0
        return "ATTENDANCE_QUERY", {"threshold": threshold}
        
    if any(k in q for k in INTENTS["RISK_OVERVIEW"]):
        return "RISK_QUERY", {}
        
    if any(k in q for k in INTENTS["TOP_PERFORMERS"]):
        limit = int(extracted_num) if (extracted_num and extracted_num <= 50) else 10
        return "TOP_PERFORMERS", {"limit": limit}
        
    if any(k in q for k in INTENTS["CORRELATION"]):
        return "CORRELATION_QUERY", {}
        
    if any(k in q for k in INTENTS["DEPT_COMPARISON"]):
        return "DEPARTMENT_QUERY", {}
        
    if any(k in q for k in INTENTS["DISTRIBUTION"]):
        return "DISTRIBUTION_QUERY", {}
        
    return "GENERAL_QUERY", {}
