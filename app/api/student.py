from fastapi import APIRouter, Query, Path
from typing import List, Optional

from app.schemas import Student, IssuedBookOut
import app.services as services

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=List[Student])
def read_students(
    department: Optional[str] = Query(None, description="Filter by department"),
    semester: Optional[str] = Query(None, description="Filter by semester"),
    search: Optional[str] = Query(
        None, description="Search by partial match in name, roll number, or phone"
    ),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(10, ge=1, description="Number of students per page"),
):
    return services.list_students(department, semester, search, page, limit)



@router.get("/{identifier}", response_model=Student)
def read_student_by_identifier(
    identifier: str = Path(..., description="Student name, roll number, or phone")
):
    return services.get_student_by_identifier(identifier)



@router.post("", response_model=Student, status_code=201)
def create_student(student: Student):
    return services.add_student(student)



@router.get("/{identifier}/books", response_model=List[IssuedBookOut])
def read_student_books(
    identifier: str,
):
    return services.get_student_books(identifier)
