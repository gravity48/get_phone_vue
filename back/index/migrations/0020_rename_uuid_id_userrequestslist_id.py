# Generated by Django 4.2.1 on 2023-05-23 22:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("index", "0019_remove_userrequestslist_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userrequestslist",
            old_name="uuid_id",
            new_name="id",
        ),
    ]
