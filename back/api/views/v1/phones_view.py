from collections import OrderedDict

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.v1.phones_serializers import (
    PhoneSerializer,
    PhoneResponseSerializer,
    UserResponseSerializer,
    ExtraParamsSerializer,
)
from index.models import UserRequestsList
from services.paginators import PhonePaginator
from services.phones.render import PhonesRender


@extend_schema_view(
    post=extend_schema(
        description=_('get numbers'),
        request=PhoneSerializer(many=True),
        responses={200: UserResponseSerializer(many=True)},
        tags=[
            _('view'),
        ],
    ),
)
class PhonesAPIView(APIView):
    paginator_class = PhonePaginator()

    @transaction.atomic
    def post(self, request):
        serializer = PhoneSerializer(data=self.request.data, many=True)
        serializer.is_valid(raise_exception=True)
        request_instance = serializer.save(user=self.request.user)
        context = PhonesRender(
            request_instance, self.paginator_class, PhoneResponseSerializer
        ).render_data()
        return Response(data=context, status=status.HTTP_200_OK)


class PhonesDetailView(APIView):
    paginator_class = PhonePaginator()

    def get(self, request, pk):
        user_request = get_object_or_404(UserRequestsList, pk)
        context = PhonesRender(
            user_request, self.paginator_class, PhoneResponseSerializer
        ).render_data()
        return Response(data=context, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, pk):
        request_instance = get_object_or_404(UserRequestsList, pk=pk)
        serializer = ExtraParamsSerializer(
            data=request.data, context={'request_instance': request_instance}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(self.request.user)
        context = PhonesRender(
            request_instance, self.paginator_class, PhoneResponseSerializer
        ).render_phone(serializer.validated_data['number'])
        return Response(data=context, status=status.HTTP_200_OK)
