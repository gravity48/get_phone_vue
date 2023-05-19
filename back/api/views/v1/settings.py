from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import SettingsModel, DocExtensionModel, DocStatusModel
from api.serializers.v1.settings import SettingsSerializer, ExtensionSerializer, DocStatusSerializer


@extend_schema_view(
    get=extend_schema(
        description=_('Get settings data'),
        responses={200: SettingsSerializer},
        tags=[
            _('settings'),
        ],
    ),
    put=extend_schema(
        description=_("Update settings data"),
        responses={200: SettingsSerializer},
        tags=[
            _('settings'),
        ],
    ),
)
class SettingsView(APIView):
    serializer_class = SettingsSerializer

    @staticmethod
    def get_object():
        return SettingsModel.objects.get(pk=1)

    @staticmethod
    def get_serializer_class(request):
        return SettingsSerializer

    def get(self, request):
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        description=_('Get doc extensions'),
        responses={200: ExtensionSerializer(many=True)},
        tags=[
            _('settings'),
        ],
    ),
)
class ExtensionsView(generics.ListAPIView):
    queryset = DocExtensionModel.objects.all()
    serializer_class = ExtensionSerializer


@extend_schema_view(
    get=extend_schema(
        description=_('Get status documents'),
        responses={200: DocStatusSerializer(many=True)},
        tags=[
            _('settings'),
        ],
    ),
)
class DocStatusViewSet(generics.ListAPIView):
    queryset = DocStatusModel.objects.all()
    serializer_class = DocStatusSerializer
