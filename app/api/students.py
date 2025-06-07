from fastapi import APIRouter, status, Query, Path, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas import (
    Student, 
    StudentResponse,
    StudentListResponse,
    SuccessResponse,
    BookIssueRecordResponse
)
import app.services.student as services
from app.database import get_db
from app.utils import success_response

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=StudentListResponse)
def fetch_students(
    department : Optional[str] = Query(None, description="Filter by department"),
    semester   : Optional[int] = Query(None, description="Filter by semester"),
    search     : Optional[str] = Query(None, description="Search by partial match in name, roll number, or phone"),
    page       : int           = Query(1, description="Page number for pagination", ge=1),
    limit      : int           = Query(10, description="Number of students per page", ge=1),
    db         : Session       = Depends(get_db),
):
    print("1")
    students, meta = services.list_students(department, semester, search, page, limit, db)
    print("6")
    
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Students fetched successfully",
        data=students,
        meta=meta
    )



@router.post("", response_model=SuccessResponse)
def add_student(student: Student, db: Session = Depends(get_db)):
    services.add_student(student, db)

    return success_response(
        status_code=201,
        message="Student Added Successfully.",
        data=None,
        meta=None,
    )



@router.get("/{identifier}", response_model=StudentResponse)
def get_student(
    identifier: str = Path(..., description="Student name, roll number, or phone"),
    db: Session = Depends(get_db)
):
    student = services.get_student_by_identifier(identifier, db)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Student fetched successfully",
        data=[student],
    )



@router.get("/{identifier}/books", response_model=BookIssueRecordResponse)
def get_books_issued_to_student(
    identifier: str = Path(..., description="Student name, roll number, or phone"),
    db: Session = Depends(get_db)
):
    issued_books =  services.get_student_books(identifier, db)
    
    return success_response(
        status_code=201,
        message="Issued Books Fetched successfully",
        data=issued_books
    )




@router.patch("/{identifier}/books/{issued_book_id}", response_model=BookIssueRecordResponse)
def return_issued_book(
    identifier: str,
    issued_book_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    book_to_return = services.return_book(identifier, issued_book_id, db)

    return success_response(
        status_code=201,
        message="Books Returned successfully",
        data=book_to_return
    )


