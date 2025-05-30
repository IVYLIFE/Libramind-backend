from typing import Any, Generic, List, TypeVar, Optional, Dict
from pydantic import BaseModel
from pydantic.generics import GenericModel

from app.schemas import BookOut

T = TypeVar("T")

class SuccessResponse(GenericModel, Generic[T]):
    status_code: int
    status: str
    message: str
    data: Optional[T] = None
    meta: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    status_code: int
    status: str
    message: str
    detail: Optional[str] = None


class BookListResponse(SuccessResponse[List[BookOut]]):
    class Config:
        title = "BookListResponse"

class BookResponse(SuccessResponse[BookOut]):
    class Config:
        title = "BookResponse"