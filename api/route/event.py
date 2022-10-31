from flask import Blueprint, jsonify, request, current_app
from api.model.event import Event
from api.schema.event import EventSchema
from api.middleware.fetch_json import fetch_json
from api.middleware.json_api import JSON_API
from api.middleware.is_admin import check_admin

event_api = Blueprint('event', __name__)
json_api = JSON_API(Event, EventSchema)


@event_api.route('/entity/event', methods=['GET'])
def get_users():
    result = Event.query.all()
    if (result):
        dump = EventSchema().dump(result, many=True)
        return jsonify(dump)
    else:
        return jsonify({
                    'error' : 'Нет событий'
            }), 404


@event_api.route('/entity/event/<uuid>', methods=['GET'])
@json_api.get_model_by_uuid
@json_api.return_schema
def get_user():
    pass



@event_api.route('/entity/event', methods=['POST'])
@check_admin
@fetch_json
@json_api.post
@json_api.return_schema
def post_user(*args, **kwargs):
    pass


@event_api.route('/entity/event/<uuid>', methods=['DELETE'])
@check_admin
@json_api.get_model_by_uuid
@json_api.delete_model
@json_api.return_schema
def detele_user():
    pass
