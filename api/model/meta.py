from flask import Flask
from api.model.declarative_base import db
import uuid as _uuid



class Meta(db.Model):
    __tablename__ = 'meta'


    uuid = db.Column(db.String, primary_key=True, index=True)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'meta',
        'polymorphic_on':type
    }


    def __init__(self, uuid = None, **kwargs):
        if not uuid:
            # Нельзя генерировать UUID в шапке (...) функции, т.к. получится фиксированное значение
            uuid = str(_uuid.uuid4().hex)

        super().__init__(uuid = uuid, **kwargs)