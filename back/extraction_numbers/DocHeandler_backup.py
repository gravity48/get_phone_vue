'''

import asyncio
import copy
import docx2txt
import multiprocessing
import re
import subprocess
import sys
import os, signal
import time
import threading
import textract
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from extraction_numbers.Doc import Doc
from extraction_numbers.class_data_base import DataBase, document_status
from functools import wraps
from loguru import logger
from pullenti_wrapper.processor import Processor, PERSON
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from extraction_numbers.stop_words import stop_words
from shutil import copyfile
from extraction_numbers.custom_process import CustomProcess
from get_phone_view.celery import app

TASK_LIMIT = 100

TIME_PROCESSING = 200

ProcessedFile = namedtuple('ProcessedFile', ['filename', 'path'])

CONVERT_DOC2TXT = """libreoffice --headless --convert-to "txt:Text (encoded):UTF8" """

logger.remove()
doc_handler_log = copy.deepcopy(logger)


class TestHandler:
    def __init__(self, kwargs):
        self.path2base = kwargs['path2base']
        self.ip_base = kwargs['ip_base']
        self.port = kwargs['port']
        self.mask_dict = {
            'txt': self.handler_textract,
            'doc': self.handler_word_reader,
            'docx': self.handler_python_docx,
            'xls': self.handler_textract,
            'xlsx': self.handler_textract,
            'tiff': self.handler_textract,
            'rtf': self.handler_textract,
        }
        self.db = DataBase(self.path2base, self.ip_base, self.port)
        self.search_numbers = kwargs['search_numbers'],
        self.search_pers_data = kwargs['search_pers_data']
        self.check_processed = kwargs['check_processed']
        self.stop_regex = self._generate_stop_regex()

    def handler_output_file(self, filename, text, pulleti_processor):
        if text:
            doc = Doc(text, filename, pulleti_processor, self.stop_regex, doc_handler_log)
            paragraphs = doc.get_paragraphs()
            numbers_map = {}
            persons_map = {}
            for item, paragraph in enumerate(paragraphs):
                numbers_map[item] = []
                persons_map[item] = []
            if self.search_numbers:
                doc_handler_log.info(f'search numbers {filename}')
                doc.extractions_numbers(numbers_map)
            if self.search_pers_data:
                doc_handler_log.info(f'search personal data {filename}')
                doc.extractions_persons_data(persons_map)
        else:
            doc_handler_log.info(f'no text {filename}')
            numbers_map = {}
            persons_map = {}
            paragraphs = []
        return paragraphs, numbers_map, persons_map

    @staticmethod
    def handler_python_docx(filepath):
        text = docx2txt.process(filepath)
        return text

    @staticmethod
    def handler_word_reader(filepath):
        current_dir = os.getcwd()
        convert_string = f""" {current_dir}/WordReader "{filepath}" """
        process = subprocess.Popen(convert_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   preexec_fn=os.setsid)
        text = process.communicate()[0].decode("utf-8")
        return text

    @staticmethod
    def handler_textract(filepath):
        text_binary = textract.process(filepath)
        base_parser = textract.parsers.utils.BaseParser()
        text = base_parser.decode(text_binary)
        return text

    def handler_pdftotxt(self, filepath):
        convert_string = f"""pdftotext "{filepath}" -"""
        process = subprocess.Popen(convert_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   preexec_fn=os.setsid)
        text = process.communicate()[0].decode("utf-8")
        return text

    def check_processed_file(self, filename):
        if self.check_processed:
            if self.db.is_processed(filename):
                doc_handler_log.info(f'File {filename} has already been processed')
                return True
            else:
                return False
        return False

    @staticmethod
    def delete_extension(filename):
        extension = filename.split('.')[-1]
        index = filename.rfind(extension)
        filename_new = filename[:index - 1]
        return filename_new, extension

    def handler_get_text(self, filepath, extension):
        handler_func = self.mask_dict[extension]
        doc_handler_log.info(f'{handler_func.__name__} {filepath}')
        text = handler_func(filepath)
        doc_handler_log.info(f'success transcoding {filepath}')
        return text

    @staticmethod
    def _generate_stop_regex():
        re_string = '(?:{})'.format('|'.join(stop_words))
        return re.compile(re_string)

    pass


class DocHandler:
    def __init__(self, default_log: str = None, input_dir=None, output_dir=None, path2base=None,
                 ip_base=None, port=None, time_processing=None, check_processed_file=True, search_numbers=True,
                 search_pers_data=True):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.path2base = path2base
        self.ip_base = ip_base
        self.port = port
        self.time_processing: int = time_processing
        doc_handler_log.add(sys.stdout, format="{time} {level} {message}", level="INFO")
        #doc_handler_log.add(f'logfiles/{default_log}.info', format='{time} {level} {message}',
        #                    filter=lambda record: record["level"].name == "INFO", rotation='5Mb', compression='zip')
        #doc_handler_log.add(f'logfiles/{default_log}.error', format='{time} {level} {message}',
        #                    filter=lambda record: record["level"].name == "ERROR", rotation='5Mb', compression='zip')
        self.mask_dict = {
            'txt': self.handler_textract,
            'doc': self.handler_word_reader,
            'docx': self.handler_python_docx,
            'xls': self.handler_textract,
            'xlsx': self.handler_textract,
            'tiff': self.handler_textract,
            'rtf': self.handler_textract,
        }
        self.db = DataBase(self.path2base, self.ip_base, self.port)
        self.pulleti_processor = Processor([PERSON])
        self.stop_regex = self._generate_stop_regex()
        self.check_processed = check_processed_file
        self.search_numbers = search_numbers
        self.search_pers_data = search_pers_data

    @staticmethod
    def _generate_stop_regex():
        re_string = '(?:{})'.format('|'.join(stop_words))
        return re.compile(re_string)

    @staticmethod
    def _get_files(mask, directories):
        files_list = []
        for folder, subdir, files in os.walk(directories):
            for filename in files:
                extension = filename.split('.')[-1]
                try:
                    mask.index(extension)
                    processed_file = ProcessedFile(filename=filename, path=f'{folder}/{filename}')
                    files_list.append(processed_file)
                except ValueError:
                    continue
        return files_list

    @staticmethod
    def __delete_extension(filename):
        extension = filename.split('.')[-1]
        index = filename.rfind(extension)
        filename_new = filename[:index - 1]
        return filename_new, extension

    def __kill_process(self, process, hard=False):
        if hard:
            try:
                os.kill(process.pid + 1, 9)
                os.kill(process.pid, 9)
            except ProcessLookupError:
                doc_handler_log.info('No such process')
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        return True

    def handler_output_file(self, filename, text, pulleti_processor):
        if text:
            doc = Doc(text, filename, pulleti_processor, self.stop_regex, doc_handler_log)
            paragraphs = doc.get_paragraphs()
            numbers_map = {}
            persons_map = {}
            for item, paragraph in enumerate(paragraphs):
                numbers_map[item] = []
                persons_map[item] = []
            if self.search_numbers:
                doc_handler_log.info(f'search numbers {filename}')
                doc.extractions_numbers(numbers_map)
            if self.search_pers_data:
                doc_handler_log.info(f'search personal data {filename}')
                doc.extractions_persons_data(persons_map)
        else:
            doc_handler_log.info(f'no text {filename}')
            numbers_map = {}
            persons_map = {}
            paragraphs = []
        return paragraphs, numbers_map, persons_map

    def handler_python_docx(self, filepath):
        text = docx2txt.process(filepath)
        return text

    def handler_word_reader(self, filepath):
        current_dir = os.getcwd()
        convert_string = f""" {current_dir}/WordReader "{filepath}" """
        process = subprocess.Popen(convert_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   preexec_fn=os.setsid)
        text = process.communicate()[0].decode("utf-8")
        return text

    def handler_textract(self, filepath):
        text_binary = textract.process(filepath)
        base_parser = textract.parsers.utils.BaseParser()
        text = base_parser.decode(text_binary)
        return text

    def handler_pdftotxt(self, filepath):
        convert_string = f"""pdftotext "{filepath}" -"""
        process = subprocess.Popen(convert_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   preexec_fn=os.setsid)
        text = process.communicate()[0].decode("utf-8")
        return text

    def handler_get_text(self, filepath, extension):
        handler_func = self.mask_dict[extension]
        doc_handler_log.info(f'{handler_func.__name__} {filepath}')
        text = handler_func(filepath)
        doc_handler_log.info(f'success transcoding {filepath}')
        return text

    @staticmethod
    def clear_temp_file(filepath):
        os.remove(filepath)

    def clear_temp_files(self):
        mask = ['txt', ]
        output_files = self._get_files(mask, self.output_dir)
        for filename, path in output_files:
            doc_handler_log.info(f'remove {path}')
            os.remove(path)

    def check_processed_file(self, filename):
        if self.check_processed:
            if self.db.is_processed(filename):
                doc_handler_log.info(f'File {filename} has already been processed')
                return True
            else:
                return False
        return False

    def _entity_thread_timeout(self, filename, filepath):
        filename, extension = self.__delete_extension(filename)
        if extension not in self.mask_dict.keys(): return
        processed_file = ProcessedFile(filename=filename, path=filepath)
        doc_handler_log.info(f'processed file {processed_file.path}')
        if self.check_processed_file(processed_file.filename): return
        file_text = self.handler_get_text(processed_file.path, extension)
        paragraphs, number_map, persons_map = self.handler_output_file(filename, file_text, self.pulleti_processor)
        doc_handler_log.info(f'save to db {filename}')
        self.db.add_record(filename, filepath, document_status['success'], number_map, paragraphs, persons_map)
        doc_handler_log.info(f'processing completed {processed_file.path}')

    def _retraining_thread_timeout(self, document_id, filename, filepath):
        extension = filepath.split('.')[-1]
        if extension not in self.mask_dict.keys(): return
        processed_file = ProcessedFile(filename=filename, path=filepath)
        doc_handler_log.info(f'processed file {processed_file.path}')
        file_text = self.handler_get_text(processed_file.path, extension)
        paragraphs, number_map, persons_map = self.handler_output_file(filename, file_text, self.pulleti_processor)
        doc_handler_log.info(f'save to db {filename}')
        self.db.update_record(document_id, document_status['success'], number_map, paragraphs, persons_map)
        doc_handler_log.info(f'processing completed {processed_file.path}')

    def _entity_proj_thread(self, filename, folder):
        filepath = f'{folder}/{filename}'
        with ThreadPool(processes=1) as pool:
            async_result = pool.apply_async(self._entity_thread_timeout, (filename, filepath))
            try:
                async_result.get(self.time_processing)
            except multiprocessing.context.TimeoutError:
                doc_handler_log.error(f'process timeout: {filepath}')
                self.__write_result_in_db(filename, filepath, document_status['timeout'], [], [], [], self.db)
            except UnicodeDecodeError:
                doc_handler_log.error(f'unicode error: {filepath}')
                self.__write_result_in_db(filename, filepath, document_status['unicode'], [], [], [], self.db)
            except Exception as e:
                doc_handler_log.error(f'unexpected {e}: {filepath}')
                self.__write_result_in_db(filename, filepath, document_status['unexpected'], [], [], [], self.db)
            finally:
                pool.terminate()

    def _retraining_proj_thread(self, document_id, filename, document_path):
        with ThreadPool(processes=1) as pool:
            async_result = pool.apply_async(self._retraining_thread_timeout, (document_id, filename, document_path))
            try:
                async_result.get(self.time_processing)
            except multiprocessing.context.TimeoutError:
                doc_handler_log.error(f'process timeout: {document_path}')
                self.db.update_record(document_id, document_status['timeout'], [], [], [])
            except UnicodeDecodeError:
                doc_handler_log.error(f'unicode error: {document_path}')
                self.db.update_record(document_id, document_status['unicode'], [], [], [])
            except Exception as e:
                doc_handler_log.error(f'unexpected {e}: {document_path}')
                self.db.update_record(document_id, document_status['unexpected'], [], [], [])
            finally:
                pool.terminate()
        pass

    def run_entity_proj(self, thread_count):
        doc_handler_log.info('Run project one at time')
        doc_handler_log.info('Get list files from folder')
        futures = set()
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            for folder, subdir, files in os.walk(self.input_dir):
                for file in files:
                    if len(futures) >= TASK_LIMIT:
                        completed, futures = wait(futures, return_when=FIRST_COMPLETED)
                    futures.add(executor.submit(self._entity_proj_thread, file, folder))
        doc_handler_log.info('Success')

    def run_retraining_proj(self, thread_count):
        doc_handler_log.info('Run retraining proj')
        doc_handler_log.info('Get list files from database')
        futures = set()
        offset = 0
        error_documents = self.db.get_error_documents(TASK_LIMIT, offset)
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            while error_documents:
                offset += TASK_LIMIT
                for document_id, filename, document_path in error_documents:
                    if len(futures) >= TASK_LIMIT:
                        completed, futures = wait(futures, return_when=FIRST_COMPLETED)
                    futures.add(executor.submit(self._retraining_proj_thread, document_id, filename, document_path))
                error_documents = self.db.get_error_documents(TASK_LIMIT, offset)
        doc_handler_log.info('Success')

    @staticmethod
    @app.task(time_limit=TIME_PROCESSING, ignore_result=True)
    def retraining_proj_process(filename, folder, kwargs):
        pulleti = Processor([PERSON])
        filepath = f'{folder}/{filename}'
        test_handler = TestHandler(kwargs)
        filename, extension = test_handler.delete_extension(filename)
        processed_file = ProcessedFile(filename=filename, path=filepath)
        doc_handler_log.info(f'processed file {processed_file.path}')
        if test_handler.check_processed_file(processed_file.filename):return
        file_text = test_handler.handler_get_text(processed_file.path, extension)
        paragraphs, number_map, persons_map = test_handler.handler_output_file(filename, file_text, pulleti)
        doc_handler_log.info(f'save to db {filename}')
        test_handler.db.add_record(filename, filepath, document_status['success'], number_map, paragraphs, persons_map)
        doc_handler_log.info(f'processing completed {processed_file.path}')
        return

    def run_retraining_proj_process(self, process_count):
        doc_handler_log.info('Run retraining proj process')
        doc_handler_log.info('Get list files from database')
        kwargs = {
            'ip_base': self.ip_base,
            'port': self.port,
            'path2base': self.path2base,
            'search_numbers': self.search_numbers,
            'search_pers_data': self.search_pers_data,
            'check_processed': self.check_processed,
        }
        tasks = []

        for folder, subdir, files in os.walk(self.input_dir):
            for file in files:
                self.retraining_proj_process.apply_async(args=(file, folder, kwargs), queue='priority.high')
    pass


if __name__ == '__main__':

    init_map = {
        'default_log': 'test',
        'input_dir': "/home/gravity/Temp/Files",
        'output_dir': '/media/gravity/Data/PycharmProjects/get_phone_view_git/temp',
        'path2base': '/home/gravity/Temp/Base/db_numbers_doc_status.fdb',
        'ip_base': '127.0.0.1',
        'port': '3050',
        'time_processing': 500,
        'check_processed_file': True,
        'search_pers_data': True,
        'search_numbers': True
    }
    doc_handler = DocHandler(**init_map)
    # doc_handler.run_entity_proj(1)
    # doc_handler.run_retraining_proj(1)
    doc_handler.run_retraining_proj_process(5)
    pass
'''

