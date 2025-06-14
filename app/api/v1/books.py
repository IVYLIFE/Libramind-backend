# books.py
from fastapi import APIRouter, status, Query, Path, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas import (
    Book,
    IssueBook,
    ErrorResponse,
    SuccessResponse,
    BookResponse,
    BookListResponse,
    BookIssueRecordResponse,
)
import app.services.book as services
from app.utils import success_response


router = APIRouter(prefix="/books", tags=["books"])

@router.get( 
    "",
    response_model=BookListResponse,
    responses={500: {"model": ErrorResponse}}
)
def read_books(
    title    : Optional[str] = Query(None, description="Filter by book title"),
    author   : Optional[str] = Query(None, description="Filter by book author"),
    category : Optional[str] = Query(None, description="Filter by book category"),
    page     : int           = Query(1, ge=1, description="Page number for pagination"),
    limit    : int           = Query(10, ge=1, le=50, description="Number of books per page"),
    db       : Session       = Depends(get_db),
):
    books, meta = services.list_books(title, author, category, page, limit, db)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Books fetched successfully",
        data=books,
        meta=meta
    )




@router.get("/overdue-books", response_model=BookIssueRecordResponse)
def get_overdue_books(db: Session = Depends(get_db)):
    print("2")

    overdue_books = services.get_overdue_books(db)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Overdue Books fetched successfully",
        data=overdue_books
    )



@router.get(
    "/{book_id}",
    response_model=BookResponse,
    responses={404: {"model": ErrorResponse}}
)
def read_book(
    book_id: str = Path(...,  description="Book ID/ISBN as unique identifier of Book"),
    db: Session = Depends(get_db)
):
    print("1")
    
    book = services.get_single_book(book_id, db)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Book fetched successfully",
        data=[book],
    )



@router.post("", response_model=SuccessResponse )
def create_book(book: Book, db: Session = Depends(get_db)):    
    result = services.add_book(book, db)

    message = "Book added successfully"
    if result["updated"]:
        message = "Book already exists. Copies updated."
    
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message=message,
        data=None,
        meta=None
    )


    
@router.put(
    "/{book_id}",
    response_model=BookResponse,
    responses={404: {"model": ErrorResponse}}
)
def update_book(
    updated: Book, 
    book_id: str = Path(..., description="Book ID/ISBN as unique identifier of Book"),
    db: Session = Depends(get_db)
):
    book = services.update_book(book_id, updated, db)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Book udated successfully",
        data=book,
    )



@router.delete(
    "/{book_id}",
    response_model=SuccessResponse,
    responses={404: {"model": ErrorResponse}}
)
def delete_book(
    book_id: str = Path(..., description="Book ID/ISBN as unique identifier of Book"),
    db: Session = Depends(get_db)
):
    if services.delete_book(book_id, db): 
        return success_response(
            status_code=status.HTTP_200_OK,
            message="Book Deleted Successfully"
        )



@router.post(
    "/{book_id}",
    response_model=BookIssueRecordResponse,
)
def issue_book_to_student(
    book_id: str = Path(..., description="Book ID/ISBN as unique identifier of Book"),
    payload: IssueBook = ...,
    db: Session = Depends(get_db)
):    
    issuance_record = services.issue_book(book_id, payload, db)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Book issued successfully",
        data=issuance_record
    )


# =====================================================================