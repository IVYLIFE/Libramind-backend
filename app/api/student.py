from fastapi import APIRouter, Query
from typing import List, Optional

from app.schemas import Student, StudentOut
import app.crud as student_crud

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=StudentOut, status_code=201)
def create_student(student: Student):
    return student_crud.add_student(student)


@router.get("", response_model=List[StudentOut])
def read_students(
    department: Optional[str] = None,
    semester: Optional[int] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
):
    return student_crud.list_students(department, semester, search, page, limit)


@router.get("/by-identifier", response_model=StudentOut)
def read_student_by_identifier(
    identifier: str = Query(..., description="Student name, roll number, or phone")
):
    return student_crud.get_student_by_identifier(identifier)
