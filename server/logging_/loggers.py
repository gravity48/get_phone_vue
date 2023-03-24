import sys
from loguru import logger
from settings import LOG_PATH, LOG_ROTATION


class DefaultLogger:

    def __init__(self, logger_id, logger_):
        self.logger_id = logger_id
        self.logger_ = logger_

    def info(self, msg):
        self.logger_.info(msg)

    def error(self, msg):
        self.logger_.error(msg)

    def debug(self, msg):
        self.logger_.debug(msg)

    def __del__(self):
        logger.remove(self.logger_id)


class MainLog(DefaultLogger):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(MainLog, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        logger_id = logger.add(sys.stdout, filter=lambda record: 'all' in record["extra"]['alias'])
        logger_ = logger.bind(alias='all')
        super().__init__(logger_id, logger_)


class ProjectLog(DefaultLogger):

    def __init__(self, alias):
        logger_id = logger.add(f'{LOG_PATH}/{alias}.log',
                               filter=lambda record: alias in record["extra"]['alias'],
                               format="{time:DD-MM-YYYY HH:mm:ss} {level} {message}",
                               rotation=LOG_ROTATION)
        logger_ = logger.bind(alias=alias)
        super().__init__(logger_id, logger_)


__all__ = ['MainLog', 'ProjectLog', 'DefaultLogger']
