from api.model.declarative_base import db
from flask import current_app
import uuid as _uuid


class Menu(db.Model):
    uuid = db.Column(db.String(32), primary_key = True)
    location = db.Column(db.Text())
    type = db.Column(db.String(30))
    goBack = db.Column(db.Boolean)
    goBackText = db.Column(db.Text())

    color = db.Column(db.Text())

    buttons = db.relationship("Button",
        backref="_menu",
        lazy='dynamic',
        cascade = "all, delete, delete-orphan" 
    )

    def __init__(self, buttons = [], uuid = None, **kwargs):
        if not uuid:
            # Нельзя генерировать UUID в шапке (...) функции, т.к. получится фиксированное значение
            uuid = str(_uuid.uuid4().hex)

        super().__init__(uuid = uuid, **kwargs)
        self.buttons = [Button(**button, menu_uuid = uuid) for button in buttons]


class Button(db.Model):
    uuid = db.Column(db.String(32), primary_key = True)
    icon = db.Column(db.Text())
    link = db.Column(db.Text())
    detail = db.Column(db.Text())
    text = db.Column(db.Text())
    onClick = db.Column(db.Text())
    menu_uuid = db.Column(db.String(32), db.ForeignKey('menu.uuid'))

    def __init__(self, uuid = None, **kwargs):
        if not uuid:
            #Нельзя генерировать UUID в шапке функции, т.к. получится фиксированное значение
            uuid = str(_uuid.uuid4().hex)

        super().__init__(uuid = uuid, **kwargs)