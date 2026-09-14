"""Student directory and individual student intelligence endpoints."""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from src.analytics.queries import filter_students
from src.analytics.database import db_manager
from src.ml.predict import predict_single_student

router = APIRouter(prefix="/students", tags=["Students"])

class StudentResponse(BaseModel):
    student_id: str
    name: str
    department: str
    gender: str
    cgpa: float
    attendance: float
    enrollment_date: str
    academic_risk_score: float
    risk_level: str
    support_priority: str

class SingleStudentDetail(BaseModel):
    student: Dict[str, Any]
    risk_assessment: Dict[str, Any]

@router.get("", response_model=List[Dict[str, Any]])
def list_students(
    department: Optional[str] = Query(None, description="Filter by department"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    min_cgpa: Optional[float] = Query(None, description="Minimum CGPA"),
    max_cgpa: Optional[float] = Query(None, description="Maximum CGPA"),
    min_attendance: Optional[float] = Query(None, description="Minimum attendance %"),
    max_attendance: Optional[float] = Query(None, description="Maximum attendance %"),
    risk_level: Optional[str] = Query(None, description="Risk level (LOW, MEDIUM, HIGH, CRITICAL)"),
    search: Optional[str] = Query(None, description="Search term for name or student ID"),
    limit: int = Query(100, ge=1, le=1000, description="Max rows to return")
):
    """Query and filter student records from analytical store."""
    df = filter_students(
        department=department,
        gender=gender,
        min_cgpa=min_cgpa,
        max_cgpa=max_cgpa,
        min_attendance=min_attendance,
        max_attendance=max_attendance,
        risk_level=risk_level,
        search_term=search,
        limit=limit
    )
    return df.to_dict(orient="records")

@router.get("/{student_id}", response_model=SingleStudentDetail)
def get_student(student_id: str):
    """Retrieve single student record with AI-driven retention risk diagnosis."""
    query = "SELECT * FROM students WHERE UPPER(student_id) = UPPER(?);"
    df = db_manager.execute_query(query, [student_id])
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Student ID '{student_id}' not found.")
    
    student_dict = df.iloc[0].to_dict()
    # Compute real-time risk explanation
    assessment = predict_single_student(student_dict)
    
    return {
        "student": student_dict,
        "risk_assessment": assessment
    }