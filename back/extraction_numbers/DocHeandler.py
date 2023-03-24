import copy
import docx2txt
import errno
import re
import subprocess
import sys
import os
import pika
import textract
import time
from collections import namedtuple
from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded
from django.conf import settings
from datetime import datetime
from extraction_numbers.stop_words import stop_words
from extraction_numbers.Doc import Doc
from extraction_numbers.class_data_base import DataBase, document_status
from loguru import logger
from pullenti_wrapper.processor import Processor, PERSON
from subprocess import CalledProcessError
from sqlalchemy.exc import SQLAlchemyError
from get_phone_view.celery import app

TASK_LIMIT = 100

TIME_PROCESSING = 200

ProcessedFile = namedtuple('ProcessedFile', ['filename', 'path'])

CONVERT_DOC2TXT = """libreoffice --headless --convert-to "txt:Text (encoded):UTF8" """


def delete_extension(filename):
    extension: str = filename.split('.')[-1]
    index = filename.rfind(extension)
    filename_new = filename[:index - 1]
    return filename_new, extension.lower()


class DocHandler:

    def __init__(self, kwargs):
        self.path2base = kwargs['path2base']
        self.ip_base = kwargs['ip_base']
        self.port = kwargs['port']
        self.mask_dict = {
            'txt': self.handler_open_file,
            'doc': self.handler_word_reader,
            'docx': self.handler_python_docx,
            'xls': self.handler_textract,
            'xlsx': self.handler_textract,
            'rtf': self.handler_textract,
            'csv': self.handler_open_file,
        }
        self.db = DataBase(self.path2base, self.ip_base, self.port)
        self.stop_regex = self._generate_stop_regex()

    def handler_output_file(self, filename, text, pulleti_processor):
        if text:
            doc = Doc(text, filename, pulleti_processor, self.stop_regex)
            paragraphs = doc.get_paragraphs()
            numbers_map = {}
            persons_map = {}
            for item, paragraph in enumerate(paragraphs):
                numbers_map[item] = []
                persons_map[item] = []
            # doc_handler_log.info(f'search numbers {filename}')
            doc.extractions_numbers(numbers_map)
            # doc_handler_log.info(f'search personal data {filename}')
            doc.extractions_persons_data(persons_map)
        else:
            # doc_handler_log.info(f'no text {filename}')
            numbers_map = {}
            persons_map = {}
            paragraphs = []
        return paragraphs, numbers_map, persons_map

    @staticmethod
    def handler_open_file(filepath):
        try:
            with open(filepath, "rt") as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(filepath, "rt", encoding='cp1251') as f:
                text = f.read()
        return text

    @staticmethod
    def handler_python_docx(filepath):
        text = docx2txt.process(filepath)
        return text

    @staticmethod
    def handler_word_reader(filepath):
        convert_string = f"""WordReader "{filepath}" --no-log """
        process = subprocess.Popen(convert_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   preexec_fn=os.setsid)
        text = process.communicate()[0].decode("utf-8")
        if process.returncode != 0:
            raise CalledProcessError(process.returncode, convert_string, output=filepath)
        return text

    @staticmethod
    def handler_textract(filepath):
        text_binary = textract.process(filepath)
        base_parser = textract.parsers.utils.BaseParser()
        text = base_parser.decode(text_binary)
        return text

    def handler_get_text(self, filepath, extension: str):
        if os.path.exists(filepath):
            handler_func = self.mask_dict[extension.lower()]
            # doc_handler_log.info(f'{handler_func.__name__} {filepath}')
            text = handler_func(filepath)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filepath)
        return text

    @staticmethod
    def _generate_stop_regex():
        re_string = '(?:{})'.format('|'.join(stop_words))
        return re.compile(re_string)

    @staticmethod
    def date_settings(kwargs, filepath):
        if kwargs['auto_date']:
            doc_date = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%d.%m.%Y')
        else:
            doc_date = datetime.strptime(kwargs['doc_date'], '%d.%m.%Y')
        return doc_date

    pass


