from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    name: str
    roll_number: str
    department: str
    semester: int
    phone: str
    email: EmailStr

class StudentOut(Student):
    id: int

    class Config:
        from_attributes = True
