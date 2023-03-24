from database import DataBase
from .BaseConfiguration import BaseConfiguration

base_configuration = BaseConfiguration('config.txt')

base_configuration.database_init()

INTERFACE, PORT = base_configuration.read_socket_data()

LOG_PATH, LOG_ROTATION = base_configuration.get_logs_info()

MONITORING_SLEEP_TIME = base_configuration.get_monitoring_sleep_time()

MAX_VIRTUAL_MEMORY, TIMEOUT = base_configuration.get_process_settings()

MAX_VIRTUAL_MEMORY = MAX_VIRTUAL_MEMORY * 1024 * 1024

TIME_HINT = base_configuration.get_time_hint()



