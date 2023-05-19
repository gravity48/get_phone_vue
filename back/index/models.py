from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


#
# ENTITY_PROJ = 1
# RETRAINING_PROJ = 2
#
#
# class ProjectType(models.Model):
#     proj_name = models.TextField(unique=True)
#
#     class Meta:
#         db_table = 'proj_type'
#
#
# class ProjectSettings(models.Model):
#     proj_settings = models.JSONField()
#     proj_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
#     is_run = models.BooleanField(default=False)
#     project_id = models.TextField(default='')
#     log_file = models.FileField(blank=True, null=True, storage=settings.DEFAULT_FILE_STORAGE)
#


class UserRequestsList(models.Model):
    request = models.CharField(max_length=1000)
    validate_data = models.JSONField(default=dict)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'requests'
        verbose_name = _('request')
        verbose_name_plural = _('requests')
