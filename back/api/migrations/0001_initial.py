# Generated by Django 4.2.1 on 2023-05-17 16:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DocExtensionModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("extension", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "doc_extensions",
            },
        ),
        migrations.CreateModel(
            name="DocStatusModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status_name", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "doc_status",
            },
        ),
        migrations.CreateModel(
            name="DocumentsModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("filename", models.CharField(max_length=500)),
                ("filepath", models.CharField(max_length=1000)),
                ("date", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.docstatusmodel",
                    ),
                ),
            ],
            options={
                "db_table": "documents",
            },
        ),
        migrations.CreateModel(
            name="ParagraphsModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                (
                    "doc",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.documentsmodel",
                    ),
                ),
            ],
            options={
                "db_table": "paragraphs",
            },
        ),
        migrations.CreateModel(
            name="ProjectsSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("proj_type", models.CharField(max_length=100)),
                ("options", models.JSONField(default=dict)),
                ("is_start", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "project_settings",
            },
        ),
        migrations.CreateModel(
            name="SettingsModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "db_ip",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}:[1-9][0-9]{0,6}$"
                            )
                        ],
                    ),
                ),
                ("db_port", models.IntegerField()),
                ("db_path", models.CharField(max_length=300)),
                ("db_login", models.CharField(max_length=100)),
                ("db_password", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "settings",
            },
        ),
        migrations.CreateModel(
            name="TelephonesModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.TextField(verbose_name=50)),
                ("number_integer", models.BigIntegerField()),
                (
                    "paragraph",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.paragraphsmodel",
                    ),
                ),
            ],
            options={
                "db_table": "telephones",
                "indexes": [
                    models.Index(fields=["number_integer"], name="telephones_number__987a1e_idx"),
                    models.Index(fields=["number"], name="telephones_number_45a49b_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="SurnamesModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("patronymic", models.CharField(max_length=100)),
                ("surname", models.CharField(max_length=100)),
                (
                    "paragraph",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.paragraphsmodel",
                    ),
                ),
            ],
            options={
                "db_table": "surnames",
                "indexes": [
                    models.Index(fields=["name"], name="surnames_name_99dcd5_idx"),
                    models.Index(fields=["patronymic"], name="surnames_patrony_3d2f28_idx"),
                    models.Index(fields=["surname"], name="surnames_surname_67a3f6_idx"),
                ],
            },
        ),
        migrations.AddIndex(
            model_name="documentsmodel",
            index=models.Index(fields=["date"], name="documents_date_11c106_idx"),
        ),
    ]
