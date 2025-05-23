from typing import List
from app.schemas.student import StudentOut


STUDENTS: List[StudentOut] = [
    # Example data
    StudentOut(id=1, name="Alice", roll_number="101", department="CS", semester=3, phone="1234567890", email="alice@example.com"),
    StudentOut(id=2, name="Bob", roll_number="102", department="EE", semester=2, phone="0987654321", email="bob@example.com"),
]