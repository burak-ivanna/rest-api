swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Бібліотечне API",
        "description": "API для управління книгами з використанням Flask-RESTful та MongoDB. Документація Swagger.",
        "version": "1.0.0",
        "contact": {
            "name": "ivanna",
            "email": "ivanna.burak.22@pnu.edu.ua"
        }
    },
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "tags": [
        {
            "name": "Книги",
            "description": "Операції з книгами"
        }
    ]
}
