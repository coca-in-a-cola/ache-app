from marshmallow import Schema, fields
from api.schema.meta import MetaSchema

selectUserSchemaAuthKeyId = lambda user: user['auth_key_id']

class UserSchema(MetaSchema):
    auth_key_id = fields.String()
    firstName = fields.String()
    middleName = fields.String()
    lastName = fields.String()
