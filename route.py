# Этот blueprint прописывает подключение SPA и убирание слешов в приложении
# Его нужно подключать последним
from flask import Blueprint

spa = Blueprint('spa', __name__, static_folder='spa/build')

# Serve SPA
@spa.route('/', defaults={'path': ''})
@spa.route('/<path:path>')
def catch_all(path):
    return spa.send_static_file("index.html")

@spa.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])