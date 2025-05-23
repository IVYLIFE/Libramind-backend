from typing import List, Optional
from fastapi import HTTPException

from app.schemas import Student, StudentOut
from app.database import STUDENTS


def add_student(student: Student) -> StudentOut:
    new_id = max((s.id for s in STUDENTS), default=0) + 1
    new_student = StudentOut(id=new_id, **student.dict())
    STUDENTS.append(new_student)
    return new_student


def list_students(
    department: Optional[str] = None,
    semester: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
) -> List[StudentOut]:
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


def get_student_by_identifier(identifier: str) -> StudentOut:
    id_lower = identifier.lower()
    for s in STUDENTS:
        if (
            s.name.lower() == id_lower
            or s.roll_number.lower() == id_lower
            or s.phone == identifier
        ):
            return s
    raise HTTPException(status_code=404, detail="Student not found")
