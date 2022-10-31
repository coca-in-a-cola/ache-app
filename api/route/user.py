from flask import Blueprint, jsonify, request, current_app
from api.model.user import User
from api.schema.user import UserSchema
from api.middleware.fetch_json import fetch_json
from api.middleware.json_api import JSON_API
from api.middleware.is_admin import check_admin


user_api = Blueprint('user', __name__)
json_api = JSON_API(User, UserSchema)


@user_api.route('/entity/user', methods=['GET'])
def get_users():
    result = User.query.all()
    if (result):
        dump = UserSchema().dump(result, many=True)
        return jsonify(dump)
    else:
        return jsonify({
                    'error' : 'Нет пользователей'
            }), 404


@user_api.route('/entity/user/<uuid>', methods=['GET'])
@json_api.get_model_by_uuid
@json_api.return_schema
def get_user():
    pass



@user_api.route('/entity/user', methods=['POST'])
@check_admin
@fetch_json
@json_api.post
@json_api.return_schema
def post_user(*args, **kwargs):
    pass


@user_api.route('/entity/user/<uuid>', methods=['DELETE'])
@check_admin
@json_api.get_model_by_uuid
@json_api.delete_model
@json_api.return_schema
def detele_user():
    pass
