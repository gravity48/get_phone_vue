from loguru import logger
from .loggers import *
from . import log_decorators

logger.remove()

main_log = MainLog()

__all__ = ['main_log', 'ProjectLog', 'log_decorators']
