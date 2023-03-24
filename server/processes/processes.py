import queue as queue_module
import time
from typing import List, Callable
from multiprocessing import Process, Queue, Event
from multiprocessing.synchronize import Event as EventClass
from pullenti_wrapper.processor import Processor, PERSON
from dochandler import DocHandler
from database import DataBase, DocumentStatus
from logging_ import ProjectLog
from settings import MONITORING_SLEEP_TIME
from sources import Specification, DataSources
from .abc import *
from .decorators import error_handler_extract_process


class ProcessMonitoring(InfinityProcess):
    """Процесс отвечающий за мониторинг процессов-работников и их корректное завершение"""

    def __init__(self, processes: List[Process], stop_workers: EventClass, ctl_process_is_done: EventClass,
                 queue: Queue, project_log: ProjectLog, proc_dict: dict):
        super(ProcessMonitoring, self).__init__(project_log, 'ProcessMonitoring')
        self.processes = processes
        self.stop_workers = stop_workers
        self.ctl_process_is_done = ctl_process_is_done
        self.queue = queue
        self.proc_dict = proc_dict

    def monitoring(self):
        """
        Проверяет в каком состоянии находятся процессы работники и
        при необходимости осуществляет их перезапуск
        """
        for item, process in enumerate(self.processes):
            if not process.is_alive():
                self.project_log.error(f'Monitoring process: Process {item} is not alive')
                process.start()
                self.project_log.error(f'Monitoring process: Process {item} start successfully')
        time.sleep(MONITORING_SLEEP_TIME)

    def stop_processes(self):
        """Если извлекающий процесс успешно завершился, завершить корректно процессы рабоники"""
        while True:
            if not self.queue.empty():
                time.sleep(MONITORING_SLEEP_TIME)
            else:
                break
        self.stop_workers.set()
        for process in self.processes:
            process.join()
        self.proc_dict['status'] = 'Task successfully done and stopped'
        self.project_log.debug('Task successfully done and stopped')

    def start_proj(self):
        """
        В случае если контрольный процесс не завершился
        процесс находится в режиме мониторинга
        В ином случае - осуществляет завершение процессов
        """
        if not self.ctl_process_is_done.is_set():
            self.monitoring()
        else:
            self.stop_processes()
            raise StopInfinityProcess()


class ProcessControlExtract(InfinityProcessTimeout):
    """
    Процесс осуществляющий извлечение из класса Источника id файлов, удовлетворяющих
    требованию класса спецификации и передачу его в процессы-работники (ExtractProcess)
    """

    def __init__(self, source: DataSources, specification: Specification, queue: Queue, raw_data: bool,
                 ctl_process_is_done: EventClass, project_log: ProjectLog):
        super(ProcessControlExtract, self).__init__(project_log, 'ProcessControlExtract')
        self.queue = queue
        self.raw_data = raw_data
        self.source = source
        self.specification = specification
        self.ctl_process_is_done = ctl_process_is_done

    def start_proj(self):
        """Извлечение id из базы источника согласно спецификации"""
        for id_ in self.source.get_source(self.specification):
            if not self.raw_data:
                self.queue.put(id_)
        self.ctl_process_is_done.set()
        raise StopInfinityProcess()


class ExtractProcess(InfinityProcess):
    """Предназначен для извлечения именованных сущностей из файла по его id в базе данных"""

    def __init__(self, process_id: int, proc_dict: dict, queue: Queue, read_doc_date: bool, project_log: ProjectLog,
                 stop_process: EventClass):
        """
        handler_id - содержит id обрабатываемого документа и используется для обработки исключений
        pullenti_processor - Препроцессор осуществляющий извлечение Именной информации
        """
        super(ExtractProcess, self).__init__(project_log, f'ExtractProcess {process_id}')
        self.process_id = process_id
        self.proc_dict = proc_dict
        self.queue = queue
        self.read_doc_date = read_doc_date
        self.stop_process = stop_process
        self.pullenti_processor = None
        self.handler_id: int = 0

    def launch_prepare(self):
        self.pullenti_processor = Processor([PERSON])

    @error_handler_extract_process
    def start_proj(self):
        """Процесс извлекает из очереди id документа в базе данных и осуществляет его обработку"""
        try:
            id_ = self.queue.get_nowait()
        except queue_module.Empty:
            time.sleep(MONITORING_SLEEP_TIME)
            if self.stop_process.is_set():
                raise StopInfinityProcess()
            return
        self.project_log.info(f'Process {self.process_id}: Record {id_} in progress')
        self.handler_id = id_
        with DataBase() as db_:
            filename, filepath = db_.get_doc_data(id_)
        doc_handler = DocHandler(filepath)
        doc_date = doc_handler.get_doc_date()
        paragraphs, number_map, persons_map = doc_handler.handler_output_file(self.pullenti_processor)
        with DataBase() as db_:
            db_.update_record(id_, DocumentStatus.SUCCESS.value, number_map, paragraphs, persons_map, doc_date)
        self.proc_dict['status'] = f'Record {id_}: {filepath}'
        self.project_log.info(f'Process {self.process_id}: Record {id_}: {filepath}')


__all__ = ['ProcessMonitoring', 'ProcessControlExtract', 'ExtractProcess']
