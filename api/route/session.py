from crypt import methods
from flask import Blueprint, jsonify, request, current_app
from api.model.user import User
from api.model.event import Event, EventUser
from api.schema.event import EventSchema
from api.schema.user import UserSchema, UserEventSchema
from api.middleware.fetch_json import fetch_json
from api.middleware.json_api import JSON_API
from api.middleware.jwt import sign_in, sign_up, fetch_user_from_token, return_current_user, add_bisy_time, delete_bisy_time
from api.integrations.get_notifications import get_notifications

session_api = Blueprint('session', __name__)
json_api = JSON_API(User, UserSchema)

@session_api.route('/session/signin', methods=['POST'])
@fetch_json
@sign_in
def lol():
    pass


@session_api.route('/session/signup', methods=['POST'])
@fetch_json
@sign_up
def lol2():
    pass


@session_api.route('/session/personal', methods=['GET'])
@fetch_user_from_token
@return_current_user
def lol3():
    pass


@session_api.route('/session/personal/time', methods=['POST'])
@fetch_user_from_token
@fetch_json
@add_bisy_time
@return_current_user
def lol4():
    pass


@session_api.route('/session/personal/time', methods=['DELETE'])
@fetch_user_from_token
@fetch_json
@delete_bisy_time
@return_current_user
def lol5():
    pass


@session_api.route('/session/personal/events/setStatus', methods=['POST'])
@fetch_user_from_token
@fetch_json
def change_status(user, data):
    try:
        data = UserEventSchema().load(data)
    except Exception as ex:
        return jsonify({
                    'error' : 'Ошибка данных ' + ex
            }), 400
    

    eventUser = EventUser.query.get((user.uuid, data['eventUUID']))
    if (eventUser):
        eventUser.status = data['status']
        current_app.db.session.commit()
        return jsonify(UserEventSchema().dump(eventUser)), 200
    else:
        return jsonify({
                    'error' : 'Нет события'
            }), 404


@session_api.route('/session/personal/events', methods=['GET'])
@fetch_user_from_token
def get_user_events(user):
    try:
        result = get_notifications(user)
        return jsonify(result), 200
    except Exception as ex:
        jsonify({
                    'error' : f'Произошла ошибка {ex}'
            }), 400
