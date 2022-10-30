from tokenize import Number
from api.model.declarative_base import db
from api.model.meta import Meta, get_meta

from datetime import datetime

from api.schema.meta import MetaSchema


class EventUser(db.Model):
    __tablename__ = 'eventUser'

    userUUID = db.Column(db.String, db.ForeignKey('meta.uuid'), primary_key=True)
    eventUUID = db.Column(db.String, db.ForeignKey('meta.uuid'), primary_key=True)
    status = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity':'entity/eventUser',
    }

    def __init__(self, userUUID: str = None, eventUUID: str = None, status: Number = 1, **kwargs):
        self.userUUID = userUUID
        self.eventUUID = eventUUID
        self.status = status

        super().__init__(**kwargs)


class Event(Meta):
    __tablename__ = 'event'

    name = db.Column(db.String)
    description = db.Column(db.String, nullable=True)
    datetimeStart = db.Column(db.DateTime)
    datetimeEnd = db.Column(db.DateTime)

    organizerUUID = db.Column(db.String)

    participants = db.relationship("EventUser",
         lazy='dynamic', cascade = "all, delete, delete-orphan", foreign_keys="EventUser.eventUUID")

    __mapper_args__ = {
        'polymorphic_identity':'entity/event',
    }

    def __init__(self, name: str = None, description: str = None,
        datetimeStart: str = None, datetimeEnd: str = None, organizerUUID : str = None,
        participants : list = [], **kwargs):
        self.name = name
        self.description = description
        self.organizerUUID = organizerUUID
        self.datetimeStart = datetimeStart
        self.datetimeEnd = datetimeEnd
        # [userEvent(participant, MetaSchema.load(self.meta)) for participant in participants]
        super().__init__(**kwargs)

        self.participants = [EventUser(**pt, eventUUID=self.uuid) for pt in participants]