import os
import threading
import time
import sys
from collections import namedtuple
from datetime import datetime
from multiprocessing.pool import ThreadPool, Pool
from multiprocessing import Process


class WorkProcess:

    def __init__(self, process, run_time, pool):
        self.process: Process = process
        self.run_time = run_time
        self.pool = pool


class QueueProcess:

    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class CustomProcess:

    def add_task_thread(self, event):
        while not event.is_set():
            if self.queue_process:
                line_process: QueueProcess = self.queue_process.pop(0)
                while 1:
                    if len(self.processes_list) < self.process_count:
                        process = Pool(1)
                        work_process = WorkProcess(
                            process.apply_async(line_process.func, line_process.args, line_process.kwargs),
                            datetime.now(), process)
                        # work_process.process.start()
                        self.processes_list.append(work_process)
                        break

    def control_process(self, event):
        def process_loop():
            for item, work_process in enumerate(self.processes_list):
                try:
                    work_process.process.successful()
                    work_process.pool.close()
                    self.processes_list.pop(item)
                    break
                except ValueError:
                    time_delta = datetime.now() - work_process.run_time
                    time_live = time_delta.total_seconds()
                    if time_live > self.time_processing:
                        work_process.pool.__exit__()
                        self.processes_list.pop(item)
                        break

        while not event.is_set():
            process_loop()
        while len(self.processes_list):
            process_loop()

    def __init__(self, process_count, time_processing):
        self.process_count = process_count
        self.time_processing = time_processing
        self.processes_list = []
        self.queue_process = []
        self.stop_event = threading.Event()

    def __enter__(self):
        self.control_thread_pool = ThreadPool(processes=2)
        self.control_thread_pool.apply_async(self.control_process, (self.stop_event,))
        self.control_thread_pool.apply_async(self.add_task_thread, (self.stop_event,))
        return self

    def apply_async(self, func, args, kwargs=dict()):
        self.queue_process.append(QueueProcess(func, args, kwargs))

    def wait_task_limit(self, task_limit):
        while 1:
            if len(self.queue_process) < task_limit:
                return True
            time.sleep(0.1)

    def join(self):
        while 1:
            if not len(self.queue_process):
                self.stop_event.set()
                self.control_thread_pool.close()
                self.control_thread_pool.join()
                break

    def __exit__(self, exc_type, exc_val, exc_tb):
        for item, work_process in enumerate(self.processes_list):
            work_process.pool.__exit__(exc_type, exc_val, exc_tb)
        self.stop_event.set()
        self.control_thread_pool.__exit__(exc_type, exc_val, exc_tb)
