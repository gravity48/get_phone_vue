import re
import os
from django import forms
from django.conf import settings
from django.core.validators import ValidationError
from django.core.exceptions import FieldError
from django.forms import CharField, IntegerField


class SearchPrsDataForm(forms.Form):
    last_name = CharField(max_length=100, required=True)
    first_name = CharField(max_length=100, required=False)
    patronymic = CharField(max_length=100, required=False)

    def clean(self):
        self.cleaned_data['last_name'] = self.cleaned_data['last_name'].upper()
        self.cleaned_data['first_name'] = self.cleaned_data['first_name'].upper()
        self.cleaned_data['patronymic'] = self.cleaned_data['patronymic'].upper()
        return self.cleaned_data
