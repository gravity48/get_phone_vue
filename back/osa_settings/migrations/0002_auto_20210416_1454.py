# Generated by Django 3.1.6 on 2021-04-16 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osa_settings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='osasettings',
            name='default_log',
        ),
        migrations.AddField(
            model_name='osasettings',
            name='is_run',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
