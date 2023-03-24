from django.db import models


class OSASettings(models.Model):
    server_name = models.TextField()
    path2base = models.TextField()
    port = models.IntegerField()
    temp_dir = models.TextField()
    is_run = models.BooleanField()
    records_number_on_page = models.IntegerField(default=5)
    archive_path = models.TextField(default='')
    indent = models.IntegerField(default=100)

    class Meta:
        db_table = 'osa_settings'
