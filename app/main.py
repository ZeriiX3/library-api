from fastapi import FastAPI, HTTPException

from app.models import BookCreate, Book
from app.database import init_db, insert_book, select_book_by_id, select_books


# ---------------------------------------------------------------------------- #


app = FastAPI(title="Library API")
init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/books", response_model=Book, status_code=201)
def add_book(book: BookCreate):
    book_id = insert_book(book.title, book.author, book.year)
    return Book(id=book_id, title=book.title, author=book.author, year=book.year)


@app.get("/books", response_model=list[Book])
def get_books():
    return select_books()


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = select_book_by_id(book_id)
    # Unknown id: return a 404 error
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
