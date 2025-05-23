from datetime import date
from typing import Optional
from pydantic import BaseModel

from app.schemas import BookOut


class IssuedBook(BaseModel):
    student_id: int
    book_id: int
    due_date: date
    issue_date: date

class IssuedBookOut(BaseModel):
    id: int
    book: BookOut
    due_date: date
    returned_date: Optional[date] = None

    class Config:
        from_attributes = True






    
