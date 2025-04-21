from flask import Blueprint, request, jsonify
from app import db
from app.models import Book
from app.schemas import BookSchema

books_bp = Blueprint('books', __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)


@books_bp.route('/books', methods=['GET'])
def get_books():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    if limit < 1 or offset < 0:
        return jsonify({'error': 'Invalid pagination parameters'}), 400

    books = Book.query.order_by(Book.id).limit(limit).offset(offset).all()
    total = Book.query.count()

    return jsonify({
        'data': books_schema.dump(books),
        'meta': {
            'total': total,
            'limit': limit,
            'offset': offset
        }
    })


@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(book))


@books_bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    errors = book_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    book = Book(
        title=data['title'],
        author=data['author'],
        year=data['year']
    )
    db.session.add(book)
    db.session.commit()

    return jsonify(book_schema.dump(book)), 201


@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200
