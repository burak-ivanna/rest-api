from flask import Blueprint, request, jsonify
from .models import books, Book
from .schemas import BookSchema

book_routes = Blueprint('book_routes', __name__)

book_schema = BookSchema()
books_schema = BookSchema(many=True)


@book_routes.route('/books', methods=['GET'])
def get_books():
    return jsonify(books_schema.dump(books))


@book_routes.route('/books/<int:id>', methods=['GET'])
def get_book_by_id(id):
    book = next((book for book in books if book['id'] == id), None)
    if book is None:
        return jsonify({"message": "Book not found"}), 404
    return jsonify(book_schema.dump(book))


@book_routes.route('/books', methods=['POST'])
def add_book():
    try:
        data = book_schema.load(request.json)
    except Exception as e:
        return jsonify({"message": "Invalid data", "error": str(e)}), 400

    new_book = Book(id=data['id'], title=data['title'],
                    author=data['author'], year=data['year'])
    books.append(new_book.__dict__)
    return jsonify(book_schema.dump(new_book)), 201


@book_routes.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    global books
    books = [book for book in books if book['id'] != id]
    return jsonify({"message": "Book deleted successfully"}), 200
