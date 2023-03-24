import time
from multiprocessing import Value, Manager, Process

from logging_ import ProjectLog

INFINITY_PROCESS_TIMEOUT = 60


class StopInfinityProcess(Exception):
    pass


class ProcessAbc:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class InfinityProcess (ProcessAbc):
    """Бесконечный процесс, вызывающий функцию  start_proj()"""

    def __init__(self, project_log: ProjectLog, proj_name: str):
        self.project_log = project_log
        self.proj_name = proj_name

    def start_proj(self):
        raise NotImplementedError

    def launch_prepare(self):
        pass

    def __call__(self, *args, **kwargs):
        self.launch_prepare()
        while True:
            try:
                self.start_proj()
            except StopInfinityProcess as e:
                self.project_log.debug(f'Infinity process {self.proj_name} stopped {e!r}')
                break
            except Exception as e:
                self.project_log.debug(f'Infinity process {self.proj_name} exceptions {e!r}')
                continue


class OneStartProcess (ProcessAbc):

    def __init__(self, project_log: ProjectLog, name: str):
        self.project_log = project_log
        self.name = name

    def __call__(self, *args, **kwargs):
        self.start_project()

    def start_project(self):
        raise NotImplementedError


class InfinityProcessTimeout(ProcessAbc):

    def __init__(self, project_log: ProjectLog, proj_name: str):
        self.timeout = INFINITY_PROCESS_TIMEOUT
        self.project_log = project_log
        self.proj_name = proj_name

    def start_proj(self):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        while True:
            try:
                self.start_proj()
            except StopInfinityProcess as e:
                self.project_log.debug(f'InfinityProcessTimeout {self.proj_name} stopped {e!r}')
                break
            except Exception as e:
                self.project_log.debug(f'InfinityProcessTimeout {self.proj_name} error {e!r}')
                time.sleep(self.timeout)
                continue


__all__ = ['ProcessAbc', 'InfinityProcess', 'OneStartProcess', 'StopInfinityProcess', 'InfinityProcessTimeout']


