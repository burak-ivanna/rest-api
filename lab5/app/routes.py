from fastapi import APIRouter, HTTPException
from app.database import books_collection
from app.models import Book
from app.schemas import BookCreate
from pydantic_mongo import ObjectIdField
from bson import ObjectId

router = APIRouter()


@router.get("/books", response_model=list[Book])
async def get_books():
    books_cursor = books_collection.find({})
    books = []
    async for book in books_cursor:
        books.append(Book(**book))
    return books


@router.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(**book)


@router.post("/books", response_model=Book)
async def create_book(book_data: BookCreate):
    book_dict = book_data.dict()
    result = await books_collection.insert_one(book_dict)
    book_dict["_id"] = result.inserted_id
    return Book(**book_dict)


@router.delete("/books/{book_id}")
async def delete_book(book_id: str):
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}
