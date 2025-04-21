from flask import jsonify, request
from app import app, db
from app.models import Book
from app.schemas import BookSchema
from marshmallow import ValidationError

book_schema = BookSchema()
books_schema = BookSchema(many=True)

def get_cursor(field, operator, value):
    if operator == 'gt':
        return Book.query.filter(field > value)
    elif operator == 'lt':
        return Book.query.filter(field < value)
    elif operator == 'gte':
        return Book.query.filter(field >= value)
    elif operator == 'lte':
        return Book.query.filter(field <= value)
    return Book.query

@app.route('/books', methods=['GET'])
def get_books():
    per_page = request.args.get('per_page', 10, type=int)
    cursor_id = request.args.get('cursor_id', None, type=int)
    cursor_op = request.args.get('cursor_op', 'gt', type=str)
    order_by = request.args.get('order_by', 'id', type=str)

    query = get_cursor(getattr(Book, order_by), cursor_op, cursor_id)
    books = query.order_by(getattr(Book, order_by)).limit(per_page).all()
    result = books_schema.dump(books)

    next_cursor_id = None
    if books:
        next_cursor_id = getattr(books[-1], order_by)

    return jsonify({
        'data': result,
        'next_cursor_id': next_cursor_id,
        'order_by': order_by
    })

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(book))

@app.route('/books', methods=['POST'])
def add_book():
    try:
        book_data = book_schema.load(request.get_json())
        new_book = Book(**book_data)
        db.session.add(new_book)
        db.session.commit()
        return jsonify(book_schema.dump(new_book)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': f'Книга з ID {book_id} видалена'}), 200