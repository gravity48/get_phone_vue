from rest_framework import serializers

from api.models import SettingsModel, DocExtensionModel, DocStatusModel, ProjectsSettings


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsModel
        fields = '__all__'


class ExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocExtensionModel
        fields = '__all__'


class DocStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocStatusModel
        fields = '__all__'
