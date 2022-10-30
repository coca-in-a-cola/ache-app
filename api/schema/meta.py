from marshmallow import Schema, fields


selectUUID = lambda meta: meta['uuid']

class MetaSchema(Schema):
    uuid = fields.String()
    type = fields.String()
    metaHref = fields.String()