# books.py
from fastapi import APIRouter, status, Query, Path
from typing import Optional

from app.schemas import (
    Book,
    IssueBook,
    ErrorResponse,
    SuccessResponse,
    BookResponse,
    BookResponse_Meta,
    BookIssueRecordResponse,
)
from app.utils import success_response
import app.services as services

router = APIRouter(prefix="/books", tags=["books"])


@router.get( 
    "",
    response_model=BookResponse_Meta,
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
def read_book(book_id: str = Path(...,  description="Book ID/ISBN as unique identifier of Book")):
    book = services.get_single_book(book_id)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Book fetched successfully",
        data=[book],
    )



@router.post("", response_model=SuccessResponse )
def create_book(book: Book):    
    result = services.add_book(book)
    message = "Book added successfully"
    if result["updated"]:
        message = "Book already exists. Copies updated."
    
    return success_response(
        status_code=201,
        message=message,
        data=None,
        meta=None
    )


    
@router.put("/{book_id}", response_model=BookResponse )
def update_book( updated: Book, book_id: str = Path(..., description="Book ID/ISBN as unique identifier of Book")):
    print("Update is called")
    book = services.update_book(book_id, updated)

    return success_response(
        status_code=200,
        message="Book udated successfully",
        data=book,
    )



@router.delete("/{book_id}", response_model=SuccessResponse )
def delete_book(book_id: str = Path(..., description="Book ID/ISBN as unique identifier of Book")):
    print("Delete is called")
    if services.delete_book(book_id): 
        return success_response(
            status_code=200,
            message="Book Deleted Successfully"
        )



@router.post("/{book_id}", response_model=BookIssueRecordResponse, status_code=201)
def issue_book_to_student(
    book_id: str = Path(..., description="Book ID/ISBN as unique identifier of Book"),
    payload: IssueBook = ...
):
    print("Issue book is called")
    
    issuance_record = services.issue_book(book_id, payload)

    return success_response(
        status_code=201,
        message="Book issued successfully",
        data=issuance_record
    )

