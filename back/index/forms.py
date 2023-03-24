import re
import os
from django import forms
from django.core.validators import ValidationError
from django.forms import CharField, IntegerField, BooleanField, JSONField
from extraction_numbers.DocHeandler import DocHandler


class IpValidator:
    message = 'Неверный IP'
    code = 'invalid'
    validators = []

    def test_re(self, value: str) -> None:
        expression_string = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        ip_string = re.search(expression_string, value)
        if ip_string is None:
            raise ValidationError(self.message, self.code)
        return None

    def __init__(self):
        self.validators = [self.test_re, ]

    def __call__(self, value: str):
        for validator in self.validators:
            validator(value)
        return


class LogDataFoldersForm(forms.Form):
    data_folder = CharField(required=True)
    log_name = CharField(required=True)
    time_processing = IntegerField(required=True)
    event = CharField(required=False)
    doc_date = CharField(required=False)
    check_processed_file = BooleanField(required=False)
    search_pers_data = BooleanField(required=False)
    search_numbers = BooleanField(required=False)
    data_array = JSONField(required=True)
    auto_date = BooleanField(required=False)
    sync_proj = BooleanField(required=False)

    def clean(self):
        if not self.errors:
            if not os.path.exists(self.cleaned_data['data_folder']):
                self.add_error('event', 'no files/folder')
            if self.cleaned_data['auto_date']:
                self.cleaned_data['doc_date'] = None
            return self.cleaned_data
    pass


class StopProjForm(forms.Form):
    proj_name = forms.CharField()


class RetrainingProjForm(forms.Form):
    log_name = CharField()
    time_processing = IntegerField(required=True)
    search_pers_data = BooleanField(required=False)
    search_numbers = BooleanField(required=False)
    data_array = JSONField(required=False)
    auto_date = BooleanField(required=False)
    doc_date = CharField(required=False)
    doc_id = IntegerField(required=True)
    delete_non_existent = BooleanField(required=False)

