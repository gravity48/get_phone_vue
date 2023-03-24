import multiprocessing
import os
import resource
import subprocess
import signal
import typing
from multiprocessing import Process
from multiprocessing.connection import Connection

from settings import MAX_VIRTUAL_MEMORY, TIMEOUT


class TextHandlerAbstract:

    def get_text(self) -> str:
        raise NotImplementedError


class BaseTextHandler(TextHandlerAbstract):

    def __init__(self, filepath: str):
        self.filepath = filepath

    @staticmethod
    def limit_process_func():
        os.setsid()
        resource.setrlimit(resource.RLIMIT_DATA, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

    def get_text(self):
        raise NotImplementedError


class ProcessFuncHandler(BaseTextHandler):

    def __init__(self, filepath: str):
        super(ProcessFuncHandler, self).__init__(filepath)

    @staticmethod
    def callable_func(filepath: str, pipe_send: Connection):
        raise NotImplementedError

    def _process_target_func(self, filepath: str, pipe_send: Connection):
        try:
            self.limit_process_func()
            self.callable_func(filepath, pipe_send)
        except Exception as e:
            pipe_send.send(f'{e!r}')
            exit(7)

    def get_text(self):
        pipe_recv, pipe_send = multiprocessing.Pipe()
        process = Process(target=self._process_target_func, args=(self.filepath, pipe_send))
        try:
            process.start()
            process.join(timeout=TIMEOUT)
            if process.exitcode is None:
                process.kill()
                process.join(timeout=TIMEOUT)
                raise subprocess.TimeoutExpired(f'Timeout callable process {self.filepath}', TIMEOUT)
            if process.exitcode != 0:
                raise subprocess.CalledProcessError(process.exitcode, f'Callable process error {self.filepath}')
            text = pipe_recv.recv()
        finally:
            pipe_send.close()
            pipe_recv.close()
            process.close()
        return text


class ProcessOpenHandler(BaseTextHandler):

    def __init__(self, filepath: str, program: str, shell: bool, *program_args):
        super(ProcessOpenHandler, self).__init__(filepath)
        self.program = program
        self.program_args = program_args
        self.shell = shell
        if self.shell:
            self.command = f"""{self.program} "{self.filepath}" {' '.join(program_args)}"""
        else:
            self.command = [self.program, self.filepath, *program_args]

    def _pre_subprocess_run(self):
        pass

    def _error_code_handler(self, return_code: int, std_out: bytes):
        error = std_out.decode("utf-8")
        raise subprocess.CalledProcessError(return_code, f'{self.program} {error}')

    def get_text(self):
        self._pre_subprocess_run()
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=self.shell,
                                   preexec_fn=self.limit_process_func)
        try:
            std_in, std_out = process.communicate(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # stop process
            process.communicate()  # read data from zombies process
            raise subprocess.TimeoutExpired(f'Timeout subprocess {self.filepath}', TIMEOUT)
        if process.returncode:
            return self._error_code_handler(process.returncode, std_out)
        return std_in.decode("utf-8", errors='replace')
