from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(ge=0, le=2100)


class Book(BookCreate):
    id: int = Field(ge=1)
