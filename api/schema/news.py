from marshmallow import Schema, fields

class NewsEntrySchema(Schema):
    uuid = fields.String()
    url = fields.String()
    title = fields.String()
    created = fields.DateTime()
    