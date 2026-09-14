"""AI Analyst copilot query endpoint."""

from typing import Optional, Dict, Any, List
from fastapi import APIRouter
from pydantic import BaseModel, Field
from src.agent.agent import student_iq_analyst

router = APIRouter(prefix="/agent", tags=["AI Analyst"])

class QueryRequest(BaseModel):
    question: str = Field(..., example="Which departments have the lowest average CGPA?")

class QueryResponse(BaseModel):
    question: str
    intent: str
    sql: str
    is_safe: bool
    safety_message: str
    execution_success: bool
    data: Optional[List[Dict[str, Any]]] = None
    chart_type: str
    explanation: str
    engine_used: str

@router.post("/query", response_model=QueryResponse)
def ask_ai_analyst(payload: QueryRequest):
    """Translates natural language questions into safe DuckDB queries with recommended visualizations."""
    resp = student_iq_analyst.ask(payload.question)
    data_list = resp.data.to_dict(orient="records") if resp.data is not None else None
    
    return QueryResponse(
        question=resp.question,
        intent=resp.intent,
        sql=resp.sql,
        is_safe=resp.is_safe,
        safety_message=resp.safety_message,
        execution_success=resp.execution_success,
        data=data_list,
        chart_type=resp.chart_type,
        explanation=resp.explanation,
        engine_used=resp.engine_used
    )