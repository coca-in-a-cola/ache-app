from marshmallow import Schema, fields

class TimeDeltaSchema(Schema):
    start = fields.DateTime()
    end = fields.DateTime()


class TimeDeltaPrivateSchema(Schema):
    start = fields.DateTime()
    end = fields.DateTime()
    name = fields.String()
    description = fields.String()