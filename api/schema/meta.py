from marshmallow import Schema, fields


selectMetaSchemaUUID = lambda meta: meta['uuid']

class MetaDataSchema(Schema):
    uuid = fields.String()
    type = fields.String()
    

class MetaSchema(Schema):
    uuid = fields.Nested(MetaDataSchema)
