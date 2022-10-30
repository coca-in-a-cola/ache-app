from marshmallow import Schema, fields

class TimeDeltaSchema(Schema):
    start = fields.DateTime()
    end = fields.DateTime()