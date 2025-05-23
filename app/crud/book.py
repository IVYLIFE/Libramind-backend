# crud.py
from fastapi import HTTPException
from typing import List, Optional


from app.schemas import Book, BookOut
from app.database import BOOKS


def list_books(
    title    : Optional[str] = None,
    author   : Optional[str] = None,
    category : Optional[str] = None,
    page     : int           = 1,
    limit    : int           = 10,
) -> List[BookOut]:

    filtered = BOOKS

    if title:
        filtered = [book for book in filtered if title.lower() in book.title.lower()]
    if author:
        filtered = [book for book in filtered if author.lower() in book.author.lower()]
    if category:
        filtered = [
            book for book in filtered if category.lower() in book.category.lower()
        ]

    start = (page - 1) * limit
    return filtered[start : start + limit]


def get_book(book_id: int) -> BookOut:
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


def add_book(book: Book) -> BookOut:
    new_id = max((book.id for book in BOOKS), default=0) + 1
    new_book = BookOut(id=new_id, **book.model_dump())
    BOOKS.append(new_book)
    return new_book


def update_book(book_id: int, updated: Book) -> BookOut:
    for idx, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS[idx] = BookOut(id=book_id, **updated.model_dump())
            return BOOKS[idx]
    raise HTTPException(status_code=404, detail="Book not found")


def delete_book(book_id: int):
    for idx, book in enumerate(BOOKS):
        if book.id == book_id:
            del BOOKS[idx]
            return
    raise HTTPException(status_code=404, detail="Book not found")
