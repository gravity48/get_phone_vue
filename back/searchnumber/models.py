from django.db import models
from django.contrib.auth.models import User


class QuestionHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    numbers_json = models.JSONField()
    fio_json = models.JSONField()
