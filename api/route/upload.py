from http import HTTPStatus
from flask import Blueprint, send_from_directory, abort, request, jsonify
from api.middleware.check_admin import check_admin
from api.model.upload import check_extension, check_safety, isdir, exists, listdir, save_file, delete_file, mkdir

upload = Blueprint('upload', __name__)

# TODO: отрефакторить код.
# Убрать логику работы из маршрутов, создать больше декораторов в api.model.upload
# Возможно, сотит подробнее выдавать информацию о файлах

@upload.route('/upload', defaults={'filename': ""}, methods=['GET'])
@upload.route('/upload/<path:filename>', methods=['GET'])
@check_safety
def serve_file(filename):
    """
     Подключает все файлы из папки "upload"
     Если пользователь запрашивает папку (в названии нет "."), то выдаёт содержимое этой папки
    ---
    """
    try:
        if (isdir(filename, 'upload')):
            return jsonify(listdir(filename, 'upload')), 200
        else:
            return send_from_directory('upload', filename, as_attachment=True)
    except Exception as ex:
        return jsonify({
                    'error' : "Папка или файл не найдены"
            }), 404


@upload.route('/upload/<path:filename>', methods=['POST'])
@check_admin
@check_safety
def upload_file(filename):
    if 'file' not in request.files:
        # может, пользователь хотел сделать директорию?
        try:
            result = mkdir(filename, 'upload')
            return jsonify({
                        'success' : result
                }), 200
        except:
            return jsonify({
                        'error' : 'Файл не прикреплён. Используйте параметр "file" в запросе'
                }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({
                    'error' : 'Файл не выбран'
            }), 400 

    if not(file and check_extension(filename)):
        return jsonify({
                        'error' : f'Файл {filename} имеет неверный формат или расширение'
                }), 400 

    try:
        save_file(file, filename, 'upload')
    except Exception as save_file_error:
        return jsonify({
                    'error' : f'Невозможно сохранить файл как {filename}: {save_file_error}'
            }), 400 

    return jsonify({
                    'success' : 'true'
            }), 200 


@upload.route('/upload/<path:filename>', methods=['DELETE'])
@check_admin
@check_safety
def remove_file(filename):
    if not exists(filename, 'upload'):
        return jsonify({
                    'error' : 'Папка или файл не найдены'
            }), 404

    if not(check_extension(filename)) and not isdir(filename, 'upload'):
        return jsonify({
                    'error' : 'Недопустимый файл или расширение'
            }), 400 
    try:
        delete_file(filename, 'upload')
    except Exception as delete_file_error:
        return jsonify({
                    'error' : f'Невозможно удалить файл {filename}: {delete_file_error}'
            }), 400 

    return jsonify({
                    'success' : 'true'
            }), 200 