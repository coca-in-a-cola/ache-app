from crypt import methods
import jwt
from http import HTTPStatus
from flask import Blueprint, jsonify, request, current_app
from api.middleware.fetch_json import fetch_json
from api.schema.user import UserSchema
from api.middleware.jwt_auth import fetch_token, auth_user, confirm_number, prolong

session_api = Blueprint('session', __name__)

#POST - создаёт новую сессию, PUT - продлевает

@session_api.route('/api/session', methods=['POST'])
@fetch_json
@auth_user
def auth_user():
    pass


@session_api.route('/api/session/confirmNumber', methods=['POST'])
@fetch_json
@fetch_token
@confirm_number
def confirm_number():
    pass


@session_api.route('/api/session', methods=['PUT'])
@fetch_json
@fetch_token
@prolong
def prolong():
    pass