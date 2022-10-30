from marshmallow import Schema, fields
from api.schema.meta import MetaSchema


class ParticipantSchema(MetaSchema):
    userUUID = fields.String()
    # eventUUID = fields.String()
    status = fields.Integer()


class EventSchema(MetaSchema):
    auth_key_id = fields.String()
    firstName = fields.String()
    middleName = fields.String()
    lastName = fields.String()

    name = fields.String()
    description = fields.String(allow_none=True)
    datetimeStart = fields.DateTime()
    datetimeEnd = fields.DateTime()

    organizerUUID = fields.String(allow_none=False)
    participants = fields.List(fields.Nested(ParticipantSchema))

