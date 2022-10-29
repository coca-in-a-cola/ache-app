from click import confirm
from flask import current_app, request, jsonify
from functools import wraps
import jwt
from api.integrations.rmrail_1c import get_user_by_card_code
from api.integrations.gsm import send
from api.model.user import User
from api.schema.user import UserSchema
from datetime import datetime, timedelta
import random


system_random = random.SystemRandom()


def generate_confirm_numer(length):
    """
    Функция создаёт криптографически защищённый код подтверждения указанной длины
    """
    return "".join(str(system_random.randint(0, 9)) for _ in range(length))


def make_token(user_info, confirmed, confirm_number = None):
    """
    функция создаёт токен с указанными параметрами
    """
    return jwt.encode(dict(
            user_info = user_info,
            confirmed = confirmed,
            confirm_number = confirm_number,
            expires = datetime.isoformat(datetime.utcnow() + timedelta(seconds = current_app.config['SESSION_TIME_IN_SECONDS'])),
    ), current_app.config['SECRET_KEY'], algorithm="HS256")


def make_session(user_info, confirmed, confirm_number, show_user_fields = []):
    """
    Конечная точка, где мы создаём и возвращаем ответ сервера на создание сессии
    """

    token = make_token(user_info, confirmed, confirm_number)
    result = dict(
        authToken = token,
        lifeTime = current_app.config['SESSION_TIME_IN_SECONDS'],
        phoneNumber = user_info['phone_number'],
        confirmed = confirmed,
    )
    if not current_app.config["GSM_ENABLED"]:
        result['confirmNumber'] = confirm_number
    
    def toCamelCase (s):
        init, *temp = s.split('_')
        return(''.join([init.lower(), *map(str.title, temp)]))

    for field in show_user_fields:
        if field == "phone_number":
            result[toCamelCase(field)] = ''.join([user_info[field][:-10], "******", user_info[field][-4:]])
            continue
        
        result[toCamelCase(field)] = user_info[field]
        
    return jsonify(result), 200


def fetch_token(f):
    """
    Декторатор проверяет наличие токена, и возвращает декодированное его содержимое
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

        # returns the current logged in users contex to the routes
        return  f(*args, token = data, **kwargs)
    return decorated


def check_user_confirmed(f):
    """
    Декторатор проверяет подтверждённый токен, переданный в фуцнкцию \n
    Применять необходимо после fetch_token, для проверки 2-х факторного входа
    """
    @wraps(f)
    def decorated(*args, token, **kwargs):
        if not token["confirmed"]:
            return jsonify({
                'error' : 'Пользователь не прошел второй этап авторизации'
            }), 401

        return f(*args, token = token, **kwargs)
    return decorated


def auth_user(f):
    """
    Декоратор авторизует пользователя в системе. \n
    После него уже не могут идти какие-либо декораторы
    """

    @wraps(f)
    def decorated(*args, data, **kwargs):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            if ('ssid' in data):
                user_info = get_user_by_card_code(data['ssid'])
                if (not user_info):
                    return jsonify({
                        'error' : 'Пользователь не найден'
                    }), 404
                
                confirm_number = generate_confirm_numer(5)

                #при работающем GSM-шлюзе, отправлять сообщения в ответе
                if (current_app.config["GSM_ENABLED"]):
                    try:
                        send(user_info["phone_number"], f"{confirm_number} - ваш код подтверждения")
                    except Exception as ex:
                        pass
                        return jsonify({
                            'error' : 'На данный момент GSM-шлюз не работает. Приносим извинения за предоставленные неудобства.'
                        }), 500 

                # Всё получилось
                return make_session(user_info, False, confirm_number, ["phone_number"])
                
            else:
                return jsonify({
                    'error' : 'должен содержать поле ssid с кодом пропуска сотрудника'
                }), 400
        else:
            return jsonify({
                    'error' : 'Ошибка! Отправляйте данные только через json'
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


def confirm_number(f):
    """
    Декоратор подтверждения номера (2-й этап авторизации)
    После него уже не могут идти какие-либо декораторы
    """
    @wraps(f)
    def decorated(*args, data, token, **kwargs):
        if token["confirmed"]:
            return jsonify({
                'success' : 'Пользователь уже подтверждён!'
            }), 201
        
        if not "confirmNumber" in data:
            return jsonify({
                'error' : 'Должен содержать поле confirmNumber с кодом подтверждения'
            }), 400
        
        if (data["confirmNumber"] != token["confirm_number"]):
            return jsonify({
                'error' : 'Неверный код подтверждения'
            }), 400 
        
        return make_session(token["user_info"], True, token["confirm_number"], ["phone_number", "fullname"])
    return decorated