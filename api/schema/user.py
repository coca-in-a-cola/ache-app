from marshmallow import Schema, fields
from api.schema.meta import MetaSchema
from api.schema.timeDelta import TimeDeltaSchema

selectUserSchemaAuthKeyId = lambda user: user['auth_key_id']

class UserEventSchema(Schema):
    eventUUID = fields.String()
    status = fields.Integer()


class UserSchema(MetaSchema):
    auth_key_id = fields.String()
    firstName = fields.String()
    middleName = fields.String()
    lastName = fields.String()
    events = fields.List(fields.Nested(UserEventSchema))
    busyTime = fields.List(fields.Nested(TimeDeltaSchema))
    alertStatus = fields.Integer()