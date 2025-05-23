from fastapi import APIRouter, Query
from typing import List
from datetime import date

from app.schemas import IssuedBook, IssuedBookOut
import app.crud as issue_crud

router = APIRouter(prefix="/issues", tags=["issues"])


@router.post("", response_model=IssuedBookOut, status_code=201)
def create_issue(issue: IssuedBook):
    return issue_crud.issue_book(issue)


@router.post("/{issue_id}/return", response_model=IssuedBookOut)
def return_book(issue_id: int, return_date: date = Query(...)):
    return issue_crud.return_book(issue_id, return_date)


@router.get("/student/{student_id}", response_model=List[IssuedBookOut])
def get_issued_books(student_id: int):
    return issue_crud.list_issued_books_by_student(student_id)
