import json
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import generic
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import OSASettings
from searchnumber.models import QuestionHistory
from . import models, forms


def user_is_staff(user):
    return user.is_staff


decorators = [settings.LOGGER.catch, user_passes_test(user_is_staff, login_url=reverse_lazy('search_numbers:index'))]


@method_decorator(decorators, name='get')
@method_decorator(decorators, name='post')
class OSASettingsView(generic.View):
    template_name = 'osa_settings/osa_settings.html'

    @staticmethod
    def __connect2base(data):
        base_connect_form = forms.BaseConnectForm(data)
        if base_connect_form.is_valid():
            server_name = base_connect_form.cleaned_data['server_ip']
            path2base = base_connect_form.cleaned_data['database_name']
            port = base_connect_form.cleaned_data['port']
            osa_settings = OSASettings.objects.all()[:1].get()
            osa_settings.server_name = server_name
            osa_settings.path2base = path2base
            osa_settings.port = port
            osa_settings.save()
            context = {
                'success': True,
                'text_info': 'Connect change successfully',
            }
            return context, settings.SUCCESS_STATUS
        else:
            errors = json.loads(base_connect_form.errors.as_json())
            return errors, settings.ERROR_STATUS

    @staticmethod
    def _add_user(data):
        user_form = forms.UserAddForm(data)
        if user_form.is_valid():
            user = User.objects.create_user(user_form.cleaned_data['username'], user_form.cleaned_data['email'],
                                            user_form.cleaned_data['pw_1'])
            question_history = QuestionHistory(user=user, numbers_json=[], fio_json={})
            user.questionhistory = question_history
            user.save()
            context = {
                'success': True,
                'text_info': 'User add successfully',
            }
            return context, settings.SUCCESS_STATUS
        else:
            errors = json.loads(user_form.errors.as_json())
            return errors, settings.ERROR_STATUS

    @staticmethod
    def _del_user(data):
        user_del_form = forms.UserDelForm(data)
        if user_del_form.is_valid():
            User.objects.filter(pk=user_del_form.cleaned_data['id']).delete()
            context = {
                'success': True,
                'info': 'User delete successfully',
            }
            return context, settings.SUCCESS_STATUS
        else:
            errors = json.loads(user_del_form.errors.as_json())
            return errors, settings.ERROR_STATUS

    def get(self, request):
        osa_settings = OSASettings.objects.all()[:1].get()
        users = User.objects.all()
        context = {
            'osa_settings': osa_settings,
            'is_run': osa_settings.is_run,
            'users': users,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        data = json.loads(request.body)
        try:
            event = data['event']
        except KeyError:
            return JsonResponse({'error': 'No event'}, status=settings.ERROR_STATUS)
        if event == 'connect2base':
            response, status = self.__connect2base(data)
            return JsonResponse(response, status=status)
        if event == 'add_user':
            response, status = self._add_user(data)
            return JsonResponse(response, status=status)
        if event == 'del_user':
            response, status = self._del_user(data)
        return JsonResponse({'status': 'success'}, status=settings.SUCCESS_STATUS)
