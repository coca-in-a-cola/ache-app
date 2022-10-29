import functools
from flask import current_app, request, jsonify
from api.model.declarative_base import db

class JSON_API:

    def __init__(self, Model:db.Model, Schema, **kwargs):
        self.Model = Model
        self.Schema = Schema
        self.__dict__.update(**kwargs)


    def create_model(self, data, many=False):
        try:
            schema = self.Schema().load(data, many=many, partial=True)
            model = self.Model(**schema)
        except:
            raise Exception(f'Невозможно создать модель типа {self.Model.__class__.__name__}')
        
        return model


    def return_model(self, f):
        @functools.wraps(f)
        def decorated(*args, model, **kwargs):
            try:
                schema = self.Schema().dump(model, many=False)
            except:
                return f(*args, model=model, **kwargs)
            return jsonify(schema), 200
        return decorated


    def query_model(self, data, many=False):
        try:
            schema = self.Schema().load(data, many=False, partial=True)
            query = self.Model.query
        except:
            raise Exception(f'Ошибка запроса модели {self.Model.__class__.__name__}')

        if not (query.count()):
            raise Exception(f'Ни одного {self.Model.__class__.__name__} не найдены')
        
        try:
            found = query.filter(*[self.Model.__dict__[key] == schema[key] for key in schema])
        except:
            return jsonify({
                    'error' : f'Ошибка запроса модели {self.Model.__class__.__name__} с параметрами {data}'
            }), 400
        
        if (not found.first()):
            return jsonify({
                    'error' : f'Не найдено {self.Model.__class__.__name__} с параметрами {data}'
            }), 404

        if (many):
            return found.all()
        return found.first()


    def return_models(self, f):
        @functools.wraps(f)
        def decorated(*args, models, **kwargs):
            try:
                schema = self.Schema().dump(models, many=True)
            except:
                return f(*args, models=models, **kwargs)
            return jsonify(schema), 200
        return decorated
    

    def post_all(self, f):
        @functools.wraps(f)
        def decorated(*args, models:list(db.Model), **kwargs):
            try:
                current_app.db.session.add_all(models)
                current_app.db.session.commit()
            except:
                current_app.db.session.rollback()
                return jsonify({
                        'error' : f'Невозможно добавить в базу модели'
                }), 400
            
            return f(*args, models=models, **kwargs)
        return decorated


    def post(self, f):
        @functools.wraps(f)
        def decorated(*args, data:dict, **kwargs):
            try:
                model = self.create_model(data)
                current_app.db.session.add(model)
                current_app.db.session.commit()

            except Exception as ex:
                current_app.db.session.rollback()
                return jsonify({
                        'error' : f'Невозможно добавить модель: f{ex}'
                }), 400
            
            return f(*args, model=model, **kwargs)
        return decorated


    def post_by_uuid(self, f):
        @functools.wraps(f)
        def decorated(*args, uuid, data:dict, **kwargs):
            try:
                data['uuid'] = uuid
                model = self.create_model(data)
                current_app.db.session.add(model)
                current_app.db.session.commit()

            except Exception as ex:
                current_app.db.session.rollback()
                return jsonify({
                        'error' : f'Невозможно изменить модель: f{ex}'
                }), 400
            
            return f(model, *args, **kwargs)
        return decorated


    def delete_by_uuid(self, f):
        @functools.wraps(f)
        def decorated(*args, uuid, **kwargs):
            try:
                model = self.Model.query.get(uuid)
                current_app.db.session.delete(model)
                current_app.db.session.commit()
            except Exception as ex:
                current_app.db.session.rollback()
                return jsonify({
                        'error' : f'Невозможно удалить модель: f{ex}'
                }), 400
            
            return f(*args, model=model, **kwargs)
        return decorated


    def put_by_uuid(self, f):
        @functools.wraps(f)
        def decorated(*args, uuid, data:dict, **kwargs):
            status = 200
            try:
                model = self.Model.query.get(uuid)
                current_app.db.session.delete(model)
            except:
                current_app.db.session.rollback()
                # если у нас ранее не было изменяемой модели, надо уведомить пользователя
                # статусом 201 Created и создать новую
                status = 201

            try:
                model = self.create_model(data)
                current_app.db.session.add(model)
                current_app.db.session.commit()
                
            except Exception as ex:
                current_app.db.session.rollback()
                return jsonify({
                        'error' : f'Невозможно изменить модель типа {self.Model.__class__.__name__}: {ex}'
                }), 400
            
            return f(*args, model=model, **kwargs)
        return decorated