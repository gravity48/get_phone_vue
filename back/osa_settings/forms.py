import re
from django import forms
from django.forms import CharField, IntegerField
from extraction_numbers.DocHeandler import DocHandler
from extraction_numbers.class_data_base import DataBase
from django.contrib.auth.models import User


def ip_validation(value):
    msg = "Неверный IP"
    expression_string = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    ip_string = re.search(expression_string, value)
    if ip_string:
        return False
    else:
        return msg


def port_validation(value):
    if not value:
        return False
    msg = 'Неверный порт'
    expression_string = r'\D'
    unacceptable_symbols = re.search(expression_string, value)
    if unacceptable_symbols:
        return msg
    else:
        return False


class BaseConnectForm(forms.Form):
    server_ip = CharField(required=True)
    database_name = CharField(required=True)
    port = CharField(required=False)
    event = CharField(required=False)

    def clean(self):
        if not self.errors:
            try:
                server_ip, port = re.split(r'/', self.cleaned_data['server_ip'])
            except ValueError:
                self.add_error('server_ip', 'Подключение в неверном формате')
                return self.cleaned_data
            if ip_validation(server_ip):
                self.add_error('server_ip', ip_validation(server_ip))
                return self.cleaned_data
            if port_validation(port):
                self.add_error('server_ip', port_validation(port))
                return self.cleaned_data
            argv = {
                'path2db': self.cleaned_data['database_name'],
                'server_ip': server_ip,
                'port': port,
            }
            db_firebird = DataBase(**argv)
            if not db_firebird.try_connection():
                self.add_error('event', 'no connect to base')
            self.cleaned_data['port'] = port
            self.cleaned_data['server_ip'] = server_ip
            return self.cleaned_data


class UserAddForm(forms.Form):
    username = CharField(required=True)
    pw_1 = CharField(required=True)
    pw_2 = CharField(required=True)
    email = CharField(required=False)
    event = CharField(required=True)

    def clean(self):
        if not self.errors:
            username = self.cleaned_data['username']
            pw_1 = self.cleaned_data['pw_1']
            pw_2 = self.cleaned_data['pw_2']
            if pw_1 != pw_2:
                self.add_error('event', 'Пароли не совпадают')
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                self.add_error('event', 'Выберите другой логин')
            self.cleaned_data['email'] = f'{username}@mail.com'
            return self.cleaned_data


class UserDelForm(forms.Form):
    id = IntegerField(required=True)

    def clean(self):
        try:
            User.objects.get(pk=self.cleaned_data['id'])
        except User.DoesNotExist:
            self.add_error('id', 'Пользователя не существует')
        return self.cleaned_data
