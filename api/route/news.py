import os
from http import HTTPStatus
from flask import Blueprint
from flask import jsonify
from api.model.news import News
from api.schema.news import NewsEntrySchema
from api.middleware.fetch_json import fetch_json
from api.middleware.check_admin import check_admin
from api.middleware.json_api import JSON_API


news_api = Blueprint('api', __name__)
json_api = JSON_API(News, NewsEntrySchema)

# в целях оптимизации модель создаётся один раз
# считаем, что pdf-файлы новостей содержатся в папке "/upload/news" проекта

@news_api.route('/api/news', methods=['GET'])
def news():
    """
     
    ---
    """
    result = News.query\
        .order_by(
            News.created.desc(),
            News.uuid
        ).all()
    
    if (not result):
        return jsonify({
                    'error' : 'Новости не найдены'
            }), 404
    else:
        return jsonify(NewsEntrySchema().dump(result, many=True)), 200
    

@news_api.route('/api/news', methods=['POST'])
@check_admin
@fetch_json
@json_api.post
@json_api.return_model
def post_news(model):
    pass


@news_api.route('/api/news/<uuid>', methods=['POST'])
@check_admin
@fetch_json
@json_api.post_by_uuid
@json_api.return_model
def post_news_by_uuid(*args, **kwargs):
    pass


@news_api.route('/api/news/<uuid>', methods=['DELETE'])
@check_admin
@json_api.delete_by_uuid
@json_api.return_model
def delete_news_by_uuid(*args, **kwargs):
    pass


@news_api.route('/api/news/<uuid>', methods=['PUT'])
@check_admin
@fetch_json
@json_api.put_by_uuid
@json_api.return_model
def put_news_by_uuid(*args, **kwargs):
    pass