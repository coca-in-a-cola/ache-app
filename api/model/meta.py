from flask import Flask, request
from api.model.declarative_base import db
import uuid as _uuid
from api.schema.meta import MetaSchema, selectUUID

def get_meta(metaSchema: MetaSchema):
    try:
        metaSchema = metaSchema.load(metaSchema)
    except Exception as ex:
        raise("Неверно указаны метаданные: " + ex)
    
    return Meta.query.get(selectUUID(metaSchema))


class Meta(db.Model):
    __tablename__ = 'meta'
    
    uuid = db.Column(db.String, primary_key=True, index=True)
    type = db.Column(db.String(50))
    metaHref = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity':'meta',
        'polymorphic_on': type
    }


    def __init__(self, uuid = None, **kwargs):
        if not uuid:
            # Нельзя генерировать UUID в шапке (...) функции, т.к. получится фиксированное значение
            uuid = str(_uuid.uuid4().hex)
        
        self.metaHref = f"{request.host_url}{self.type}/{uuid}"

        super().__init__(uuid = uuid, **kwargs)