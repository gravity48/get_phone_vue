import os

from django.core.paginator import Paginator

from base.paginators import PhonePageNumberPaginator


class PhonePaginator(PhonePageNumberPaginator):
    page_size = os.environ['PAGE_SIZE']
    django_paginator_class = Paginator
