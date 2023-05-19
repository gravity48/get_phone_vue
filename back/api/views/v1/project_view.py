from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics

from api.models import ProjectsSettings
from api.serializers.v1.project import (
    ProjSettingsListSerializer,
    ProjSettingsCreateUpdateSerializer,
    ProjSettingsRetrieveSerializer,
)
from base.view import PartialUpdateMixin


@extend_schema_view(
    get=extend_schema(
        description=_('get projects list'),
        responses={200: ProjSettingsListSerializer(many=True)},
        tags=[
            _('project'),
        ],
    ),
    post=extend_schema(
        description=_('create project'),
        request=ProjSettingsCreateUpdateSerializer,
        responses={200: ProjSettingsCreateUpdateSerializer},
        tags=[
            _('project'),
        ],
    ),
)
class ProjSettingsListCreateView(generics.ListCreateAPIView):
    queryset = ProjectsSettings.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjSettingsListSerializer
        if self.request.method == 'POST':
            return ProjSettingsCreateUpdateSerializer


@extend_schema_view(
    get=extend_schema(
        description=_('get project detail'),
        responses={200: ProjSettingsListSerializer(many=True)},
        tags=[
            _('project'),
        ],
    ),
    put=extend_schema(
        description=_('update project'),
        request=ProjSettingsCreateUpdateSerializer,
        responses={200: ProjSettingsCreateUpdateSerializer},
        tags=[
            _('project'),
        ],
    ),
    delete=extend_schema(
        description=_('delete project'),
        tags=[
            _('project'),
        ],
    ),
)
class ProjSettingsDetailView(PartialUpdateMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectsSettings.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjSettingsRetrieveSerializer
        elif self.request.method == 'PUT':
            return ProjSettingsCreateUpdateSerializer
