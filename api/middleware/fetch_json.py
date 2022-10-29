import functools
from flask import current_app, request, jsonify

'''
    Обрабатывает JSON-запрос, извлекая из него объект
'''
def fetch_json(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return jsonify({
                    'error' : 'Ошибка! Отправляйте данные только через json'
            }), 400

        try:
            data = request.json
        except:
            return jsonify({
                    'error' : 'Данные неверно закодированы в json'
            }), 400            

        return f(*args, data=data, **kwargs)
    return decorated