# book.py
from fastapi import HTTPException

from app.schemas import Book, BookOut
from app.database import BOOKS


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
        paged_books = filtered[start : start + limit]
        books = [book.model_dump() for book in paged_books]

        meta_info = {
            "page": page,
            "limit": limit,
            "total_books": len(filtered),
            "fetched_count": len(paged_books),
            "filters_applied": filters
        }

        return books, meta_info

    except Exception as e:
        raise RuntimeError(f"Database or service failure: {str(e)}")



def get_book( book_id: int ) -> dict:
    for book in BOOKS:
        if book.id == book_id:
            return book.model_dump()
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
                        "book": existing_book.model_dump()
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
            "book": new_book.model_dump()
        }

    except Exception as e:
        raise e



def update_book(book_id: int, updated: Book) -> dict:
    try:
        for idx, book in enumerate(BOOKS):
            if book.id == book_id:
                updated_book = BookOut(id=book_id, **updated.model_dump())
                BOOKS[idx] = updated_book
                return updated_book.model_dump()

        raise HTTPException(status_code=404, detail="Book not found")

    except HTTPException as he:
        raise he
 
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while updating the book: {str(e)}"
        )



def delete_book( book_id: int ) -> dict:
    try:
        for idx, book in enumerate(BOOKS):
            if book.id == book_id:
                del BOOKS[idx]
                return True

        raise HTTPException(status_code=404, detail="Book not found")

    except HTTPException as he:
        raise he
 
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while updating the book: {str(e)}"
        )
