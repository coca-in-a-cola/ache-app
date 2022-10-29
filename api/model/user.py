from api.model.declarative_base import db
from api.model.meta import Meta


class User(Meta):
    __tablename__ = 'user'


    auth_key_id = db.Column(db.String)
    firstName = db.Column(db.String)
    middleName = db.Column(db.String)
    lastName = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity':'user',
    }

    def __init__(self, auth_key_id: str, firstName: str, lastName: str, middleName: str, **kwargs):
        self.auth_key_id = auth_key_id
        self.lastName = lastName
        self.firstName = firstName
        self.middleName = middleName

        super().__init__(**kwargs)