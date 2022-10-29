from click import confirm
from flask import current_app, request, jsonify, response
from functools import wraps
import jwt
from api.model.user import User
from api.schema.user import UserSchema
from api.schema.meta import selectMetaSchemaUUID

from datetime import datetime, timedelta


def make_token(user : User):
    """
    функция создаёт токен сессии для пользователя
    """
    return jwt.encode(dict(
            user = UserSchema.dump(user),
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
                token = request.get_json()['authToken']
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
            user = User.query.get(selectMetaSchemaUUID(data['user']))
        except Exception as ex:
            return jsonify({
                'error' : f'Пользователь не найден: {ex}'
            }), 404
        
        # returns the current logged in users contex to the routes
        return  f(*args, user = user, **kwargs)
    return decorated


def sign_in(f):
    """
    Декоратор авторизует пользователя в системе и выдаёт ему токен
    После него уже не могут идти какие-либо декораторы
    """

    @wraps(f)
    def decorated(*args, data, **kwargs):
        if ('auth_key_id' in data):
            user = User.query.filter(User.auth_key_id == data['auth_key_id'])
            if (len(user)):
                user = user[0]
                response.headers['x-access-token'] = make_token(user)
                pass
            else:
                
                return jsonify({
                    'error' : 'Пользователь не найден'
                }), 201
            
            confirm_number = generate_confirm_numer(5)

            #при работающем GSM-шлюзе, отправлять сообщения в ответе
            if (current_app.config["GSM_ENABLED"]):
                try:
                    send(user["phone_number"], f"{confirm_number} - ваш код подтверждения")
                except Exception as ex:
                    pass
                    return jsonify({
                        'error' : 'На данный момент GSM-шлюз не работает. Приносим извинения за предоставленные неудобства.'
                    }), 500 

            # Всё получилось
            return make_session(user, False, confirm_number, ["phone_number"])
            
        else:
            return jsonify({
                'error' : 'должен содержать поле ssid с кодом пропуска сотрудника'
            }), 400
            
    return decorated


"""
    Декоратор продления сессии
    После него уже не могут идти какие-либо декораторы
"""
def prolong(f):
    @wraps(f)
    def decorated(*args, token, **kwargs):
        if (token and token["confirmed"]):
            make_session(token['user_info'], token["confirmed"], token["confirm_number"])

        return jsonify({
                'error' : 'Сессия не найдена'
        }), 400
    return decorated