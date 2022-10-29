from api.model.declarative_base import db
import uuid as _uuid
from app_config import TASK_SUCCESS_REPORT_DESCRIPTION_DEFAULT

class FormTask(db.Model):
    __tablename__ = "formTask"

    uuid = db.Column(db.String(32), primary_key = True)
    title = db.Column(db.String(32))
    completionTimeInHours = db.Column(db.Integer())

    successMessage = db.Column(db.Text())

    performers = db.relationship("Performer",
        backref="_formTask",
        lazy='dynamic',
        cascade = "all, delete, delete-orphan" 
    )

    fields = db.relationship("FormField",
        backref="_formTask",
        lazy='dynamic',
        cascade = "all, delete, delete-orphan" 
    )


    def __init__(self, uuid = None, completionTimeInHours=48, performers = [],
        successMessage = TASK_SUCCESS_REPORT_DESCRIPTION_DEFAULT, \
        fields = [], **kwargs):
        
        if not uuid:
            uuid = str(_uuid.uuid4().hex)

        super().__init__(uuid = uuid, completionTimeInHours=completionTimeInHours,\
            successMessage=successMessage, **kwargs)
        
        for item in performers:
            if not 'completionTimeInHours' in item:
                item['completionTimeInHours'] = completionTimeInHours

        self.performers = [Performer(**item, formtask_uuid = uuid) for item in performers]
        self.fields = [FormField(**item, formtask_uuid = uuid) for item in fields]


class Performer(db.Model):
    __tablename__ = "performer"

    uuid = db.Column(db.String(32), primary_key = True)
    uuid_1c = db.Column(db.String(36))
    fullname = db.Column(db.Text())
    completionTimeInHours = db.Column(db.Integer())
    responsible = db.Column(db.Boolean())

    formtask_uuid = db.Column(db.String(32), db.ForeignKey('formTask.uuid'))

    def __init__(self, uuid = None, **kwargs):
        if not uuid:
            uuid = str(_uuid.uuid4().hex)
        super().__init__(uuid = uuid, **kwargs)


class FormField(db.Model):
    __tablename__ = "formField"

    uuid = db.Column(db.String(32), primary_key = True)
    name = db.Column(db.Text())
    label = db.Column(db.Text())
    type = db.Column(db.Text())
    placeholder = db.Column(db.Text())
    required = db.Column(db.Boolean())

    formtask_uuid = db.Column(db.String(32), db.ForeignKey('formTask.uuid'))

    def __init__(self, uuid = None, **kwargs):
        if not uuid:
            uuid = str(_uuid.uuid4().hex)
        super().__init__(uuid = uuid, **kwargs)                