class ProjectsInit:
    def __init__(self, default_log: str = None, input_dir=None, output_dir=None, path2base=None,
                 ip_base=None, port=None, time_processing=None, test=None, doc_date=None, extensions_array=None,
                 auto_date=False, status_array=None):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.path2base = path2base
        self.ip_base = ip_base
        self.port = port
        self.time_processing: int = time_processing
        self.extensions_array = extensions_array
        self.status_array = status_array
        self.auto_date = auto_date
        if doc_date is None:
            self.doc_date = datetime.now().strftime('%d.%m.%Y')
        else:
            self.doc_date = doc_date
        credentials = pika.PlainCredentials(settings.CELERY_BROKER_USER, settings.CELERY_BROKER_PASSWORD)
        parameters = pika.ConnectionParameters(credentials=credentials,
                                               host=settings.CELERY_BROKER_HOST,
                                               port=settings.CELERY_BROKER_PORT, heartbeat=1800,
                                               blocked_connection_timeout=900)
        connection = pika.BlockingConnection(parameters=parameters)
        self.channel = connection.channel()
        self.log_name = default_log
        logger.remove()
        self.doc_handler_log = copy.deepcopy(logger)
        self.doc_handler_log.remove()
        if test:
            self.doc_handler_log.add(sys.stdout, format="{time} {level} {message}", level="INFO")
        else:
            self.doc_handler_log.add(f'logfiles/{default_log}.info', format='{time} {level} {message}',
                                     filter=lambda record: record["level"].name == "INFO", rotation='20Mb',
                                     compression='zip')
            self.doc_handler_log.add(f'logfiles/{default_log}.error', format='{time} {level} {message}',
                                     filter=lambda record: record["level"].name == "ERROR", rotation='20Mb',
                                     compression='zip')

    def tasks_count(self, queue_name):
        queue = self.channel.queue_declare(queue=queue_name, durable=True)
        message_count = queue.method.message_count
        return message_count

    @staticmethod
    def _sync_proj(auto_date, filepath, filename, db):
        if auto_date:
            doc_date = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%d.%m.%Y')
        else:
            doc_date = datetime.strptime(auto_date, '%d.%m.%Y')
        db.add_record(filename, filepath, document_status['sync'], [], [], [], doc_date)

    @staticmethod
    @app.task(ignore_result=True)
    def entity_proj_celery(filename, filepath, kwargs):
        log_name = kwargs['log_name']
        doc_handler = DocHandler(kwargs)
        loguru_import = __import__('loguru', globals(), locals(), [], 0)
        loguru_import.logger.remove()
        log = loguru_import.logger
        log.add(f'logfiles/{log_name}.info', format='{time} {level} {message}',
                filter=lambda record: record["level"].name == "INFO")
        log.add(f'logfiles/{log_name}.error', format='{time} {level} {message}',
                filter=lambda record: record["level"].name == "ERROR")
        try:
            filename, extension = delete_extension(filename)
            pulleti = Processor([PERSON])
            processed_file = ProcessedFile(filename=filename, path=filepath)
            log.info(f'get text from file {processed_file.path}')
            file_text = doc_handler.handler_get_text(processed_file.path, extension)
            log.info(f'handler output file {processed_file.path}')
            paragraphs, number_map, persons_map = doc_handler.handler_output_file(filename, file_text, pulleti)
            log.info(f'save to db {processed_file.path}')
            doc_date = doc_handler.date_settings(kwargs, filepath)
            doc_handler.db.add_record(filename, filepath, document_status['success'], number_map, paragraphs,
                                      persons_map, doc_date)
            log.info(f'processing completed {processed_file.path}')
            return
        except (SoftTimeLimitExceeded, TimeLimitExceeded):
            log.error(f'process timeout: {filepath}')
            doc_handler.db.add_record(filename, filepath, document_status['timeout'], [], [], [], None)
            return
        except UnicodeDecodeError:
            log.error(f'decode error: {filepath}')
            doc_handler.db.add_record(filename, filepath, document_status['unicode'], [], [], [], None)
            return
        except CalledProcessError:
            log.error(f'process error: {filepath}')
            doc_handler.db.add_record(filename, filepath, document_status['process'], [], [], [], None)
        except Exception as e:
            log.error(f'unexpected {e}: {filepath}')
            doc_handler.db.add_record(filename, filepath, document_status['unexpected'], [], [], [], None)
            return

    def run_entity_with_celery(self, check_processed, sync_proj):
        self.doc_handler_log.info('Run entity proj')
        self.doc_handler_log.info('Get list files from folder')
        kwargs = {
            'ip_base': self.ip_base,
            'port': self.port,
            'path2base': self.path2base,
            'auto_date': self.auto_date,
            'sync_proj': sync_proj,
            'log_name': self.log_name,
            'doc_date': self.doc_date,
        }
        db = DataBase(self.path2base, self.ip_base, self.port)
        for folder, subdir, files in os.walk(self.input_dir):
            for file in files:
                while 1:
                    message_count = self.tasks_count('priority.high')
                    if message_count < TASK_LIMIT:
                        break
                filepath = f'{folder}/{file}'
                filename, extension = delete_extension(file)
                if extension not in self.extensions_array.keys(): continue
                reconnect_count = 10
                timeout = 10
                while reconnect_count:
                    try:
                        if check_processed:
                            if db.is_processed(filepath):
                                break
                        self.doc_handler_log.info(f'Add task processed {filepath}')
                        if sync_proj:
                            self._sync_proj(kwargs['auto_date'], filepath, filename, db)
                            break
                        self.entity_proj_celery.apply_async(
                            args=(file, f'{folder}/{file}', kwargs),
                            queue='priority.high', time_limit=self.time_processing + 20,
                            soft_time_limit=self.time_processing)
                        # self.entity_proj_celery(file, f'{folder}/{file}', kwargs)
                        break
                    except SQLAlchemyError as e:
                        error = str(e.__dict__['orig'])
                        self.doc_handler_log.error(f'{error}: attempts left - {reconnect_count} timeout - {timeout}')
                        time.sleep(timeout)
                        timeout *= 10
                        reconnect_count -= 1
                        continue
        self.doc_handler_log.info('Success')
        pass

    @staticmethod
    @app.task(ignore_result=True)
    def retrain_proj_celery(record_id, filename, filepath, extension, kwargs):
        log_name = kwargs['log_name']
        doc_handler = DocHandler(kwargs)
        loguru_import = __import__('loguru', globals(), locals(), [], 0)
        loguru_import.logger.remove()
        log = loguru_import.logger
        log.add(f'logfiles/{log_name}.info', format='{time} {level} {message}',
                filter=lambda record: record["level"].name == "INFO")
        log.add(f'logfiles/{log_name}.error', format='{time} {level} {message}',
                filter=lambda record: record["level"].name == "ERROR")
        try:
            pulleti = Processor([PERSON])
            processed_file = ProcessedFile(filename=filename, path=filepath)
            log.info(f'get text from file id: {record_id} {processed_file.path}')
            file_text = doc_handler.handler_get_text(processed_file.path, extension)
            log.info(f'handler output file id: {record_id} {processed_file.path}')
            paragraphs, number_map, persons_map = doc_handler.handler_output_file(filename, file_text, pulleti)
            log.info(f'save to db id: {record_id} {processed_file.path}')
            doc_date = doc_handler.date_settings(kwargs, filepath)
            doc_handler.db.update_record(record_id, document_status['success'], number_map, paragraphs, persons_map,
                                         doc_date)
            log.info(f'processing completed {record_id} {processed_file.path}')
        except (SoftTimeLimitExceeded, TimeLimitExceeded):
            log.error(f'process timeout: {record_id} {filepath}')
            doc_handler.db.update_record(record_id, document_status['timeout'], [], [], [], None)
            return
        except UnicodeDecodeError:
            log.error(f'decode error: {record_id} {filepath}')
            doc_handler.db.update_record(record_id, document_status['unicode'], [], [], [], None)
            return
        except FileNotFoundError:
            log.error(f'file not found: {record_id} {filepath}')
            if kwargs['delete_non_existent']:
                doc_handler.db.delete_record(record_id)
                return
        except CalledProcessError:
            log.error(f'process error: {record_id} {filepath}')
            doc_handler.db.update_record(record_id, document_status['process'], [], [], [], None)
        except Exception as e:
            log.error(f'unexpected {e}: {filepath}')
            doc_handler.db.update_record(record_id, document_status['unexpected'], [], [], [], None)
            return
        pass

    def run_retrain_proj(self, doc_id, delete_non_existent):
        self.doc_handler_log.info('Run retrain proj')
        self.doc_handler_log.info('Get list files from database')
        db = DataBase(self.path2base, self.ip_base, self.port)
        kwargs = {
            'ip_base': self.ip_base,
            'port': self.port,
            'path2base': self.path2base,
            'log_name': self.log_name,
            'auto_date': self.auto_date,
            'doc_date': self.doc_date,
            'delete_non_existent': delete_non_existent,
        }
        offset = 0
        limit = 100
        documents = db.get_documents_by_status(self.status_array, doc_id, limit)
        pulleti = Processor([PERSON])
        del pulleti
        while documents:
            for document in documents:
                while 1:
                    message_count = self.tasks_count('priority.high')
                    if message_count < TASK_LIMIT:
                        break
                filename, extension = delete_extension(document.path2doc)
                self.retrain_proj_celery.apply_async(
                    args=(document.id, document.filename, document.path2doc, extension, kwargs), queue='priority.high',
                    time_limit=self.time_processing + 20,
                    soft_time_limit=self.time_processing)
                #self.retrain_proj_celery(document.id, document.filename, document.path2doc, extension, kwargs)
            offset = offset + limit
            timeout = 10
            reconnect_count = 10
            while reconnect_count:
                try:
                    documents = db.get_documents_by_status(self.status_array, doc_id, limit, offset)
                    break
                except SQLAlchemyError as e:
                    error = str(e.__dict__['orig'])
                    self.doc_handler_log.error(f'{error}: attempts left - {reconnect_count} timeout - {timeout}')
                    time.sleep(timeout)
                    timeout = timeout * 10
                    reconnect_count -= 1
                    continue
        pass


if __name__ == '__main__':
    filepath_2 = """/mnt/Test/B73_31-12-2019 20_53_42 48047 49802.txt"""
    with open(filepath_2, "rt", encoding='cp1251') as file:
        string = file.read()
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
        'search_numbers': True,
        'test': True,
    }
    proj = ProjectsInit(**init_map)
    # doc_handler.run_entity_proj(1)
    # doc_handler.run_retraining_proj(1)
    proj.run_entity_with_celery(init_map['search_numbers'], init_map['search_pers_data'],
                                init_map['check_processed_file'])
    pass
