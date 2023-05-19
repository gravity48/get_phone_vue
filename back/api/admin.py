from django.contrib import admin

from api.models import DocExtensionModel, SettingsModel, DocStatusModel


# Register your models here.


@admin.register(DocExtensionModel)
class ExtensionsAdmin(admin.ModelAdmin):
    list_display = ('extension',)


@admin.register(SettingsModel)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('db_ip',)


@admin.register(DocStatusModel)
class DocStatusAdmin(admin.ModelAdmin):
    list_display = ('status_name',)
