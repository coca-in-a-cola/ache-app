from api.model.declarative_base import db
from api.model.meta import Meta


class BusyTime(db.Model):
    __tablename__ = 'busytime'

    userUUID = db.Column(db.String, db.ForeignKey('meta.uuid'), primary_key = True)
    start = db.Column(db.DateTime(), primary_key = True)
    end = db.Column(db.DateTime(), primary_key = True)
    
    __mapper_args__ = {
        'polymorphic_identity':'entity/busytime',
    }

    def __init__(self, userUUID: str = None, start: str = None, end: str = None, **kwargs):
        self.userUUID = userUUID
        self.start = start
        self.end = end

        super().__init__(**kwargs)
    

class User(Meta):
    __tablename__ = 'user'


    auth_key_id = db.Column(db.String)
    firstName = db.Column(db.String)
    middleName = db.Column(db.String)
    lastName = db.Column(db.String)
    
    events = db.relationship("EventUser",
         lazy='dynamic', foreign_keys="EventUser.userUUID")

    busyTime = db.relationship("BusyTime",
         lazy='dynamic', cascade = "all, delete, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity':'entity/user',
    }

    def __init__(self, auth_key_id: str = None, firstName: str = None,
        lastName: str = None, middleName: str = None, busyTime = [], **kwargs):
        self.auth_key_id = auth_key_id
        self.lastName = lastName
        self.firstName = firstName
        self.middleName = middleName


        super().__init__(**kwargs)
        self.busyTime = [BusyTime(**bt, userUUID=self.uuid) for bt in busyTime]