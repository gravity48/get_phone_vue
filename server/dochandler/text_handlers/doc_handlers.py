import re
from multiprocessing.connection import Connection

import docx2txt
from .abc import  ProcessOpenHandler, ProcessFuncHandler


class PythonDocxHandler(ProcessFuncHandler):

    def __init__(self, filepath):
        super(PythonDocxHandler, self).__init__(filepath)

    @staticmethod
    def callable_func(filepath: str, pipe_send: Connection):
        text = docx2txt.process(filepath)
        pipe_send.send(text)


class WordReaderHandler(ProcessOpenHandler):

    def __init__(self, filepath):
        program = 'WordReader'
        super(WordReaderHandler, self).__init__(filepath, program, False, '--no-log')


class CatDocHandler(ProcessOpenHandler):

    def _pre_subprocess_run(self):
        self.filepath = re.sub(r'`', r'\\`', self.filepath)

    def _error_code_handler(self, return_code: int, std_out: bytes):
        errors = std_out.decode("utf-8")
        if str(errors) == 'This file looks like ZIP archive or Office 2007 or later file.\nNot supported by catdoc\n':
            return PythonDocxHandler(self.filepath).get_text()

    def __init__(self, filepath: str):
        program = 'catdoc'
        super(CatDocHandler, self).__init__(filepath, program, False)

