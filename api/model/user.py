from api.model.declarative_base import db
from flask import current_app

class User(db.Model):
    card_code = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(100))
    personnel_number = db.Column(db.Integer)
    subdivision = db.Column(db.Text())
    position = db.Column(db.Text())
    phone_number = db.Column(db.String(30))
