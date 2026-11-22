from fastapi import FastAPI, HTTPException
from app.models import BookCreate, Book

app = FastAPI(title="Library API")

books = []  # In-memory storage for books


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/books", response_model=Book, status_code=201)
def add_book(book: BookCreate):
    # For now, we will save the books in memory
    new_book = Book(
        id= len(books) + 1,
        title= book.title,
        author= book.author,
        year= book.year,
    )
    books.append(new_book)
    return new_book

@app.get("/books", response_model=list[Book])
def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")