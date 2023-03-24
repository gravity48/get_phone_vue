import django, datetime, json
import os
import copy
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, FileResponse, Http404, HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import generic
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from functools import wraps
from get_phone_view.middleware.login_all import login_exempt
from . import forms

# Custom Login View Django.

event_list = {'login', 'registration', 'logout'}


def parse_event(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        error_map = {'error': 'No event', }
        try:
            data = json.loads(args[0].body)
            event = data['event']
        except (ValueError, json.JSONDecodeError):
            return JsonResponse(error_map, status=settings.ERROR_STATUS)
        if event in event_list:
            kwargs['event'] = event
            kwargs['data'] = data
            response = func(*args, **kwargs)
            return response
        else:
            return JsonResponse(error_map, status=settings.ERROR_STATUS)
    return wrapper


decorators = [parse_event, login_exempt]


@method_decorator(login_exempt, name='get')
@method_decorator(decorators, name='post')
class LoginView(generic.View):
    template_name = 'custom_auth/login.html'
    login_exempt = True

    @staticmethod
    def _login_method(data, request):
        login_form = forms.LoginForm(data)
        if login_form.is_valid():
            login = data['login']
            password = data['password']
            user: User = authenticate(request, username=login, password=password)
            django.contrib.auth.login(request, user)
            if login_form.cleaned_data['remember']:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)
            group_list = list(map(lambda x: x.name, user.groups.all()))
            request.session['group_users'] = group_list
            next_page = request.GET.get("next", "/")
            return {'success': True, "next_page": next_page}, settings.SUCCESS_STATUS
        else:
            errors = json.loads(login_form.errors.as_json())
            return errors, settings.ERROR_STATUS

    @staticmethod
    def _logout(request):
        response = {'success': True}
        django.contrib.auth.logout(request)
        return response, settings.SUCCESS_STATUS

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect('index:index')
        return render(request, self.template_name)

    def post(self, request: HttpRequest, event: str, data):
        if event == 'login':
            response, status = self._login_method(data, request)
            return JsonResponse(response, status=status)
        if event == 'logout':
            response, status = self._logout(request)
            return JsonResponse(response, status=status)
        return JsonResponse({'status': 'ok'})
