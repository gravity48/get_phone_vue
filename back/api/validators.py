from django.core.validators import RegexValidator


def ip_validator(value):
    return RegexValidator(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[1-9][0-9]{0,6}$')(value)
