'''
BACKUP TXT

path2log = models.FileField(blank=True, null=True,
                                storage=settings.DEFAULT_FILE_STORAGE)
    path2files = models.TextField(blank=True, null=True)
    is_run = models.BooleanField(default=False)
    project_id = models.TextField(default='')
    time_processing = models.IntegerField(default=60)
    thread_count = models.IntegerField(default=1)



        log_data_folders_map = {
            'data_folder':  project_settings.path2files,
            'log_name':  project_settings.path2log.name,
            'time_processing': project_settings.time_processing,
            'thread_count': project_settings.thread_count,
        }
        log_data_form = forms.LogDataFoldersForm(log_data_folders_map)
        if not log_data_form.is_valid():
            return {'error_txt': 'LogFormValid'}, settings.ERROR_STATUS


'''
