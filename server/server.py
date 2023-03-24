from processes import ExtractEntityTask, Task, RetrainTask
from logging_ import ProjectLog


class ProjectWrapper:
    """
    Класс обертка для запуска/остановки/отслеживания статуса задачи(проекта)
    """

    def __init__(self, alias: str):
        self.alias = alias
        self.task: None or Task = None
        self.project_log = ProjectLog(alias)

    def start_proj(self, proj_type: str, options: dict):
        """Запуск задачи в зависимости от его типа"""
        if proj_type == 'extract_entity_proj':
            self._start_extract_proj(options)
        if proj_type == 'retrain_proj':
            self._start_retrain_proj(options)

    def _start_extract_proj(self, options):
        """Преобразование опций поступающих с web socket и запуск задачи Извлечение именнованных сущностей"""
        folder = options['options']['folder']
        extensions = [ext['extension'] for ext in options['options']['doc_extension']]
        only_new_files = options['options'].get('only_new_files', False)
        raw_data = options['options'].get('raw_data', False)
        process_count = options['options']['process_count']
        delete_not_found = options['options'].get('delete_not_found', False)
        self.task = ExtractEntityTask(folder, extensions, only_new_files, raw_data,
                                      delete_not_found, self.project_log)
        self.task.start(process_count)

    def _start_retrain_proj(self, options):
        """Преобразование опций поступающих с web socket и запуск задачи Переобучение выборки"""
        doc_status = [_['id'] for _ in options['options']['status']]
        record_id = options['options']['record_id']
        raw_data = options['options'].get('raw_data', False)
        process_count = options['options']['process_count']
        delete_not_found = options['options'].get('delete_not_found', False)
        self.task = RetrainTask(doc_status, record_id, raw_data, delete_not_found,
                                self.project_log)
        self.task.start(process_count)

    def status(self):
        """Отслеживание статуса задачи для передачи его в web socket"""
        return self.task.status()

    def stop(self):
        """Остановка задачи"""
        del self.project_log
        self.task.stop()
