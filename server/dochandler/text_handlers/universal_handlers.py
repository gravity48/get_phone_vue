from multiprocessing.connection import Connection

import textract
from .abc import ProcessFuncHandler


class TextractHandler(ProcessFuncHandler):

    def __init__(self, filepath):
        super(TextractHandler, self).__init__(filepath)

    @staticmethod
    def callable_func(filepath: str, pipe_send: Connection):
        text_binary = textract.process(filepath)
        base_parser = textract.parsers.utils.BaseParser()
        text = base_parser.decode(text_binary)
        pipe_send.send(text)
