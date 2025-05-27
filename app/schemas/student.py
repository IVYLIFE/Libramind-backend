from pydantic import BaseModel, EmailStr, Field

class Student(BaseModel):
    
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=100, 
        description="Full name of the student"
    )

    roll_number: str = Field(
        ..., 
        description="Unique roll number identifier for the student (alphanumeric)"
    )

    department: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        description="Department name"
    )

    semester: str = Field(
        ...,
        description="Semester (1 to 8)"
    )

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="Phone number (10-15 digits, optional country code)",
    )
    
    email: EmailStr = Field(..., description="Valid email address")

    class Config:
        from_attributes = True
