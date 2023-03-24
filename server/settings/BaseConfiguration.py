import configparser
from typing import Tuple
from database import DataBase


class BaseConfiguration:

    def __init__(self, file_: str):
        self.file_ = file_
        self.config = configparser.ConfigParser()
        self.config.read(file_)
        self.database_init()

    def database_init(self):
        if self.config['DATABASE']['database'] == 'postgresql':
            DataBase.init_postgres_db(**self.config['DATABASE'])

    def read_socket_data(self) -> Tuple[str, int]:
        return self.config['WEBSOCKET']['host'], int(self.config['WEBSOCKET']['port'])

    def get_logs_info(self) -> Tuple[str, str]:
        return self.config['LOGS']['log_path'], self.config['LOGS']['rotation']

    def get_process_settings(self) -> Tuple[int, int]:
        return self.config['PROCESS'].getint('max_virtual_memory'), self.config['PROCESS'].getint('timeout')

    def get_time_hint(self):
        return self.config['DEBUG'].getint('time_hint')

    def get_monitoring_sleep_time(self):
        return self.config['DEBUG'].getfloat('sleep_time_monitoring')

    def update_db_info(self, *args, **kwargs):
        self.config['DATABASE']['db_host'] = kwargs['db_ip']
        self.config['DATABASE']['db_port'] = str(kwargs['db_port'])
        self.config['DATABASE']['db_login'] = kwargs['db_login']
        self.config['DATABASE']['db_password'] = kwargs['db_password']
        self.config['DATABASE']['db_path'] = kwargs['db_path']
        with open(self.file_, 'w') as _:
            self.config.write(_)
        del DataBase.instance
        DataBase.init_postgres_db(**self.config['DATABASE'])
        pass


