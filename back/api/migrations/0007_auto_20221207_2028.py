# Generated by Django 3.2 on 2022-12-07 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20221207_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingsmodel',
            name='db_login',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settingsmodel',
            name='db_password',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
