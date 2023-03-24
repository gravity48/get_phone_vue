from multiprocessing.connection import Connection

from .abc import ProcessFuncHandler


class FileOpenHandler(ProcessFuncHandler):

    def __init__(self, filepath: str):
        super(FileOpenHandler, self).__init__(filepath)

    @staticmethod
    def callable_func(filepath: str, pipe_send: Connection):
        try:
            with open(filepath, "rt") as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(filepath, "rt", encoding='cp1251', errors='replace') as f:
                text = f.read()
        pipe_send.send(text)

