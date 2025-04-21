from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from resources import BookResource, BookListResource
from swagger_config import swagger_template
from db import db

app = Flask(__name__)
api = Api(app)

swagger = Swagger(app, template=swagger_template)

api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<string:book_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
