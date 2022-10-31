from click import confirm
from flask import current_app, request, jsonify, Response
from functools import wraps
import jwt
from api.model.user import User, BusyTime
from api.schema.user import UserSchema
from api.schema.timeDelta import TimeDeltaPrivateSchema
from api.schema.meta import selectUUID

from datetime import datetime, timedelta


def make_token(user : User):
    """
    функция создаёт токен сессии для пользователя
    """
    return jwt.encode(dict(
            user = UserSchema().dump(user),
            expires = datetime.isoformat(datetime.utcnow() + timedelta(seconds = current_app.config['SESSION_TIME_IN_SECONDS'])),
    ), current_app.config['SECRET_KEY'], algorithm="HS256")
    

def fetch_user_from_token(f):
    """
    Декторатор проверяет наличие токена, и возвращает данные пользователя
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # or request body as authToken
        if not token:
            try:
                token = request.get_json()['x-access-token']
            except:
                return jsonify({'error' : 'Токен не найден!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
        except:
            return jsonify({
                'error' : 'Неверно закодированный токен! Создана угроза безопасности. Об этом инциденте будет доложено.'
            }), 401

        if (datetime.utcnow() > datetime.fromisoformat(data['expires'])):
            return jsonify({
                'error' : 'Время сессии истекло! Войдите в систему снова'
            }), 401

        try:
            user = User.query.get(selectUUID(data['user']))
        except Exception as ex:
            return jsonify({
                'error' : f'Пользователь не найден: {ex}'
            }), 404
        
        # returns the current logged in users contex to the routes
        return  f(*args, user = user, **kwargs)
    return decorated


def return_current_user(f):
    """
    Декоратор возвращает данные пользователя по токену
    После него уже не могут идти какие-либо декораторы
    """

    @wraps(f)
    def decorated(*args, user, **kwargs):
        try:
            return jsonify(UserSchema().dump(user)), 200
        except Exception as ex:
            return jsonify({
                'error' : f'Ошибка личного кабинета: {ex}'
            }), 400
    return decorated


def add_bisy_time(f):
    """
    Обновляет данные пользователя по времени занятости
    """

    @wraps(f)
    def decorated(*args, user, data, **kwargs):
        try:
            schema = TimeDeltaPrivateSchema().load(data, partial=True)
            model = BusyTime(userUUID = user.uuid, **schema)
            user.busyTime.append(model)
            current_app.db.session.add(model)
            current_app.db.session.commit()

        except Exception as ex:
            current_app.db.session.rollback()
            return jsonify({
                'error' : f'Ошибка добавления времени {ex}'
            }), 400

        return f(*args, user=user, model = user, **kwargs)
    return decorated


def delete_bisy_time(f):
    """
    Удаляет данные пользователя по времени занятости
    """

    @wraps(f)
    def decorated(*args, user, data, **kwargs):
        try:
            schema = TimeDeltaPrivateSchema().load(data)
            model = BusyTime.query.get((user.uuid, schema['start'], schema['end']))
            current_app.db.session.delete(model)
            current_app.db.session.commit()

        except Exception as ex:
            current_app.db.session.rollback()
            return jsonify({
                'error' : f'Ошибка удаления времени {ex}'
            }), 400

        return f(*args, user=user, model = user, **kwargs)
    return decorated


def sign_in(f):
    """
    Декоратор авторизует пользователя в системе и выдаёт ему токен
    После него уже не могут идти какие-либо декораторы
    """

    @wraps(f)
    def decorated(*args, data, **kwargs):
        if ('auth_key_id' in data):
            user = User.query.filter(User.auth_key_id == data['auth_key_id']).all()
            if (len(user)):
                user = user[0]
                token = make_token(user)
                resp = jsonify(
                    {
                        'x-access-token': token,
                        'expires': current_app.config['SESSION_TIME_IN_SECONDS']
                    }
                )
                resp.headers['x-access-token'] = token
                return resp, 200
            else:
                
                return jsonify({
                    'error' : 'Пользователь не найден'
                }), 404
    return decorated


def sign_up(f):
    """
    Декоратор регистрирует нового пользователя в системе
    После него уже не могут идти какие-либо декораторы
    """

    @wraps(f)
    def decorated(*args, data, **kwargs):
        user = User.query.filter(User.auth_key_id == data['auth_key_id']).all()
        if len(user):
            return jsonify({
                    'error' : 'Пользователь уже зарегистрирован для данного ТГ-аккаунта'
                }), 403

        try:        
            schema = UserSchema().load(data, partial=True)
            model = User(**schema)
            current_app.db.session.add(model)
            current_app.db.session.commit()

            return jsonify({
                'success': True,
            }), 200
        except Exception as ex:
            current_app.db.session.rollback()
            return jsonify({
                    'error' : 'Ошибка регистрации пользователя'
                }), 400

    return decorated