import re
import os
from django import forms
from django.conf import settings
from django.core.validators import ValidationError
from django.core.exceptions import FieldError
from django.forms import CharField, IntegerField
from collections import namedtuple
CheckCorrectTelephones = namedtuple('CheckCorrectTelephones', ['status', 'error'])


def number_validation(value):
    match = re.search(r'^\d{10}($|\n)', value)
    if not match:
        raise ValidationError('number not registered', code='invalid')
    return match.group(0)


class SearchNumbersForm(forms.Form):
    search_string = CharField(max_length=20, validators=[number_validation, ])


def check_file_size(value):
    if value.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError('the file has exceeded the maximum size')


class FileForm(forms.Form):
    file = forms.FileField(validators=(check_file_size,))
    search_string = CharField(required=False)

    def clean(self):
        if not self.errors:
            numbers_list = list()
            with self.cleaned_data['file'].open("rb") as file:
                lines = file.readlines()
            for line_number, line in enumerate(lines):
                try:
                    number = number_validation(line.decode())
                    numbers_list.append(int(number))
                except (ValidationError, ValueError):
                    self.add_error('search_string', f'Error in line {line_number + 1}')
                    return self.cleaned_data
            self.cleaned_data['numbers_list'] = numbers_list
            return self.cleaned_data

