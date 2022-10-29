from api.model.declarative_base import db
from flask import current_app
from datetime import datetime
import uuid as _uuid


class Maps(db.Model):
    uuid = db.Column(db.String(32), primary_key = True)
    url = db.Column(db.Text())
    title = db.Column(db.Text())
    location = db.Column(db.Text())

    def __init__(self, uuid = None, location = "", **kwargs):
        if not uuid:
            uuid = str(_uuid.uuid4().hex)
        super().__init__(uuid = uuid, location = location, **kwargs)