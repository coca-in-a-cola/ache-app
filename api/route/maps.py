import os
from http import HTTPStatus
from flask import Blueprint
from flask import jsonify
from api.model.maps import Maps
from api.schema.maps import MapsSchema
from api.middleware.fetch_json import fetch_json
from api.middleware.check_admin import check_admin
from api.middleware.json_api import JSON_API


maps_api = Blueprint('maps', __name__)
json_api = JSON_API(Maps, MapsSchema)

# в целях оптимизации модель создаётся один раз
# считаем, что pdf-файлы новостей содержатся в папке "/upload/news" проекта

@maps_api.route('/api/maps-list/', methods=['GET'])
def maps_list():
    """
     
    ---
    """
    result = Maps.query.all()
    
    if (not result):
        return jsonify({
                    'error' : 'Карты не найдены'
            }), 404
    else:
        return jsonify(MapsSchema().dump(result, many=True)), 200
    

@maps_api.route('/api/maps/<location>', methods=['GET'])
def maps_by_loc(location):
    """
     
    ---
    """
    result = Maps.query.filter(
            Maps.location == location
        ).all()
    
    if (not result):
        return jsonify({
                    'error' : 'Карты не найдены'
            }), 404
    else:
        return jsonify(MapsSchema().dump(result, many=True)), 200


@maps_api.route('/api/maps-list', methods=['POST'])
@check_admin
@fetch_json
@json_api.post
@json_api.return_model
def post_news(model):
    pass


@maps_api.route('/api/maps-list/<uuid>', methods=['POST'])
@check_admin
@fetch_json
@json_api.post_by_uuid
@json_api.return_model
def post_news_by_uuid(*args, **kwargs):
    pass


@maps_api.route('/api/maps-list/<uuid>', methods=['DELETE'])
@check_admin
@json_api.delete_by_uuid
@json_api.return_model
def delete_news_by_uuid(*args, **kwargs):
    pass


@maps_api.route('/api/maps-list/<uuid>', methods=['PUT'])
@check_admin
@fetch_json
@json_api.put_by_uuid
@json_api.return_model
def put_news_by_uuid(*args, **kwargs):
    pass