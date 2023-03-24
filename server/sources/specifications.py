from typing import List, Dict
from database import DataBase
from logging_ import ProjectLog
from .abc import Specification


class FileSpecification(Specification):

    def __init__(self, extensions: List[str], only_new_file: bool, project_log: ProjectLog, proc_dict: Dict):
        self.extensions: List[str] = extensions
        self.only_new_file: bool = only_new_file
        self.project_log = project_log
        self.proc_dict = proc_dict

    @staticmethod
    def delete_extension(filename: str) -> str:
        return filename.split('.')[-1]

    def is_satisfy(self, item: str):
        extension = self.delete_extension(item)
        if extension not in self.extensions:
            return False
        if self.only_new_file:
            with DataBase() as db:
                if db.is_processed(item):
                    self.project_log.info(f'{item} is processed')
                    self.proc_dict['status'] = f'{item} is processed'
                    return False
        return True


class DataBaseSpecification(Specification):

    def __init__(self, doc_status: List[str], record_id: int):
        self.doc_status: List[str] = doc_status
        self.id_ = record_id

    def is_satisfy(self, item) -> bool:
        pass

    def as_dict(self):
        return {
            'doc_status': self.doc_status,
            'id': self.id_,
        }


__all__ = ['FileSpecification', 'DataBaseSpecification']
