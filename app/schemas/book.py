from pydantic import BaseModel, Field, ConfigDict


class Book(BaseModel):
    title    : str = Field(min_length=3, description="Title of the book")
    author   : str = Field(min_length=3, description="Author of the book")
    isbn     : str = Field(min_length=10, max_length=13, description="ISBN of the book")
    category : str = Field(min_length=3, description="Category of the book")
    copies   : int = Field(ge=1, description="Number of copies available")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Sample Title",
                    "author": "Sample Author",
                    "isbn": "1234567890",
                    "category": "Sample Category",
                    "copies": 1,
                }
            ]
        }
    )


class BookOut(Book):
    id: int = Field(ge=1)

    class Config:
        from_attributes = True
