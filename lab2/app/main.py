from fastapi import FastAPI, HTTPException
from .models import books
from .schemas import BookSchema, BookCreateSchema
from .services import (
    get_all_books,
    get_book_by_id,
    add_book,
    delete_book
)

app = FastAPI()


@app.get("/books/", response_model=list[BookSchema])
async def read_books():
    return get_all_books()


@app.get("/books/{book_id}", response_model=BookSchema)
async def read_book(book_id: int):
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books/", response_model=BookSchema, status_code=201)
async def create_book(book: BookCreateSchema):
    return add_book(book)


@app.delete("/books/{book_id}", status_code=204)
async def remove_book(book_id: int):
    if not delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return None
