SESSION_TIME_IN_SECONDS = 30*60
SQLALCHEMY_DATABASE_URI = 'sqlite:///db/Main.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOAD_ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'])

# Отправка форм
TASK_SUCCESS_REPORT = lambda number: \
    f"Ваша заявка № {number} сформирована"
TASK_SUCCESS_REPORT_DESCRIPTION_DEFAULT = \
"""По готовности придет смс-сообщение.
Выдача документов осуществляется в отделе кадров пл. ВСП - каб. 103 
с пн по пт с 8:00 до 17:00 (обед с 11:00 до 12:00)"""