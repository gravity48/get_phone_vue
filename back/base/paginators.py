from collections import OrderedDict
from typing import Type

from django.core.paginator import Paginator, InvalidPage
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound


class AbstractPhonePaginator:
    page_size: int
    django_paginator_class: Type[Paginator]

    def get_paginated_data(self, data, phone):
        raise NotImplementedError

    def paginate_queryset(self, queryset, filter_params: dict, phone: str):
        raise NotImplementedError


class PhonePageNumberPaginator(AbstractPhonePaginator):
    def get_paginated_data(self, data, phone):
        return OrderedDict(
            [
                ('number', phone),
                ('count', self.page.paginator.count),
                ('num_pages', self.page.paginator.num_pages),
                ('page', self.page.number),
                ('results', data),
            ]
        )

    @staticmethod
    def get_page_number(paginator, filter_params: dict, phone: str):
        page_number = filter_params.get(phone, 1)
        if page_number > paginator.num_pages:
            raise NotFound(_(f'Page {page_number} not found'))
        return page_number

    def paginate_queryset(self, queryset, filter_params: dict, phone: str):
        paginator = self.django_paginator_class(queryset, self.page_size)
        page_number = self.get_page_number(paginator, filter_params, phone)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage:
            raise NotFound(_(f'Page {page_number} not found'))
        return list(self.page)
