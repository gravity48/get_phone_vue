from functools import wraps
from subprocess import CalledProcessError, TimeoutExpired
from database import DataBase, DocumentStatus
from .abc import StopInfinityProcess


def error_handler_extract_process(func):
    @wraps(func)
    def wrapper_(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except UnicodeDecodeError as e:
            with DataBase() as db_:
                db_.update_status(self.handler_id, DocumentStatus.UNICODE.value)
            self.project_log.error(f'Process {self.process_id}: Record {self.handler_id}: UnicodeDecodeError {e!r}')
        except CalledProcessError as e:
            with DataBase() as db_:
                db_.update_status(self.handler_id, DocumentStatus.PROCESS.value)
            self.project_log.error(f'Process {self.process_id}: Record {self.handler_id}: CalledProcessError {e!r}')
        except TimeoutExpired as e:
            with DataBase() as db_:
                db_.update_status(self.handler_id, DocumentStatus.TIMEOUT.value)
            self.project_log.error(f'Process {self.process_id}: Record {self.handler_id}: TimeoutExpiredError {e!r}')
        except FileNotFoundError as e:
            with DataBase() as db_:
                if self.delete_not_found:
                    db_.remove_document(self.handler_id)
                else:
                    db_.update_status(self.handler_id, DocumentStatus.NOT_FOUND.value)
            self.project_log.error(f'Process {self.process_id}: Record {self.handler_id}: FileNotFoundError')
        except StopInfinityProcess:
            raise StopInfinityProcess()
        except Exception as e:
            with DataBase() as db_:
                db_.update_status(self.handler_id, DocumentStatus.UNEXPECTED.value)
            self.project_log.error(f'Process {self.process_id}: Record {self.handler_id}: Unexpected  {e!r}')
    return wrapper_


def error_handler_control_process(func):
    @wraps(func)
    def wrapper_(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except StopInfinityProcess:
            raise StopInfinityProcess()
        except Exception as e:
            self.project_log.error(f'Control Process Error:  Unexpected  {e!r}')
    return wrapper_

