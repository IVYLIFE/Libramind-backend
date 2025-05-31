from fastapi import APIRouter, status, Query, Path
from typing import List, Optional

from app.schemas import Student, StudentResponse, BookIssueRecordResponse
from app.utils import success_response
import app.services as services

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=StudentResponse)
def fetch_students(
    department : Optional[str] = Query(None, description="Filter by department"),
    semester   : Optional[str] = Query(None, description="Filter by semester"),
    search     : Optional[str] = Query(None, description="Search by partial match in name, roll number, or phone"),
    page       : int           = Query(1, description="Page number for pagination", ge=1),
    limit      : int           = Query(10, description="Number of students per page", ge=1),
):
    students, meta = services.list_students(department, semester, search, page, limit)
    
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Students fetched successfully",
        data=students,
        meta=meta
    )



@router.post("", response_model=dict)
def add_student(student: Student):
    services.add_student(student)

    return success_response(
        status_code=201,
        message="Student Added Successfully.",
    )



@router.get("/{identifier}", response_model=StudentResponse)
def get_student(
    identifier: str = Path(..., description="Student name, roll number, or phone")
):
    student = services.get_student_by_identifier(identifier)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Student fetched successfully",
        data=[student],
    )



@router.get("/{identifier}/books", response_model=BookIssueRecordResponse)
def get_books_issued_to_student(
    identifier: str = Path(..., description="Student name, roll number, or phone")
):
    issued_books =  services.get_student_books(identifier)
    
    return success_response(
        status_code=201,
        message="Issued Books Fetched successfully",
        data=issued_books
    )




@router.patch("/{student_id}/books/{issued_book_id}", response_model=BookIssueRecordResponse)
def return_issued_book(student_id: str, issued_book_id: int = Path(..., gt=0)):
    book_to_return = services.return_book(student_id, issued_book_id)

    return success_response(
        status_code=201,
        message="Books Returned successfully",
        data=book_to_return
    )


