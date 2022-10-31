from flask import Flask
from argparse import ArgumentParser
from route import spa
from waitress import serve
import app_secrets
import app_config
from itertools import chain
from api.model.declarative_base import db
from flask_cors import CORS
import sys

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # registering blueprints
    from api.route.user import user_api
    from api.route.event import event_api
    from api.route.session import session_api
    app.register_blueprint(user_api)
    app.register_blueprint(event_api)
    app.register_blueprint(session_api)
    # Держите его последним
    app.register_blueprint(spa)

    # user_db.create_all(app=app)
    return app


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-t', '--host', default='0.0.0.0', type=str, help='IP-адрес сервера. 0.0.0.0 откроет его для всех публичных адресов, 127.0.0.1 - только на локальном')
    parser.add_argument('-p', '--port', default=5000, type=int, help='Порт, на котором будет работать приложение')
    parser.add_argument('-b', '--production', default=False, action='store_true', help='Отметьте, если сервер работает в боевом режиме')
    parser.add_argument('-d', '--drop_db', default=False, action='store_true', help='ОПАСНО! Форматирует базу данных. Рекомендуется делать при первом запуске')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    app = create_app()
    args = get_args()
    
    # устанавливаем конфиг
    app.config['PRODUCTION'] = args.production

    for key, value in chain(*[[(var, getattr(module, var)) for var in dir(module) \
        if not var.startswith("__")] for module in [app_config, app_secrets]]):
        app.config[key] = value

    db.init_app(app)
    app.db = db
    #db.create_all()

    if (args.drop_db):
        @app.before_first_request
        def create_tables():
            db.drop_all()
            db.create_all()

        
    # app.py -p 3000 запустит приложение с портом 3000
    port = args.port
    host = args.host

    if (args.production):
        serve(app, host=host, port=port)
    else:
        CORS(app)
        app.run(host=host, port=port)
