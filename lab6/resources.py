from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from db import collection
from flasgger import swag_from

parser = reqparse.RequestParser()
parser.add_argument(
    'title',
    type=str,
    required=True,
    help='Назва обовʼязкова',
    location='json'
)
parser.add_argument(
    'author',
    type=str,
    required=True,
    help='Автор обовʼязковий',
    location='json'
)


class BookListResource(Resource):
    @swag_from({
        'tags': ['Книги'],
        'description': 'Отримати всі книги',
        'responses': {
            200: {
                'description': 'Список усіх книг',
                'examples': {
                    'application/json': [
                        {
                            "_id": "507f1f77bcf86cd799439011",
                            "title": "1984",
                            "author": "George Orwell"
                        }
                    ]
                }
            }
        }
    })
    def get(self):
        """Отримати всі книги"""
        books = list(collection.find())
        for book in books:
            book['_id'] = str(book['_id'])
        return books, 200

    @swag_from({
        'tags': ['Книги'],
        'description': 'Додати нову книгу',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string', 'example': '1984'},
                        'author': {'type': 'string', 'example': 'George Orwell'}
                    },
                    'required': ['title', 'author']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Книгу успішно додано',
                'examples': {
                    'application/json': {
                        "message": "Книгу додано",
                        "id": "507f1f77bcf86cd799439011"
                    }
                }
            },
            400: {
                'description': 'Невірні вхідні дані'
            }
        }
    })
    def post(self):
        """Додати нову книгу"""
        try:
            args = parser.parse_args()
            if len(args['title']) > 100 or len(args['author']) > 50:
                return {"message": "Назва або автор занадто довгі"}, 400
            result = collection.insert_one({
                "title": args['title'],
                "author": args['author']
            })
            return {"message": "Книгу додано", "id": str(result.inserted_id)}, 201
        except Exception as e:
            return {"message": f"Помилка: {str(e)}"}, 400


class BookResource(Resource):
    @swag_from({
        'tags': ['Книги'],
        'description': 'Отримати книгу за ID',
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'ID книги'
            }
        ],
        'responses': {
            200: {
                'description': 'Дані книги',
                'examples': {
                    'application/json': {
                        "_id": "507f1f77bcf86cd799439011",
                        "title": "1984",
                        "author": "George Orwell"
                    }
                }
            },
            404: {
                'description': 'Книгу не знайдено'
            },
            400: {
                'description': 'Невірний ID книги'
            }
        }
    })
    def get(self, book_id):
        """Отримати книгу за ID"""
        try:
            book = collection.find_one({"_id": ObjectId(book_id)})
            if not book:
                return {"message": "Книгу не знайдено"}, 404
            book['_id'] = str(book['_id'])
            return book, 200
        except Exception:
            return {"message": "Невірний ID книги"}, 400

    @swag_from({
        'tags': ['Книги'],
        'description': 'Оновити книгу',
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'ID книги'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string', 'example': 'Нова назва'},
                        'author': {'type': 'string', 'example': 'Новий автор'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Книгу оновлено',
                'examples': {
                    'application/json': {
                        "message": "Книгу оновлено"
                    }
                }
            },
            404: {
                'description': 'Книгу не знайдено'
            },
            400: {
                'description': 'Невірні вхідні дані'
            }
        }
    })
    def put(self, book_id):
        """Оновити книгу"""
        try:
            args = parser.parse_args()
            result = collection.update_one(
                {"_id": ObjectId(book_id)},
                {"$set": {"title": args['title'], "author": args['author']}}
            )
            if result.matched_count == 0:
                return {"message": "Книгу не знайдено"}, 404
            return {"message": "Книгу оновлено"}, 200
        except Exception as e:
            return {"message": f"Помилка: {str(e)}"}, 400

    @swag_from({
        'tags': ['Книги'],
        'description': 'Видалити книгу',
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'ID книги'
            }
        ],
        'responses': {
            200: {
                'description': 'Книгу видалено',
                'examples': {
                    'application/json': {
                        "message": "Книгу видалено"
                    }
                }
            },
            404: {
                'description': 'Книгу не знайдено'
            },
            400: {
                'description': 'Невірний ID книги'
            }
        }
    })
    def delete(self, book_id):
        """Видалити книгу"""
        try:
            result = collection.delete_one({"_id": ObjectId(book_id)})
            if result.deleted_count == 0:
                return {"message": "Книгу не знайдено"}, 404
            return {"message": "Книгу видалено"}, 200
        except Exception:
            return {"message": "Невірний ID книги"}, 400
