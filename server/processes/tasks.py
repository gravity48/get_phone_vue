from typing import Dict, List
from threading import Thread
from multiprocessing import Value, Manager, Process, Event
from logging_ import ProjectLog
from sources.DataSourses import FileSources, DataBaseSource
from sources.specifications import FileSpecification, DataBaseSpecification
from .abc import *
from .processes import *


class Task:

    def __init__(self):
        """
        self.is_run = Value('i', 1)
        self.proc_dict = None
        self.queue = Queue(maxsize=2)
        """
        self.control_process: None or Process = None
        self.process_monitor: None or Thread = None
        self.manager = Manager()
        self.proc_dict = self.manager.dict()
        self.queue = self.manager.Queue(maxsize=10)
        self.workers: List[Process] = []
        self.stop_workers_event = Event()
        self.ctl_process_is_done_event = Event()

    def start(self, process_count: int):
        raise NotImplementedError

    def status(self):
        alive_workers = sum(map(lambda x: int(x.is_alive()), self.workers))
        return f"""{self.proc_dict['status']} {alive_workers}/{len(self.workers)}"""

    def stop(self):
        self.control_process.kill()
        self.control_process.join()
        self.process_monitor.kill()
        self.process_monitor.join()
        for process in self.workers:
            process.kill()
            process.join()
        self.manager.shutdown()


class ExtractProcessTask(Task):

    def __init__(self, delete_not_found: bool, project_log: ProjectLog):
        super(ExtractProcessTask, self).__init__()
        self.delete_not_found = delete_not_found
        self.project_log = project_log

    def start(self, process_count: int):
        for index in range(process_count):
            self.workers.append(Process(
                target=ExtractProcess(index, self.proc_dict, self.queue, self.delete_not_found, self.project_log,
                                      self.ctl_process_is_done_event), ))
            self.workers[-1].start()
        self.process_monitor = Thread(
            target=ProcessMonitoring(self.workers, self.stop_workers_event, self.ctl_process_is_done_event, self.queue,
                                     self.project_log, self.proc_dict), )
        self.process_monitor.start()


class ExtractEntityTask(ExtractProcessTask):
    """
    Класс-проект Извлечения именнованных сущностей и служит для запуска процессов:
    1) Workers - список процессов-работников(ExtractProcess), непосредственно осуществляющих извлечение
                именнованных сущностей из документов
    2) Process Monitor - поток, отслеживающий состояние процессов-работников и осуществляющий их перезапуск в
                случае необходимости
    3) ProcessControlExtract - процесс извлекающий сведения из различных источников и передающий его в процессы
                работники.
    """

    def __init__(self, folder: str, extensions: List[str],
                 only_new_file: bool, raw_data: bool, delete_not_found: bool, project_log: ProjectLog):
        """
        folder - папка для обработки
        extensions - список расширений, которые будут учавствовать в обработке
        only_new_file - добавлять в обработку только файлы, которые не содержаться в базе данных
        raw_data - если False, то данные фактически не обрабатываются а лишь вносяться в базу данных с статусом Process
        delete_not_found - если True, ненайденные файлы будут удалены из базы
        project_log - класс Логгера
        """
        super().__init__(delete_not_found, project_log)
        self.folder = folder
        self.extensions = extensions
        self.only_new_file = only_new_file
        self.raw_data = raw_data

    def start(self, process_count: int):
        super(ExtractEntityTask, self).start(process_count)
        self.control_process = Process(target=ProcessControlExtract(FileSources(self.folder),
                                                                    FileSpecification(self.extensions,
                                                                                      self.only_new_file,
                                                                                      self.project_log, self.proc_dict),
                                                                    self.queue,
                                                                    self.raw_data, self.ctl_process_is_done_event,
                                                                    self.project_log), )
        self.control_process.start()


class RetrainTask(ExtractProcessTask):

    def __init__(self, doc_status: List[str], record_id: int, raw_data: bool,
                 delete_not_found: bool, project_log: ProjectLog):
        super().__init__(delete_not_found, project_log)
        self.record_id = record_id
        self.doc_status = doc_status
        self.raw_data = raw_data

    def start(self, process_count: int):
        super(RetrainTask, self).start(process_count)
        self.control_process = Process(
            target=ProcessControlExtract(DataBaseSource(), DataBaseSpecification(self.doc_status, self.record_id),
                                         self.queue, self.raw_data, self.ctl_process_is_done_event, self.project_log), )
        self.control_process.start()


__all__ = ['Task', 'ExtractEntityTask', 'RetrainTask']
