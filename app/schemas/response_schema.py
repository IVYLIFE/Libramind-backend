from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Field

from app.schemas import BookOut, Student, BookIssueRecord


# ==============================
# ✅ 1. Error Response
# ==============================

class ErrorResponse(BaseModel):
    status_code: int = Field(..., example=400, description="HTTP status code for error")
    status: str = Field(..., example="failure", description="Status of the response")
    detail: Optional[str] = Field(None, example="Something went wrong", description="Detailed error message")

    class Config:
        title = "ErrorResponse"


# ==============================
# ✅ 2. Success Response (No data, no meta)
# ==============================

class SuccessResponse(BaseModel):
    status_code: int = Field(..., example=200, description="HTTP status code")
    status: str = Field(..., example="success", description="Status of the response")
    message: str = Field(..., example="Operation successful", description="Short success message")

    class Config:
        title = "SuccessResponse"


# ==============================
# ✅ 3. Success Response with Data
# 1. BookResponse
# 2. StudentResponse
# 3. BookIssueRecordResponse
# ==============================

class BookResponse(SuccessResponse):
    data: List[BookOut] = Field(..., description="List of books")
    class Config:
        title = "BookResponse"


class StudentResponse(SuccessResponse):
    data: List[Student] = Field(..., description="List of students")
    class Config:
        title = "StudentResponse"


class BookIssueRecordResponse(SuccessResponse):
    data: List[BookIssueRecord] = Field(..., description="List of book issue records")
    class Config:
        title = "BookIssueRecordResponse"


# ==============================
# ✅ 4. Success Response with Data and Meta
# ==============================


class BookListResponse(SuccessResponse):
    data: List[BookOut] = Field(..., description="List of books")
    meta: Dict[str, Any] = Field(
        ...,
        example={
            "page": 1,
            "limit": 10,
            "total_books": 30,
            "fetched_count": 10,
            "filters_applied": {}
        },
        description="Pagination and filter info"
    )

    class Config:
        title = "BookListResponse"


class StudentListResponse(SuccessResponse):

    data: List[Student] = Field(..., description="List of students")
    meta: Dict[str, Any] = Field(
        ..., 
        example={
            "page": 1,
            "limit": 10,
            "total_records": 50,
            "fetched_count": 10,
            "filters_applied": {}
        },
        description="Pagination and filter info"
    )


    class Config:
        title = "StudentListResponse"

