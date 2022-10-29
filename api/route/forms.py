import os
from http import HTTPStatus
from flask import Blueprint
from flask import jsonify, current_app
from api.middleware.jwt_auth import check_user_confirmed
from api.model.forms import FormTask, FormField
from api.schema.forms import FormTaskSchema
from api.middleware.fetch_json import fetch_json
from api.middleware.check_admin import check_admin
from api.middleware.json_api import JSON_API
from api.middleware.jwt_auth import fetch_token
from api.integrations.rmrail_1c import send_form_task
from api.middleware.du_task_number import du_task_number

forms_api = Blueprint('forms', __name__)
json_api = JSON_API(FormTask, FormTaskSchema)


@forms_api.route('/api/forms', methods=['GET'])
def forms():
    result = FormTask.query.all()
    if (result):
        dump = FormTaskSchema().dump(result, many=True)
        return jsonify(dump)
    else:
        return jsonify({
                    'error' : 'Нет форм'
            }), 404
    

@forms_api.route('/api/forms', methods=['POST'])
@check_admin
@fetch_json
@json_api.post
@json_api.return_model
def post_forms(model):
    pass


@forms_api.route('/api/forms/send/<uuid>', methods=['POST'])
@fetch_json
@fetch_token
@check_user_confirmed
def send_form(*args, uuid, data, token, **kwargs):
    formTask = FormTask.query.get(uuid)
    taskNumber = du_task_number()

    
    if not formTask:
        return jsonify({
                    'error' : f'Форма не найдена c uuid {uuid}'
            }), 404
    
    try:
        send_form_task(token["user_info"], formTask, taskNumber, data)
    except Exception as ex:
        return jsonify({
                'error' : f'Не удалось отправить форму! Исключение: \n {ex}'
        }), 400
    
    return jsonify(dict(
        label = current_app.config["TASK_SUCCESS_REPORT"](taskNumber),
        text = formTask.successMessage)), 200


@forms_api.route('/api/forms/<uuid>', methods=['GET'])
def get_forms_by_uuid(*args, uuid, **kwargs):
    result = FormTask.query.get(uuid)
    if (result):
        dump = FormTaskSchema().dump(result, many=False)
        return jsonify(dump)
    else:
        return jsonify({
                    'error' : 'Форма не найдена'
            }), 404


@forms_api.route('/api/forms/<uuid>', methods=['POST'])
@check_admin
@fetch_json
@json_api.post_by_uuid
@json_api.return_model
def post_forms_by_uuid(*args, **kwargs):
    pass


@forms_api.route('/api/forms/<uuid>', methods=['DELETE'])
@check_admin
@json_api.delete_by_uuid
@json_api.return_model
def delete_forms_by_uuid(*args, **kwargs):
    pass


@forms_api.route('/api/forms/<uuid>', methods=['PUT'])
@check_admin
@fetch_json
@json_api.put_by_uuid
@json_api.return_model
def put_forms_by_uuid(*args, **kwargs):
    pass