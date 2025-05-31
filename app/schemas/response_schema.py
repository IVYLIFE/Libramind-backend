from typing import Any, Generic, List, TypeVar, Optional, Dict
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from app.schemas import BookOut, Student, BookIssueRecord

T = TypeVar("T")

class ErrorResponse(BaseModel):
    status_code: int = Field(..., example=400)
    status: str = Field(..., example="failure")
    detail: Optional[str] = Field(None, example="Something went Wrong")

# Without data and meta
class SuccessResponse(GenericModel, Generic[T]):
    status_code: int = Field(..., example=200)
    status: str = Field(..., example="success")
    message: str = Field(..., example="Operation successful")


# All fields : data + meta
class BookResponse_Meta(SuccessResponse[List[BookOut]]):
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
        title = "BookResponse_Meta"

# Without meta
class BookResponse(SuccessResponse[List[BookOut]]):
    data: List[BookOut] = Field(..., description="List of books")
    class Config:
        title = "BookResponse"




class StudentResponse_Meta(SuccessResponse[List[Student]]):

    data: List[Student] = Field(..., description="List of students")
    meta: Dict[str, Any] = Field(
        ..., 
        example={
            "page": 1,
            "limit": 10,
            "total_students": 50,
            "fetched_count": 10,
            "filters_applied": {}
        },
        description="Pagination and filter info"
    )


    class Config:
        title = "StudentResponse"


# Without meta
class StudentResponse(SuccessResponse[List[BookOut]]):
    data: List[Student] = Field(None, description="List of students")
    class Config:
        title = "StudentResponse"


class BookIssueRecordResponse(SuccessResponse[List[BookIssueRecord]]):
    data: Optional[List[BookIssueRecord]] = Field(..., description="List of book issue records")
    class Config:
        title = "BookIssueRecordResponse"