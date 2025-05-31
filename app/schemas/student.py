from pydantic import BaseModel, EmailStr, Field, ConfigDict

class Student(BaseModel):
    
    name: str = Field(
        ..., 
        min_length=2, 
        description="Full name of the student"
    )

    roll_number: str = Field(
        ..., 
        description="Unique roll number identifier for the student (alphanumeric)"
    )

    department: str = Field(
        ..., 
        min_length=2, 
        description="Department name"
    )

    semester: int = Field(
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

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "John Doe",
                    "roll_number": "A12345",
                    "department": "CS",
                    "semester": 3,
                    "phone": "1234567890",
                    "email": "john.doe@example.com"
                }
            ]
        }
    )
