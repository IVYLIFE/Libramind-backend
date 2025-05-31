from fastapi import HTTPException
from typing import List
from datetime import date
import json

from app.schemas import Student, BookIssueRecord
from app.database import BOOKS, STUDENTS, ISSUED_BOOKS


def list_students( 
    department: str, 
    semester: int, 
    search: str, 
    page: int, 
    limit: int 
) -> tuple[list[Student], dict]:
    print("2")
    try:
        filtered = STUDENTS

        filters = {}
        if department:
            filtered = [s for s in filtered if s.department.lower() == department.lower()]
            print("3")
            filters["department"] = department
        if semester:
            filtered = [s for s in filtered if s.semester == semester]
            print("4")
            filters["semester"] = semester
        if search:
            print("5")
            lower_search = search.lower()
            filtered = [
                s
                for s in filtered
                if lower_search in s.name.lower()
                or lower_search in s.roll_number.lower()
                or lower_search in s.phone
            ]
            filters["search_value"] = search

        start = (page - 1) * limit
        students = filtered[start : start + limit]


        meta_info = {
            "page": page,
            "limit": limit,
            "total_students": len(filtered),
            "fetched_count": len(students),
            "filters_applied": filters
        }

        return students, meta_info

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Server error. Please try again later."
        )



def get_student_by_identifier(identifier: str) -> Student:
    print(f"\n\n=========== [get_student_by_identifier({identifier})] ===========\n")
    try:
        id_lower = identifier.lower()
        for student in STUDENTS:
            if (
                student.name.lower() == id_lower or
                student.roll_number.lower() == id_lower or
                student.phone == identifier
            ):
                print("Student found")
                print(student.model_dump())
                print("\n========================================")
                return student
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while fetching the student"
        )
    
    raise HTTPException(status_code=404, detail=f"Student not found for identifier = {identifier}")



def add_student(student: Student) -> bool:
    try:
        duplicate_fields = {}

        for existing in STUDENTS:
            if existing.roll_number.lower() == student.roll_number.lower():
                duplicate_fields["roll number"] = student.roll_number
            if existing.name.lower() == student.name.lower():
                duplicate_fields["name"] = student.name
            if existing.phone == student.phone:
                duplicate_fields["phone"] = student.phone

        if duplicate_fields:
            fields_str = ", ".join(
                [f"{label}: {value}" for label, value in duplicate_fields.items()]
            )
            raise HTTPException(
                status_code=400, detail=f"Student with {fields_str} already exists."
            )

        STUDENTS.append(student)
        return True
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while adding the student")



def get_student_books(identifier: str) -> List[BookIssueRecord]:
    # Find student by name or roll number or phone (case insensitive for strings)
    student = get_student_by_identifier(identifier)

    # Find issued books for that student
    try:

        issued_books = [ 
            ib for ib in ISSUED_BOOKS 
            if ib.student_roll_number == student.roll_number
        ]

        return issued_books

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching issued books"
        )



def return_book(student_id: str, issued_book_id: int) -> BookIssueRecord:
    
    # Retrieve the student
    student = get_student_by_identifier(student_id)

    issued_books = get_student_books(student.roll_number)

    try:

        book_to_return = None
        for book in issued_books:
            if book.id == issued_book_id:
                book_to_return = book
                break


        if not book_to_return or book_to_return.returned_date:
            raise HTTPException(status_code=400, detail="No Books isued to the Student or Book has already been returned")

        # Update the returned date to today
        book_to_return.returned_date = date.today()
       
        # Increase the book's available copies
        for book in BOOKS:
            if book.id == book_to_return.book_id:
                book.copies += 1
                break

        return book_to_return

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while returning the book"
        )
