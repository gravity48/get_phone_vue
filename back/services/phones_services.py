from typing import List

from django.db.models import QuerySet

from api.models import TelephonesModel


def get_queryset(phones: List[str]) -> QuerySet:
    phones_int = [int(phone) for phone in phones]
    return TelephonesModel.objects.filter(number_integer__in=phones_int)


def search_number_contains(text: str, number: str) -> str:
    return ''
