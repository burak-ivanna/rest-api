from .models import books
from .schemas import BookSchema, BookCreateSchema
from typing import Optional


def get_all_books() -> list[BookSchema]:
    return books.copy()


def get_book_by_id(book_id: int) -> Optional[BookSchema]:
    return next((book for book in books if book["id"] == book_id), None)


def add_book(book_data: BookCreateSchema) -> BookSchema:
    new_id = max(book["id"] for book in books) + 1 if books else 1
    new_book = {
        "id": new_id,
        "title": book_data.title,
        "author": book_data.author,
        "year": book_data.year
    }
    books.append(new_book)
    return new_book


def delete_book(book_id: int) -> bool:
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(i)
            return True
    return False
