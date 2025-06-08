# book.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from typing import Union
from datetime import date, timedelta

from app.models import BookModel, IssuedBookModel
from app.schemas import Book, BookOut, BookIssueRecord, IssueBook
from app.services.student import book_issue_record_schema, get_student_by_identifier
from app.utils.utils import check_is_isbn


def list_books(
    title: str, 
    author: str, 
    category: str, 
    page: int, 
    limit: int, 
    db: Session
) -> tuple[list[BookOut], dict]:
    try:
        query = select(BookModel)

        if title: query = query.filter(BookModel.title.ilike(f"%{title}%"))
        if author: query = query.filter(BookModel.author.ilike(f"%{author}%"))
        if category: query = query.filter(BookModel.category.ilike(f"%{category}%"))

        total = db.scalar(select(func.count()).select_from(query.subquery()))

        books = db.execute(query.offset((page - 1) * limit).limit(limit)).scalars().all()
        books = [BookOut.model_validate(book) for book in books]

        meta_info = {
            "page": page,
            "limit": limit,
            "total_books": total,
            "fetched_count": len(books),
            "filters_applied": {
                k: v for k, v in {
                    "title": title,
                    "author": author,
                    "category": category
                }.items() if v
            }
        }

        return books, meta_info

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Server error. Please try again later."
        )



def get_single_book(
    book_id: str,
    db: Session,
    as_orm: bool = False
) -> Union[BookModel, BookOut]:
    """
    Fetch a single book by ID or ISBN from the database.
    Args:
        book_id (str): The book identifier, either numeric ID or string ISBN.
        as_orm (bool): This decide the result type
        db (Session): SQLAlchemy database session.

    Returns: Union[BookModel, BookOut]: Book schema or Book Model.
    Raises:
        HTTPException 404 if no book found.
        HTTPException 500 on server error.
    """

    try:

        book_id = book_id.replace("-", "").strip()
        
        if check_is_isbn(book_id):
            query = select(BookModel).where(BookModel.isbn == book_id)
            key = "isbn"
        else:
            query = select(BookModel).where(BookModel.id == int(book_id))
            key = "id"


        book = db.execute(query).scalars().first()

        if not book:
            raise HTTPException(
                status_code=404,
                detail=f"No book found with {key.upper()}: {book_id}"
            )
        
        if as_orm:
            return book

        # Convert ORM model to Pydantic schema (BookOut)
        book = BookOut.model_validate(book)
        return book


    except HTTPException:
        raise
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching the book")



def add_book(book: Book, db: Session) -> dict:
    """
    Add a new book to the database or update copies if it already exists.
    Args:
        book (BookCreate): Book input schema.
        db (Session): SQLAlchemy DB session.

    Returns: dict: Result indicating whether the book was updated or newly added.
    Raises: HTTPException: On ISBN conflict or DB errors.
    """

    try:
        # 1. Check if book already exists by ISBN
        query = select(BookModel).where((BookModel.isbn == book.isbn))
        existing_book = db.execute(query).scalars().first()

        if existing_book:
            # 2. If title/author/category match → increase copies
            if (
                existing_book.title == book.title and
                existing_book.author == book.author and
                existing_book.category == book.category
            ):
                existing_book.copies += book.copies
                db.commit()
                db.refresh(existing_book)

                return {
                    "updated": True,
                    "book": BookOut.model_validate(existing_book)
                }
            else:
                # 3. Same ISBN but different metadata = conflict
                raise HTTPException(
                    status_code=409,
                    detail="ISBN already belongs to a different book"
                )

        # 4. Create new book entry
        new_book = BookModel(**book.model_dump())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return {
            "updated": False,
            "book": BookOut.model_validate(new_book)
        }
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while adding the book")
    


def update_book(
    book_id: str, 
    book_to_update: Book, 
    db: Session
) -> BookOut:
    """
    Update a book by ID or ISBN with new data.
    Args:
        book_id (str): Book ID or ISBN.
        updated (Book): Updated book data.
        db (Session): Database session.

    Returns: BookOut: Updated book data.
    Raises: HTTPException: If book not found or update fails.
    """

    # Get ORM instance for update
    book_orm = get_single_book(book_id, db, as_orm=True)
    try:

        # Update fields on ORM model
        for field, value in book_to_update.model_dump().items():
            if field == "isbn":
            # Skip updating ISBN
                continue

            setattr(book_orm, field, value)

        db.commit()
        db.refresh(book_orm)

        # Return Pydantic schema after update
        return BookOut.model_validate(book_orm)

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while updating the book"
        )



def delete_book(book_id: str, db: Session) -> bool:
    """
    Delete a book by ID or ISBN.
    Args:
        book_id (str): Book ID or ISBN.
        db (Session): Database session.

    Returns: bool: True if deleted.
    Raises: HTTPException: If book not found or deletion fails.
    """
    
    book_orm = get_single_book(book_id, db, as_orm=True)

    try:
        db.delete(book_orm)
        db.commit()
        return True
 
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while updating the book: {str(e)}"
        )
    


def issue_book(
    book_id: str,
    payload: IssueBook,
    db: Session
) -> BookIssueRecord:
    
    """
    Issues a book to a student if available.
    Args:
        book_id (str): ID or ISBN of the book to issue.
        payload (IssueBook): Student ID and issue duration.
        db (Session): Active database session.

    Returns: BookIssueRecord: Details of the issued book record.
    Raises: HTTPException: If book/student not found, already issued, or DB error occurs.
    """

    print(f"""\n\n=========== [issue_book({book_id} {payload})] ===========\n""")

    # Check if book exists
    book = get_single_book(book_id, db, as_orm=True)
    

    # Check for available copies
    if book.copies <= 0:
        raise HTTPException(
            status_code=400, 
            detail="No available copies for this book."
        )
    
    # Check if student exists
    student = get_student_by_identifier(payload.student_id, db, as_orm=True)

    try:

        # Check if already issued to the student
        already_issued = db.query(IssuedBookModel).filter(
            IssuedBookModel.book_id == book.id,
            IssuedBookModel.student_id == student.id,
            IssuedBookModel.returned_date.is_(None)
        ).first()
        
        if already_issued:
            raise HTTPException(
                status_code=400, 
                detail="This book is already issued to the student"
            )

        issue_date = date.today()
        due_date = issue_date + timedelta(days=payload.duration_days)

        issued_book = IssuedBookModel(
            book_id=book.id,
            student_id=student.id,
            issue_date=issue_date,
            due_date=due_date,
            returned_date=None,
        )

        db.add(issued_book)
        book.copies -= 1
        db.commit()

        db.refresh(issued_book)

        return book_issue_record_schema(issued_book)

    

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while issuing the book"
        )



def get_overdue_books(db: Session) -> list[BookIssueRecord]:
    """
    Fetch all books that are currently overdue (not returned and past due date).

    Args:
        db (Session): Active database session.

    Returns:
        List[BookIssueRecord]: List of overdue issued books with is_overdue = True

    Raises:
        HTTPException: If any unexpected database error occurs.
    """

    print(f"\n\n\n get_overdue_books() \n\n\n")
    try:
        overdue_books = db.query(IssuedBookModel).filter(
            IssuedBookModel.returned_date.is_(None),
            IssuedBookModel.due_date < date.today()
        ).all()

        print(overdue_books)
        return [book_issue_record_schema(book) for book in overdue_books]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching overdue books"
        )


# =====================================================================