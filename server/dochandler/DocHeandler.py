from typing import Pattern, Tuple, List, Dict
import errno
import os
from collections import namedtuple, defaultdict
from pullenti_wrapper.processor import Processor, PERSON
from datetime import datetime
from .Doc import Doc
from .text_handlers.abc import BaseTextHandler
from .text_handlers.factory import ExtractTextFactory

ProcessedFile = namedtuple('ProcessedFile', ['filename', 'path'])

DocData = namedtuple('DocData', ['paragraphs', 'numbers', 'persons'])


class DocHandler:

    def __init__(self, filepath: str):
        self.filepath: str = filepath

    def get_doc_date(self) -> datetime:
        return datetime.fromtimestamp(os.path.getmtime(self.filepath))

    def handler_output_file(self, pulleti_processor: Processor) -> DocData:
        doc = Doc(self.handler_get_text(), pulleti_processor)
        paragraphs = doc.get_paragraphs()
        numbers_map = doc.get_numbers_map()
        persons_map = doc.get_person_map()
        return DocData(paragraphs, numbers_map, persons_map)

    def handler_get_text(self):
        if os.path.exists(self.filepath):
            base_text_handler: BaseTextHandler = ExtractTextFactory.get_handler(self.filepath)
            text = base_text_handler.get_text()
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.filepath)
        return text
