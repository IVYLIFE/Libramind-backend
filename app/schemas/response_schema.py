from typing import Any, Generic, List, TypeVar, Optional, Dict
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from app.schemas import BookOut, Student, BookIssueRecord

T = TypeVar("T")

class SuccessResponse(GenericModel, Generic[T]):
    status_code: int
    status: str
    message: str
    data: Optional[T] = None
    meta: Optional[Dict[str, Any]]

class ErrorResponse(BaseModel):
    status_code: int
    status: str
    detail: Optional[str] = None

class BookResponse(SuccessResponse[List[BookOut]]):
    meta: Optional[Dict[str, Any]] = Field(None, example={
        "page": 1,
        "limit": 10,
        "total_books": 25,
        "fetched_count": 10,
        "filters_applied": {}
    })

    class Config:
        title = "BookResponse"

class StudentResponse(SuccessResponse[List[Student]]):
    meta: Optional[Dict[str, Any]] = Field(None, example={
        "page": 1,
        "limit": 10,
        "total_students": 50,
        "fetched_count": 10,
        "filters_applied": {}
    })

    class Config:
        title = "StudentResponse"

class BookIssueRecordResponse(SuccessResponse[List[BookIssueRecord]]):
    class Config:
        title = "BookIssueRecordResponse"