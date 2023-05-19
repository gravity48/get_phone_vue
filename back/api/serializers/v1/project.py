from rest_framework import serializers

from api.models import ProjectsSettings


class ProjSettingsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsSettings
        fields = (
            'proj_type',
            'is_start',
        )


class ProjSettingsCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsSettings
        exclude = ('created_at',)


class ProjSettingsRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsSettings
        fields = '__all__'
