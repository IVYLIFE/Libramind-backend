from typing import List, Optional
from fastapi import HTTPException
from datetime import date

from app.schemas import IssuedBook, IssuedBookOut
from app.database import ISSUES, BOOKS, STUDENTS


def issue_book(issue: IssuedBook) -> IssuedBookOut:
    # Check if student exists
    student_exists = any(s.id == issue.student_id for s in STUDENTS)
    if not student_exists:
        raise HTTPException(status_code=404, detail="Student not found")

    # Find the book and check available copies
    book = next((b for b in BOOKS if b["id"] == issue.book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book["copies"] < 1:
        raise HTTPException(status_code=400, detail="No copies available to issue")

    # Reduce copies
    book["copies"] -= 1

    # Create issue record
    new_id = max((i.id for i in ISSUES), default=0) + 1
    new_issue = IssuedBookOut(
        id=new_id,
        student_id=issue.student_id,
        book_id=issue.book_id,
        issue_date=issue.issue_date,
        expected_return_date=issue.expected_return_date,
        returned_date=None,
    )
    ISSUES.append(new_issue)
    return new_issue


def return_book(issue_id: int, return_date: date) -> IssuedBookOut:
    issue = next((i for i in ISSUES if i.id == issue_id), None)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue record not found")
    if issue.returned_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")

    # Mark as returned
    issue.returned_date = return_date

    # Increase book copies
    book = next((b for b in BOOKS if b["id"] == issue.book_id), None)
    if book:
        book["copies"] += 1

    return issue


def list_issued_books_by_student(student_id: int) -> List[IssuedBookOut]:
    # Return all issues for student where returned_date is None (currently issued)
    return [i for i in ISSUES if i.student_id == student_id and i.returned_date is None]
