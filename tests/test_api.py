import pytest
from fastapi.testclient import TestClient

from app.main import app, books

client = TestClient(app)

VALID_BOOK = {"title": "Les Misérables", "author": "Victor Hugo", "year": 1862}


@pytest.fixture(autouse=True)
def clear_books():
    # Clear the books list before each test
    books.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}  


def test_add_book():
    response = client.post("/books", json=VALID_BOOK)
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["title"] == VALID_BOOK["title"]


def test_add_invalid_book():
    invalid_book = {"title": "", "author": "Author", "year": 2020}
    response = client.post("/books", json=invalid_book)
    assert response.status_code == 422


def test_get_books():
    # Add a book first
    client.post("/books", json=VALID_BOOK)
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_book_by_id():
    # Add a book first
    client.post("/books", json=VALID_BOOK)
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_nonexistent_book():
    response = client.get("/books/999")
    assert response.status_code == 404
