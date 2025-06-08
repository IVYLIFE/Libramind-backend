from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(13), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False)
    copies = Column(Integer)

    # Relationship to issued books
    issued_records = relationship("IssuedBookModel", back_populates="book")


# =====================================================================