import os
from http import HTTPStatus
from flask import Blueprint, jsonify, request, current_app
from api.schema.menus import MenuSchema
from definitions import ROOT_DIR
from api.middleware.check_admin import check_admin
from api.middleware.fetch_json import fetch_json
from api.middleware.json_api import JSON_API
from api.schema.menus import MenuSchema
from api.model.menus import Menu
import uuid


menus_api = Blueprint('menus', __name__)
json_api = JSON_API(Menu, MenuSchema)


@menus_api.route('/api/menus', defaults={'link': ''}, methods=['GET'])
@menus_api.route('/api/menus/<path:link>', methods=['GET'])
def get_menu(link):
    """
     Выдаёт соответствующее меню по пути
    ---
    """
    try:
        result = json_api.query_model({'location': link})
    except Exception as ex:
        return jsonify({
                    'error' : f'По вашему запросу не нейдено меню. Ошибка: {ex}'
            }), 404
    
    return jsonify(MenuSchema().dump(result))


@menus_api.route('/api/menus-list', methods=['GET'])
def get_menus_list():
    result = Menu.query.all()
    if (result):
        dump = MenuSchema().dump(result, many=True)
        return jsonify(dump)
    else:
        return jsonify({
                    'error' : 'Нет меню'
            }), 404


@menus_api.route('/api/menus-list', methods=['POST'])
@check_admin
@fetch_json
@json_api.post
@json_api.return_model
def post_menu(*args, **kwargs):
    pass


@menus_api.route('/api/menus-list/<uuid>', methods=['POST'])
@check_admin
@fetch_json
@json_api.post_by_uuid
@json_api.return_model
def place_menu(*args, **kwargs):
    pass


@menus_api.route('/api/menus-list/<uuid>', methods=['DELETE'])
@check_admin
@json_api.delete_by_uuid
@json_api.return_model
def delete_news_by_uuid(*args, **kwargs):
    pass


@menus_api.route('/api/menus-list/<uuid>', methods=['PUT'])
@check_admin
@fetch_json
@json_api.put_by_uuid
@json_api.return_model
def put_news_by_uuid(*args, **kwargs):
    pass