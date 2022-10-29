import functools
from api.model.declarative_base import db
from flask import current_app
from functools import wraps
import uuid
import os
from flask import jsonify



class File(db.Model):
    name = db.Column(db.Text())
    path = db.Column(db.Text(), primary_key = True)
    hashsum = db.Column(db.Text(), primary_key = True)


def check_safety(f):
    """
    Декоратор проверяет, безопасен ли переданный пользовтелем параметр filename \n
    filename, ведущие на родительскую папку, папку пользоователя,
    корень системы и т.д. НЕ БЕЗОПАСНЫ и их редактирование может причинить вред
    работе приложения и всего сервера

    ОБЯЗАТЕЛЬНО СТАВЬТЕ ЭТОТ ДЕКОРАТОР ПЕРЕД ФУНКЦИЕЙ, ПРИНИМАЮЩЕЙ ПАРАМЕТР filename
    """
    @wraps(f)
    def decorated(*args, filename, **kwargs):
        here = os.path.abspath(".")
        there = os.path.abspath(filename)
        if not there.startswith(here):
            # тут можно ещё и отправлять отчёты о попытке взлома системы
            return jsonify({
                    'error' : "Ошибка безопасности!!!"
            }), 400
        return  f(*args, filename = filename, **kwargs)
    return decorated


def check_extension(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower()\
        in current_app.config['UPLOAD_ALLOWED_EXTENSIONS']
    

def mkrecursivedirs(paths, upload_dir):

    full_relative_path = f"{upload_dir}"
    for directory in paths:
        if ('.' in directory):
            raise Exception('Неверный фомрат пути!')
    
        full_relative_path = os.path.join(full_relative_path, directory)
        if not os.path.exists(full_relative_path):
            os.mkdir(full_relative_path)
    return full_relative_path


def mkdir(filename, upload_dir):
    path = filename.split('/')
    full_relative_path = mkrecursivedirs(path[:len(path)-1], upload_dir)
    return full_relative_path


def save_file(file, filename, upload_dir):    
    path = filename.split('/')
    full_relative_path = mkrecursivedirs(path[:len(path)-1], upload_dir)

    full_relative_path = os.path.join(full_relative_path, path[-1])

    file.save(full_relative_path)


def delete_file(filename, upload_dir):
    full_relative_path = os.path.join(upload_dir, filename)

    if not os.path.exists(full_relative_path):
        raise Exception('Файл не найден')
    
    if os.path.isdir(full_relative_path):
        os.rmdir(full_relative_path)
    else:
        os.remove(full_relative_path)


def isdir(filename, upload_dir):
    full_relative_path = os.path.join(upload_dir, filename)
    return os.path.isdir(full_relative_path)


def exists(filename, upload_dir):
    full_relative_path = os.path.join(upload_dir, filename)
    return os.path.exists(full_relative_path)


def listdir(filename, upload_dir):
    full_relative_path = os.path.join(upload_dir, filename)

    if not os.path.exists(full_relative_path):
        raise Exception('Папка или файл не найдены')
    if not os.path.isdir(full_relative_path):
        raise Exception('Не является папкой')
    
    return os.listdir(full_relative_path)
