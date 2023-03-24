from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from functools import wraps
from get_phone_view.celery import app
from osa_settings.forms import BaseConnectForm
from osa_settings.models import OSASettings
from index.tasks import launch_entity_proj, launch_retrain_proj
from django_celery_results.models import TaskResult
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from . import forms, models
import json


def user_is_staff(user):
    return user.is_staff


decorators = [settings.LOGGER.catch, user_passes_test(user_is_staff, login_url=reverse_lazy('search_numbers:index'))]


@method_decorator(decorators, name='get')
@method_decorator(decorators, name='post')
class IndexView(generic.View):
    template_name = 'index/index.html'
    template_log = 'index/logfiles.html'

    @staticmethod
    def __set_entity_proj(data):
        log_data_form = forms.LogDataFoldersForm(data)
        if log_data_form.is_valid():
            try:
                project_settings: models.ProjectSettings = models.ProjectSettings.objects.filter(
                    proj_type=models.ENTITY_PROJ).get()
                project_settings.proj_settings = log_data_form.cleaned_data
                project_settings.log_file = log_data_form.cleaned_data['log_name']
                project_settings.save()
            except models.ProjectSettings.DoesNotExist:
                return {'errors': 'no migrations'}, settings.ERROR_STATUS
            return {'success': True}, settings.SUCCESS_STATUS
        else:
            errors = json.loads(log_data_form.errors.as_json())
            return errors, settings.ERROR_STATUS

    @staticmethod
    def __run_entity_project(data):
        osa_settings = OSASettings.objects.all()[:1].get()
        entity_settings = models.ProjectSettings.objects.filter(proj_type=models.ENTITY_PROJ).get()
        base_connection_map = {
            'server_ip': f'{osa_settings.server_name}/{osa_settings.port}',
            'database_name': osa_settings.path2base
        }
        base_form = BaseConnectForm(base_connection_map)
        if not base_form.is_valid():
            return {'error_txt': 'Connection Failed'}, settings.ERROR_STATUS
        init_map = {
            'default_log': entity_settings.proj_settings['log_name'],
            'input_dir': entity_settings.proj_settings['data_folder'],
            'time_processing': entity_settings.proj_settings['time_processing'],
            'output_dir': settings.TEMP_DIR,
            'path2base': osa_settings.path2base,
            'ip_base': osa_settings.server_name,
            'port': osa_settings.port,
            'auto_date': entity_settings.proj_settings['auto_date'],
            'doc_date': entity_settings.proj_settings['doc_date'],
            'extensions_array': entity_settings.proj_settings['data_array'],
            'check_processed_file': entity_settings.proj_settings['check_processed_file'],
            'sync_proj': entity_settings.proj_settings['sync_proj'],
        }
        # delay
        project_id = launch_entity_proj.delay(init_map)
        settings.LOGGER.success('Run entity project')
        entity_settings.project_id = project_id.id
        entity_settings.is_run = True
        entity_settings.save()
        return {'success': True}, settings.SUCCESS_STATUS

    @staticmethod
    def __set_retraining_proj(data):
        retraining_proj_form = forms.RetrainingProjForm(data)
        if retraining_proj_form.is_valid():
            project_settings = models.ProjectSettings.objects.get(proj_type=models.RETRAINING_PROJ)
            project_settings.proj_settings = retraining_proj_form.cleaned_data
            project_settings.log_file = retraining_proj_form.cleaned_data['log_name']
            project_settings.save()
            return {'success': True}, settings.SUCCESS_STATUS
        else:
            errors = json.loads(retraining_proj_form.errors.as_json())
            return errors, settings.ERROR_STATUS

    @staticmethod
    def run_retraining_proj(data):
        osa_settings = OSASettings.objects.all()[:1].get()
        retrain_settings = models.ProjectSettings.objects.filter(proj_type=models.RETRAINING_PROJ).get()
        base_connection_map = {
            'server_ip': f'{osa_settings.server_name}/{osa_settings.port}',
            'database_name': osa_settings.path2base
        }
        base_form = BaseConnectForm(base_connection_map)
        if not base_form.is_valid():
            return {'error_txt': 'Connection Failed'}, settings.ERROR_STATUS
        init_map = {
            'default_log': retrain_settings.proj_settings['log_name'],
            'time_processing': retrain_settings.proj_settings['time_processing'],
            'output_dir': settings.TEMP_DIR,
            'path2base': osa_settings.path2base,
            'ip_base': osa_settings.server_name,
            'port': osa_settings.port,
            'auto_date': retrain_settings.proj_settings['auto_date'],
            'doc_date': retrain_settings.proj_settings['doc_date'],
            'status_array': retrain_settings.proj_settings['data_array'],
            'doc_id': retrain_settings.proj_settings['doc_id'],
            'delete_non_existent': retrain_settings.proj_settings['delete_non_existent'],
        }
        # delay
        project_id = launch_retrain_proj.delay(init_map)
        settings.LOGGER.success('Run retrain project')
        retrain_settings.project_id = project_id.id
        retrain_settings.is_run = True
        retrain_settings.save()
        return {'success': True}, settings.SUCCESS_STATUS

    def update_log(self):
        project_settings = models.ProjectSettings.objects.filter(is_run=True).first()
        if project_settings is None: return {'error': 'no running project'}, settings.ERROR_STATUS
        try:
            with open(f'{project_settings.log_file.path}.info') as info_log:
                text = info_log.readlines()
                render_html = render_to_string(self.template_log, {'text': text})
        except FileNotFoundError:
            return {'error': 'no log file found'}, settings.ERROR_STATUS
        return {'success': True, 'render_html': render_html}, settings.SUCCESS_STATUS

    @staticmethod
    def stop_proj(data):
        stop_proj_form = forms.StopProjForm(data)
        if stop_proj_form.is_valid():
            task_id = None
            if stop_proj_form.cleaned_data['proj_name'] == 'entity_proj':
                task_id = \
                    models.ProjectSettings.objects.values('project_id').get(proj_type=models.ENTITY_PROJ)[
                        'project_id']
                app.control.revoke(task_id, terminate=True, signal='SIGKILL')
                models.ProjectSettings.objects.filter(proj_type=models.ENTITY_PROJ).update(is_run=False)
            if stop_proj_form.cleaned_data['proj_name'] == 'retrain_proj':
                task_id = \
                    models.ProjectSettings.objects.values('project_id').get(proj_type=models.RETRAINING_PROJ)[
                        'project_id']
                app.control.revoke(task_id, terminate=True, signal='SIGKILL')
                models.ProjectSettings.objects.filter(proj_type=models.RETRAINING_PROJ).update(is_run=False)
            return {'success': True}, settings.SUCCESS_STATUS
        else:
            errors = json.loads(stop_proj_form.errors.as_json())
            return errors, settings.ERROR_STATUS

    def get(self, request):
        file_extensions = models.FileExtensions.objects.all()
        entity_settings = models.ProjectSettings.objects.filter(proj_type=models.ENTITY_PROJ).get()
        retraining_settings = models.ProjectSettings.objects.filter(proj_type=models.RETRAINING_PROJ).get()
        doc_status = models.DocumentStatus.objects.all()
        context = {
            'entity_settings': entity_settings,
            'retraining_settings': retraining_settings,
            'file_extensions': file_extensions,
            'doc_status': doc_status,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        try:
            event = data['event']
        except KeyError:
            return JsonResponse({'error': 'No event'}, status=settings.ERROR_STATUS)
        if event == 'set_entity_proj':
            response, status = self.__set_entity_proj(data)
            return JsonResponse(response, status=status)
        if event == 'run_entity_proj':
            response, status = self.__run_entity_project(data)
            return JsonResponse(response, status=status)
        if event == 'set_retraining_proj':
            response, status = self.__set_retraining_proj(data)
            return JsonResponse(response, status=status)
        if event == 'run_retraining_proj':
            response, status = self.run_retraining_proj(data)
            return JsonResponse(response, status=status)
        if event == 'update_log':
            response, status = self.update_log()
            return JsonResponse(response, status=status)
        if event == 'stop_proj':
            response, status = self.stop_proj(data)
            return JsonResponse(response, status=status)
        return JsonResponse({'error': 'No event'}, status=settings.SUCCESS_STATUS)


class IndexViewApi(generic.View):
    template_name = 'index/index.html'

    def get(self, request):
        return render(request, self.template_name)
