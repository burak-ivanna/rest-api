from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=120))
    author = fields.String(required=True, validate=validate.Length(max=120))
    publication_date = fields.DateTime(dump_only=True)