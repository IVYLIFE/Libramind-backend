from datetime import date
from typing import List
from app.schemas import BookIssueRecord

ISSUED_BOOKS: List[BookIssueRecord] = [
    BookIssueRecord(
        id=1,
        book_id=1,
        student_roll_number="101",
        issue_date=date(2023, 10, 1),
        due_date=date(2023, 10, 15),
        returned_date=None
    ),
]
