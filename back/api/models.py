import re
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class DocStatusModel(models.Model):
    class StatusChoices(models.TextChoices):
        success = 'success', _('Success')
        timeout = 'timeout', _('Timeout')
        unicode = 'unicode', _('Unicode')
        unexpected = 'unexpected', _('Unexpected')
        process = 'process', _('Process')

    status_name = models.CharField(max_length=100, choices=StatusChoices.choices)

    class Meta:
        db_table = 'doc_status'


class DocumentsModel(models.Model):
    status = models.ForeignKey(DocStatusModel, on_delete=models.CASCADE)
    filename = models.CharField(max_length=500)
    filepath = models.CharField(max_length=1000)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'documents'
        indexes = [
            models.Index(fields=['date']),
        ]


class ParagraphsModel(models.Model):
    doc = models.ForeignKey(DocumentsModel, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        db_table = 'paragraphs'


class TelephonesModel(models.Model):
    paragraph = models.ForeignKey(ParagraphsModel, on_delete=models.CASCADE)
    number = models.TextField(50)
    number_integer = models.BigIntegerField()

    class Meta:
        db_table = 'telephones'
        indexes = [
            models.Index(fields=['number_integer']),
            models.Index(fields=['number'])
        ]


class SurnamesModel(models.Model):
    paragraph = models.ForeignKey(ParagraphsModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    class Meta:
        db_table = 'surnames'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['patronymic']),
            models.Index(fields=['surname']),
        ]


class SettingsModel(models.Model):
    db_ip = models.CharField(max_length=100,
                             validators=[RegexValidator(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[1-9][0-9]{0,6}$')])
    db_port = models.IntegerField()
    db_path = models.CharField(max_length=300)
    db_login = models.CharField(max_length=100)
    db_password = models.CharField(max_length=100)

    class Meta:
        db_table = 'settings'


class DocExtensionModel(models.Model):
    class ExtensionChoices(models.TextChoices):
        doc = 'doc', _('Doc')
        docx = 'docx', _('Docx')
        xls = 'xls', _('Xls')
        xlsx = 'xlsx', _('Xlsx')
        txt = 'txt', _('Txt')
        rtf = 'rtf', _('Rtf')
        csv = 'csv', _('Csv')

    extension = models.CharField(max_length=30, choices=ExtensionChoices.choices)

    class Meta:
        db_table = 'doc_extensions'


class ProjectsSettings(models.Model):
    proj_type = models.CharField(max_length=100)
    options = models.JSONField(default=dict)
    is_start = models.BooleanField(default=False)

    class Meta:
        db_table = 'project_settings'


