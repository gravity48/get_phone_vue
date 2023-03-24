import typing
from .abc import BaseTextHandler
from .universal_handlers import TextractHandler
from .xls_handler import XlrdHandler, XlsReaderHandler
from .doc_handlers import PythonDocxHandler, WordReaderHandler, CatDocHandler
from .txt_handlers import FileOpenHandler


class ExtractTextFactory:
    handler_by_ext: typing.Dict[str, typing.Type[BaseTextHandler]] = {
        'txt': FileOpenHandler,
        'doc': WordReaderHandler,
        'docx': PythonDocxHandler,
        'xls': XlsReaderHandler,
        'xlsx': XlsReaderHandler,
        'rtf': TextractHandler,
        'csv': TextractHandler,
    }

    @staticmethod
    def _get_extension(filename: str) -> str:
        return filename.split('.')[-1].lower()

    @classmethod
    def get_handler(cls, filepath) -> BaseTextHandler:
        ext = cls._get_extension(filepath)
        return cls.handler_by_ext[ext](filepath)


__all__ = ['ExtractTextFactory', ]




