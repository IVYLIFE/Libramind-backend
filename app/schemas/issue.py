from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional


class IssueBook(BaseModel):
    student_id: str = Field(..., description="ID of student to whom the book will issue")
    duration_days: int = Field(..., ge=1, description="No of days for which the book is issued")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "student_id": "101",
                    "duration_days": 10,
                }
            ]
        }
    )



class BookIssueRecord(BaseModel):
    id: int = Field(..., description="Unique ID of the issued book record", ge=1)
    book_id: int = Field(..., description="Details of the issued book", ge=1)
    student_id: int = Field(..., description="Id of the student to whom the book is issued")
    issue_date: date = Field(..., description="Date when the book was issued")
    due_date: date = Field(..., description="Expected return date for the book")
    returned_date: Optional[date] = Field(None, description="Actual date when the book was returned")
    is_overdue: bool = Field(..., description="Whether the book is overdue")


    class Config:
        from_attributes = True


# =====================================================================