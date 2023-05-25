import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRequestsList(models.Model):
    class RequestType(models.TextChoices):
        PHONE_REQUEST = "PH", _("phone request")
        PERSON_REQUEST = "PR", _("person request")

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    filter_params = models.JSONField(
        _('filter params to queryset'),
        default=dict,
    )
    validate_data = models.JSONField(_('valid data request'), default=dict)
    user = models.ForeignKey(
        User, verbose_name=_('users query'), on_delete=models.CASCADE, related_name='requests'
    )
    request_type = models.CharField(max_length=2, choices=RequestType.choices)

    created_at = models.DateTimeField(
        _('request created date'),
        auto_now_add=True,
    )

    class Meta:
        db_table = 'requests'
        verbose_name = _('request')
        verbose_name_plural = _('requests')
