from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    roll_number = Column(String(20), nullable=False, unique=True)
    department = Column(String(50), nullable=False)
    semester = Column(Integer, nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    # Relationship to issued books
    issued_books = relationship("IssuedBookModel", back_populates="student")


# =====================================================================