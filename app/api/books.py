# routes.py
from fastapi import APIRouter, status, Query, Path
from typing import Optional
import json

from app.schemas import Book, BookResponse, BookListResponse, ErrorResponse
from app.utils import success_response, error_response
import app.services as services

router = APIRouter(prefix="/books", tags=["books"])


@router.get( 
    "",
    response_model=BookListResponse,
    responses={500: {"model": ErrorResponse}}
)
def read_books(
    title    : Optional[str] = Query(None),
    author   : Optional[str] = Query(None),
    category : Optional[str] = Query(None),
    page     : int           = Query(1, ge=1),
    limit    : int           = Query(10, ge=1, le=50),
):
    books, meta = services.list_books(title, author, category, page, limit)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Books fetched successfully",
        data=books,
        meta=meta
    )



@router.get("/{book_id}", response_model=BookResponse )
def read_book(book_id: int = Path(ge=1)):
    book = services.get_book(book_id)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Book fetched successfully",
        data=book,
    )



@router.post("", response_model=BookResponse )
def create_book(book: Book):    
    result = services.add_book(book)

    if result["updated"]:
        return success_response(
            status_code=200,
            message="Book already exists. Copies updated.",
            data=result["book"]
        )
    else:
        return success_response(
            status_code=201,
            message="Book added successfully",
            data=result["book"]
        )

    


@router.put("/{book_id}", response_model=BookResponse )
def update_book( updated: Book, book_id: int = Path(ge=1)):
    book = services.update_book(book_id, updated)

    return success_response(
        status_code=200,
        message="Book udated successfully",
        data=book,
    )



@router.delete("/{book_id}", response_model=BookResponse )
def delete_book(book_id: int = Path(ge=1)):
    
    if services.delete_book(book_id): 
        return success_response(
            status_code=200,
            message="Book Deleted Successfully"
        )
