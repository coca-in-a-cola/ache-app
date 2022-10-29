from crypt import methods
import jwt
from http import HTTPStatus
from flask import Blueprint, jsonify, request, current_app
from api.schema.user import UserSchema
from api.integrations.rmrail_1c import get_user_by_card_code
from api.jwt.fetch_token import fetch_token
from api.jwt.make_token import make_token
from definitions import ROOT_DIR
from datetime import datetime, timedelta

session_api = Blueprint('session', __name__)

#TODO: дописать!!!
#POST - создаёт новую сессию, PUT - продлевает, DELETE - завершает

@session_api.route('/api/user', methods=['GET'])
def auth_user():
    pass