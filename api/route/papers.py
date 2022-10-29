from http import HTTPStatus
from flask import Blueprint
from flask import jsonify
from api.model.papers import PapersModel
from api.schema.news import NewsEntrySchema

papers_api = Blueprint('papers', __name__)


@papers_api.route('/api/papers')
def papers():
    result = PapersModel().entries

    result_obj = {"newsList": result}
    if (result):
        return jsonify(NewsEntrySchema().dump(result, many=True))
    else:
        return HTTPStatus.NOT_FOUND, 404