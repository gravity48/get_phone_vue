from datetime import datetime
from typing import Dict, Callable
from database import DataBase, DocumentStatus
from functools import wraps
from subprocess import CalledProcessError
from settings import TIME_HINT
from .loggers import DefaultLogger


def event_logger(logger_: DefaultLogger):
    def _event_logger(func: Callable):
        @wraps(func)
        def wrapper_(data: Dict):
            try:
                logger_.info(f'Run function {func.__name__} with data {data}')
                result = func(data)
                logger_.info(f'Run function {func.__name__} successfully')
                return result
            except Exception as e:
                logger_.error(f'Run function {func.__name__} error {e!r}')
        return wrapper_

    return _event_logger


__all__ = ['event_logger', ]
