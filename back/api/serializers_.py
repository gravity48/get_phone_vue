# from collections import namedtuple
# from django.conf import settings
# from django.contrib.auth.models import User
# from django.core.validators import RegexValidator
# from api.models import (
#     DocumentsModel,
#     SettingsModel,
#     DocExtensionModel,
#     ProjectsSettings,
#     DocStatusModel,
# )
# from rest_framework import serializers
#
# FolderSerializer = namedtuple('FolderSerializer', ['name', 'path', 'sub_folders'])
#
##
#
# class DocumentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DocumentsModel
#         fields = '__all__'
#
#

#

#
# class DocExtensionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DocExtensionModel
#         fields = '__all__'
#
#

#
# class ProjectSettingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectsSettings
#         fields = '__all__'
#
#
# class ProjectSettingsUpdateSerializer(serializers.Serializer):
#     options = serializers.JSONField(error_messages={})
#
#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance
#
#
# class PhoneViewSerializer(serializers.Serializer):
#     number = serializers.CharField(max_length=200)
#     paragraph = serializers.CharField(source='paragraph__text')
#     filepath = serializers.CharField(max_length=1000, source='paragraph__doc__filepath')
#     doc_date = serializers.DateTimeField(source='paragraph__doc__date')
#     filename = serializers.CharField(max_length=100, source='paragraph__doc__filename')
