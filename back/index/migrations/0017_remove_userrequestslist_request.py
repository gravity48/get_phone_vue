# Generated by Django 4.2.1 on 2023-05-19 13:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("index", "0016_remove_userrequestslist_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userrequestslist",
            name="request",
        ),
    ]
