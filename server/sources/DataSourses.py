import os
from typing import Dict
from database import DataBase
from logging_ import ProjectLog
from .abc import *
from .specifications import DataBaseSpecification


class DataBaseSource(DataSources):
    """Источник из базы данных"""
    def __init__(self):
        pass

    def get_source(self, specification: DataBaseSpecification):
        filter_: Dict = specification.as_dict()
        while True:
            with DataBase() as db:
                record_id = db.get_document_by_filter(filter_)
            if record_id:
                filter_['id'] = record_id
                yield record_id
            else:
                return


class FileSources(DataSources):
    """Файловый источник"""
    def __init__(self, path: str):
        self.path = path

    def get_source(self, specification) -> int:
        for folder, subdir, files in os.walk(self.path):
            for file in files:
                filepath = f'{folder}/{file}'
                if specification.is_satisfy(filepath):
                    with DataBase() as db:
                        record_id = db.add_record(file, filepath)
                    yield record_id


__all__ = ['DataBaseSource', 'FileSources']
