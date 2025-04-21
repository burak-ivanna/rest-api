from marshmallow import Schema, fields, validate


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    author = fields.Str(
        required=True, validate=validate.Length(min=1, max=100))
    year = fields.Int(
        required=True, validate=validate.Range(min=1000, max=2100))
