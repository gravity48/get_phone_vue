from collections import OrderedDict
from typing import Type

from rest_framework.serializers import Serializer

from api.models import TelephonesModel
from base.paginators import PhonePageNumberPaginator
from index.models import UserRequestsList


class PhonesRender:
    def __init__(self, requests_instance, paginator, serializer):
        self.request: UserRequestsList = requests_instance
        self.paginator_class: PhonePageNumberPaginator = paginator
        self.serializer_class: Type[Serializer] = serializer

    def render_phone(self, number) -> OrderedDict:
        queryset = TelephonesModel.objects.filter(number_integer=int(number)).order_by(
            'paragraph__doc__date'
        )
        page = self.paginator_class.paginate_queryset(queryset, self.request.filter_params, number)
        serializer = self.serializer_class(instance=page, many=True)
        queryset_data = self.paginator_class.get_paginated_data(serializer.data, number)
        return queryset_data

    def render_data(self) -> OrderedDict:
        numbers = [phone for phone in self.request.validate_data]
        data = list()
        for number in numbers:
            queryset_data = self.render_phone(number)
            data.append(queryset_data)
        context = OrderedDict(
            [
                ('request_id', self.request.id),
                ('data', data),
            ]
        )
        return context
