from distutils.command.upload import upload
import os
from unittest import result
from definitions import ROOT_DIR
from natsort import natsorted
from datetime import datetime, timezone

class PapersModel:
    class PaperEntry:
        def __init__(self, url, title):
            self.url = url
            self.title = title

    def __init__(self):
        # подготовка данных
        # считаем, что pdf-файлы новостей содержатся в папке "/upload/news" проекта
        news_directory = os.path.join(ROOT_DIR, 'upload', 'papers')
        news_files = os.listdir(news_directory)

        # считаем, что сервер рендерит pdf-файлы газет по url "/upload/papers"
        papers_url = "/upload/papers"

        # пока что имена - это и есть названия файла
        self.entries = [
            self.PaperEntry(url=f"{papers_url}/{filename}", title=os.path.splitext(filename)[0] \
                + f" от {datetime.fromtimestamp(os.path.getmtime(os.path.join(news_directory, filename))).strftime('%d.%m.%Y')}") \
            for filename in sorted(news_files,
            key = lambda fname: os.path.getmtime(os.path.join(news_directory, fname)),
            reverse=True) ]

    def getTop(self, n_entries):
        return self.entries[:n_entries] 