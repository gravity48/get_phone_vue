from collections import namedtuple
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from api.models import DocumentsModel, SettingsModel, DocExtensionModel, ProjectsSettings, DocStatusModel
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from extraction_numbers.class_data_base_new import DataBase
from extraction_numbers.websocket_client import WebSocketClient


FolderSerializer = namedtuple('FolderSerializer', ['name', 'path', 'sub_folders'])


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data['is_staff'] = self.user.is_staff
        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.is_staff = validated_data.get('is_staff', False)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'date_joined', 'password']


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsModel
        fields = '__all__'


class DataBaseSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsModel
        fields = '__all__'


class DataBaseSettingsUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(error_messages=settings.DEF_ERROR_MESSAGES)
    db_ip = serializers.CharField(max_length=100,
                                  validators=[RegexValidator(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[1-9][0-9]{0,6}$')],
                                  error_messages=settings.DEF_ERROR_MESSAGES)
    db_port = serializers.IntegerField(error_messages=settings.DEF_ERROR_MESSAGES)
    db_path = serializers.CharField(max_length=300, error_messages=settings.DEF_ERROR_MESSAGES)
    db_login = serializers.CharField(max_length=100, error_messages=settings.DEF_ERROR_MESSAGES)
    db_password = serializers.CharField(max_length=100, error_messages=settings.DEF_ERROR_MESSAGES)

    def validate(self, attrs):
        if WebSocketClient().sync_database(attrs):
            return attrs
        raise serializers.ValidationError('Соединение к базе данных отсутствует')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DocExtensionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocExtensionModel
        fields = '__all__'


class DocStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocStatusModel
        fields = '__all__'


class ProjectSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsSettings
        fields = '__all__'


class ProjectSettingsUpdateSerializer(serializers.Serializer):
    options = serializers.JSONField(error_messages=settings.DEF_ERROR_MESSAGES)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PhoneViewSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=200)
    paragraph = serializers.CharField(source='paragraph__text')
    filepath = serializers.CharField(max_length=1000, source='paragraph__doc__filepath')
    doc_date = serializers.DateTimeField(source='paragraph__doc__date')
    filename = serializers.CharField(max_length=100, source='paragraph__doc__filename')





