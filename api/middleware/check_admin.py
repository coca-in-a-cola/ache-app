from flask import current_app, request, jsonify
import functools
from app_secrets import admin_login, admin_password

def isAdmin(login, password):
    return login == admin_login and password == admin_password

# Декторатор проверяет админский доступ в basic auth
def check_admin(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not isAdmin(auth.username, auth.password):
            return jsonify({
                'error' : 'неверный логин или пароль'
            }), 401
        return f(*args, **kwargs)
    return decorated