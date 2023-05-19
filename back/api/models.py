import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.validators import ip_validator


class DocStatusModel(models.Model):
    status_name = models.CharField(_("documents status name"), max_length=100)

    class Meta:
        db_table = 'doc_status'
        verbose_name = _('doc status')
        verbose_name_plural = _('doc status')


#
# class DocumentsModel(models.Model):
#     status = models.ForeignKey(
#         DocStatusModel,
#         on_delete=models.CASCADE,
#         verbose_name=_("doc status"),
#     )
#     filename = models.CharField(_("filename"), max_length=500)
#     filepath = models.CharField(_("filepath"), max_length=1000)
#     date = models.DateTimeField(_("document date"), blank=True, null=True)
#
#     class Meta:
#         db_table = 'documents'
#         verbose_name = _('document')
#         verbose_name_plural = _('documents')
#         indexes = [
#             models.Index(fields=['date']),
#         ]
#
#
# class ParagraphsModel(models.Model):
#     doc = models.ForeignKey(
#         DocumentsModel,
#         on_delete=models.CASCADE,
#         verbose_name=_(),
#     )
#     text = models.TextField()
#
#     class Meta:
#         db_table = 'paragraphs'
#
#
# class TelephonesModel(models.Model):
#     paragraph = models.ForeignKey(ParagraphsModel, on_delete=models.CASCADE)
#     number = models.TextField(50)
#     number_integer = models.BigIntegerField()
#
#     class Meta:
#         db_table = 'telephones'
#         indexes = [models.Index(fields=['number_integer']), models.Index(fields=['number'])]
#
#
# class SurnamesModel(models.Model):
#     paragraph = models.ForeignKey(ParagraphsModel, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     patronymic = models.CharField(max_length=100)
#     surname = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = 'surnames'
#         indexes = [
#             models.Index(fields=['name']),
#             models.Index(fields=['patronymic']),
#             models.Index(fields=['surname']),
#         ]
#
#


class SettingsModel(models.Model):
    db_ip = models.CharField(
        _('database ip'),
        max_length=100,
        validators=[
            ip_validator,
        ],
    )
    db_port = models.IntegerField(
        _('db port'),
    )
    db_path = models.CharField(_('database path'), max_length=300)
    db_login = models.CharField(_('database login'), max_length=100)
    db_password = models.CharField(_('database password'), max_length=100)

    class Meta:
        db_table = 'settings'
        verbose_name = _('settings')
        verbose_name_plural = _('settings')


class DocExtensionModel(models.Model):
    extension = models.CharField(_('extension name'), max_length=30)

    class Meta:
        db_table = 'doc_extensions'
        verbose_name = _('extension')
        verbose_name_plural = _('extensions')


class ProjectsSettings(models.Model):
    id = models.UUIDField(
        _('project id'),
        default=uuid.uuid4,
        primary_key=True,
    )

    class ProjTypeChoices(models.TextChoices):
        SEARCH = "SR", _("Search proj")
        REFRESH = "RF", _("Refresh proj")

    proj_type = models.CharField(
        _('proj type'),
        max_length=100,
        choices=ProjTypeChoices.choices,
        default=ProjTypeChoices.SEARCH,
    )
    options = models.JSONField(
        _('proj options'),
        default=dict,
    )
    is_start = models.BooleanField(
        _('proj is started'),
        default=False,
    )
    created_at = models.DateTimeField(
        _('proj created at'),
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'project_settings'
        verbose_name = _('project setting')
        verbose_name_plural = _('projects settings')
