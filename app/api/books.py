# routes.py
from fastapi import APIRouter, Query
from typing import List, Optional

from app.schemas import Book, BookOut
import app.services as services

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=List[BookOut])
def read_books(
    title    : Optional[str] = Query(None),
    author   : Optional[str] = Query(None),
    category : Optional[str] = Query(None),
    page     : int           = Query(1, ge=1),
    limit    : int           = Query(10, ge=1, le=50),
):
    return services.list_books(title, author, category, page, limit)


@router.get("/{book_id}", response_model=BookOut)
def read_book(book_id: int):
    return services.get_book(book_id)


@router.post("", response_model=BookOut, status_code=201)
def create_book(book: Book):
    return services.add_book(book)


@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, updated: Book):
    return services.update_book(book_id, updated)


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int):
    return services.delete_book(book_id)
