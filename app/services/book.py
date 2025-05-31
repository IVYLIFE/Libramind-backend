# book.py
from fastapi import HTTPException

from datetime import date, timedelta
import json

from app.schemas import Book, BookOut, BookIssueRecord, IssueBook
from app.database import BOOKS, ISSUED_BOOKS
from app.services.student import get_student_by_identifier


def list_books(title, author, category, page, limit) -> tuple[list[BookOut], dict]:
    try:
        filtered = BOOKS

        filters = {}
        if title:
            filtered = [book for book in filtered if title.lower() in book.title.lower()]
            filters["title"] = title
        if author:
            filtered = [book for book in filtered if author.lower() in book.author.lower()]
            filters["author"] = author
        if category:
            filtered = [book for book in filtered if category.lower() in book.category.lower()]
            filters["category"] = category

        start = (page - 1) * limit
        books = filtered[start : start + limit]

        meta_info = {
            "page": page,
            "limit": limit,
            "total_books": len(filtered),
            "fetched_count": len(books),
            "filters_applied": filters
        }

        return books, meta_info

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Server error. Please try again later."
        )



def get_single_book(book_id: int) -> BookOut:
    try:
        for book in BOOKS:
            if book.id == book_id:
                return book

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching the book")

    raise HTTPException(status_code=404, detail="Book not found")



def add_book(book: Book) -> dict:
    try:
        for existing_book in BOOKS:
            if(existing_book.isbn == book.isbn) :
                if (
                    existing_book.title == book.title and
                    existing_book.author == book.author and
                    existing_book.category == book.category
                ):
                    existing_book.copies += book.copies
                    return {
                        "updated": True,
                        "book": existing_book
                    }
                else:
                    raise HTTPException(
                        status_code=409,
                        detail="ISBN already belongs to a different book"
                    )

        new_id = max((book.id for book in BOOKS), default=0) + 1
        new_book = BookOut(id=new_id, **book.model_dump())
        BOOKS.append(new_book)

        return {
            "updated": False,
            "book": new_book
        }
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while adding the book")
    


def update_book(book_id: int, updated: Book) -> BookOut:
    try:
        for idx, book in enumerate(BOOKS):
            if book.id == book_id:
                updated_book = BookOut(id=book_id, **updated.model_dump())
                BOOKS[idx] = updated_book
                return updated_book

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while updating the book"
        )

    raise HTTPException(status_code=404, detail="Book not found")



def delete_book( book_id: int ) -> bool:
    try:
        for idx, book in enumerate(BOOKS):
            if book.id == book_id:
                del BOOKS[idx]
                return True
 
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while updating the book: {str(e)}"
        )
    
    raise HTTPException(status_code=404, detail="Book not found")



def issue_book(book_id: int, payload: IssueBook) -> BookIssueRecord:
    # Check if book exists
    book = get_single_book(book_id)

    # Check for available copies
    if book.copies <= 0:
        raise HTTPException(
            status_code=400, detail="No available copies for this book."
        )
    
    # Check if student exists
    student = get_student_by_identifier(payload.student_id)

    try:
        already_issued = any(
            issued_book.id == book.id and
            issued_book.student_roll_number == student.roll_number and
            issued_book.returned_date is None
            for issued_book in ISSUED_BOOKS
        )
        if already_issued:
            raise HTTPException(status_code=400, detail="This book is already issued to the student")

        issue_date = date.today()
        due_date = issue_date + timedelta(days=payload.duration_days)

        issued_book = BookIssueRecord(
            id=len(ISSUED_BOOKS) + 1,
            book_id=book.id,
            student_roll_number=student.roll_number,
            issue_date=issue_date,
            due_date=due_date,
            returned_date=None,
        )

        ISSUED_BOOKS.append(issued_book)

        book.copies -= 1 
        return issued_book
    

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while issuing the book"
        )

