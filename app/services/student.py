from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from typing import List, Union
from datetime import date
import json

from app.models import BookModel, StudentModel
from app.schemas import Student, BookIssueRecord


def list_students( 
    department: str, 
    semester: int, 
    search: str, 
    page: int, 
    limit: int,
    db: Session
) -> tuple[list[Student], dict]:
    try:
        query = select(StudentModel)

        if department: query = query.filter(StudentModel.department.ilike(f"%{department}%"))
        if semester: query = query.filter(StudentModel.semester == semester)
        if search:
            search = f"%{search.lower()}%"
            query = query.filter(
                StudentModel.name.ilike(search) |
                StudentModel.roll_number.ilike(search) |
                StudentModel.phone.ilike(search)
            )

        total = db.scalar(select(func.count()).select_from(query.subquery()))

        students_orm = db.execute(
            query.offset((page - 1) * limit).limit(limit)
        ).scalars().all()

        students = [Student.model_validate(s) for s in students_orm]

        filters = {
            k: v for k, v in {
                "department": department,
                "semester": semester,
                "search": search
            }.items() if v not in (None, "")
        }


        meta_info = {
            "page": page,
            "limit": limit,
            "total_students": total,
            "fetched_count": len(students),
            "filters_applied": filters
        }

        return students, meta_info

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Server error. Please try again later."
        )



def get_student_by_identifier(
    identifier: str, 
    db: Session,
    as_orm: bool = False
) -> Union[StudentModel, Student]:
    print(f"\n\n=========== [get_student_by_identifier({identifier})] ===========\n")
    try:
        id_lower = identifier.lower()
        
        query = select(StudentModel).where(
            (func.lower(StudentModel.name) == id_lower) |
            (func.lower(StudentModel.roll_number) == id_lower) |
            (StudentModel.phone == identifier)
        )
        student = db.execute(query).scalars().first()

        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student not found for identifier = {identifier}"
                )

        if as_orm:
            print("Student ORM : ", student)
            print(f"\n\n=============================================\n")
            return student

        # Convert ORM model to Pydantic schema (Student)
        student = Student.model_validate(student)
        print("Student pdantic scheme : ", student)
        print(f"\n\n=============================================\n")
        return student


    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while fetching the student"
        )
    


def add_student(student: Student, db: Session) -> bool:
    """
    Add a student to the database after checking for duplicates
    by roll number, name, or phone number.
    Args:
        student (Student): The student data to add.
        db (Session): SQLAlchemy session for DB access.

    Returns: bool: True if student added successfully.
    Raises: HTTPException: 400 for duplicates, 500 for server error.
    """

    new_student = StudentModel(**student.model_dump())

    try:
        db.add(new_student)
        db.commit()
        return True

    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig).lower()

        # Collect all fields that caused the uniqueness constraint violation
        duplicate_fields = []
        if "roll_number" in error_msg:
            duplicate_fields.append(("roll number", student.roll_number))
        if "email" in error_msg:
            duplicate_fields.append(("email", student.email))
        if "phone" in error_msg:
            duplicate_fields.append(("phone", student.phone))

        if not duplicate_fields:
            raise HTTPException(
                status_code=400,
                detail="Student with given data already exists."
            )

        # Create a detailed error message
        error_details = ", ".join([f"{field}: {value}" for field, value in duplicate_fields])
        raise HTTPException(
            status_code=400,
            detail=f"Student with the following duplicate fields already exists: {error_details}."
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while adding the student."
        )



def get_student_books(identifier: str, db: Session) -> List[BookIssueRecord]:
    
    student = get_student_by_identifier(identifier, db, as_orm=True)

    try:
        print("1")
        issued_books = student.issued_books
        print("2")
        return [BookIssueRecord.model_validate(book) for book in issued_books]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching issued books"
        )



def return_book(
    identifier: str,
    issued_book_id: int,
    db: Session
) -> BookIssueRecord:
    

    student = get_student_by_identifier(identifier, db, as_orm=True)

    # Find the specific issued book by ID from the student's issued books
    issued_book = next((book for book in student.issued_books if book.id == issued_book_id), None)

    if not issued_book:
        raise HTTPException(status_code=404, detail="Issued book not found")

    if issued_book.returned_date:
        raise HTTPException(status_code=400, detail="Book has already been returned")

    try:
        # Update the returned date to today
        issued_book.returned_date = date.today()

        # Increase the book's available copies
        book = db.query(BookModel).filter(BookModel.id == issued_book.book_id).first()
        # book = get_single_book(str(issued_book.book_id), db, as_orm=True)

        if book:
            book.copies += 1

        db.commit()
        db.refresh(issued_book)

        return BookIssueRecord.model_validate(issued_book)
       

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while returning the book"
        )
