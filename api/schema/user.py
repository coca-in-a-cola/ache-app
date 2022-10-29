from marshmallow import Schema, fields


class UserSchema(Schema):
    card_code = fields.Integer()
    fullname = fields.String()
    personnel_number = fields.Integer()
    subdivision = fields.String()
    position = fields.String()
    phone_number = fields.String()