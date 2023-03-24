from django import forms
from django.forms.fields import CharField, EmailField
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    login = CharField(max_length=50)
    password = CharField(max_length=50)
    remember = CharField(required=False, max_length=5)

    def clean(self):
        if not self.errors:
            login_current = self.cleaned_data['login']
            password_current = self.cleaned_data['password']
            user = authenticate(username=login_current, password=password_current)
            if user is not None:
                return self.cleaned_data
            else:
                raise forms.ValidationError('Неверный логин/пароль')