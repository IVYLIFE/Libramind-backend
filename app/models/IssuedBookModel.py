from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class IssuedBookModel(Base):
    __tablename__ = "issued_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    returned_date = Column(Date, nullable=True)

    # Relationships to Book and Student
    student = relationship("StudentModel", back_populates="issued_books")
    book = relationship("BookModel", back_populates="issued_records")


# =====================================================================