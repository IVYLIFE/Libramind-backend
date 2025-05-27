from typing import List, Optional
from fastapi import HTTPException

from app.schemas import Student, IssuedBookOut
from app.database import STUDENTS, ISSUED_BOOKS, BOOKS


def list_students(
    department: Optional[str] = None,
    semester: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
) -> List[Student]:
    filtered = STUDENTS

    if department:
        filtered = [s for s in filtered if s.department.lower() == department.lower()]
    if semester:
        filtered = [s for s in filtered if s.semester == semester]
    if search:
        lower_search = search.lower()
        filtered = [
            s
            for s in filtered
            if lower_search in s.name.lower()
            or lower_search in s.roll_number.lower()
            or lower_search in s.phone
        ]
    start = (page - 1) * limit
    return filtered[start : start + limit]



def get_student_by_identifier(identifier: str) -> Student:
    id_lower = identifier.lower()
    print(f"Searching for student with identifier: {identifier} (lowercase: {id_lower})")
    for s in STUDENTS:
        if (
            s.name.lower() == id_lower
            or s.roll_number.lower() == id_lower
            or s.phone == identifier
        ):
            return s
    raise HTTPException(status_code=404, detail="Student not found")



def add_student(student: Student) -> Student:

    duplicate_fields = {}

    for existing in STUDENTS:
        if existing.roll_number.lower() == student.roll_number.lower():
            duplicate_fields["roll number"] = student.roll_number
        if existing.name.lower() == student.name.lower():
            duplicate_fields["name"] = student.name
        if existing.phone == student.phone:
            duplicate_fields["phone"] = student.phone

    if duplicate_fields:
        fields_str = ", ".join([f"{label}: {value}" for label, value in duplicate_fields.items()])
        raise HTTPException(
            status_code=400,
            detail=f"Student with {fields_str} already exists."
        )

    # Add the new student if no duplicate is found
    new_student = Student(**student.model_dump())
    STUDENTS.append(new_student)
    return new_student



def get_student_books(identifier: str) -> List[IssuedBookOut]:
    # Find student by name or roll number or phone (case insensitive for strings)
    student = None
    id_lower = identifier.lower()
    for s in STUDENTS:
        if (
            s.name.lower() == id_lower or
            s.roll_number.lower() == id_lower or
            s.phone == identifier
        ):
            student = s
            break
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Find issued books for that student
    issued = [
        ib for ib in ISSUED_BOOKS if ib.student_roll_number == student.roll_number
    ]

    # Build list of IssuedBookOut with book info + due_date
    result = []
    for ib in issued:
        book = next((b for b in BOOKS if b.id == ib.book_id), None)
        if book:
            result.append(IssuedBookOut(book=book, due_date=ib.due_date))
    return result