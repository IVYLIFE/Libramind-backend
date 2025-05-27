from pydantic import BaseModel, Field


class Book(BaseModel):
    title    : str = Field(min_length=3)
    author   : str = Field(min_length=3)
    isbn     : str = Field(min_length=10, max_length=13)
    category : str = Field(min_length=3)
    copies   : int = Field(ge=1)


class BookOut(Book):
    id: int = Field(ge=1)

    class Config:
        from_attributes = True
