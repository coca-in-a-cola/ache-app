from marshmallow import Schema, fields

class ButtonSchema(Schema):
    uuid = fields.String()
    icon = fields.String(allow_none=True)
    link = fields.String(allow_none=True)
    detail = fields.String(allow_none=True)
    text = fields.String()
    onClick = fields.String(allow_none=True)


class MenuSchema(Schema):
    uuid = fields.String()
    location = fields.String()
    type = fields.String()
    goBack = fields.Bool()
    goBackText = fields.String(allow_none=True)
    buttons = fields.List(fields.Nested(ButtonSchema))
    color = fields.String(allow_none=True)