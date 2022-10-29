from marshmallow import Schema, fields

class MapsSchema(Schema):
    uuid = fields.String()
    url = fields.String()
    title = fields.String()
    location = fields.String()
    