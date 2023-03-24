import re

regex_numbers_str = [
    r"(^|\D|\n)(?P<prefix>\+?7|8|\+?38)?[\s(-]*(?P<phone>(?P<code>[09]\d{2})[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2})($|\D)",
    r"(^|\D|\n)(?P<prefix>\+?38)?[\s(-]*(?P<phone>(?P<code>0\d{2})\d[\s)-]*\d{2}[\s-]*\d{2}[\s-]*\d{2})($|\D)",
    r"(^|\D|\n)(?P<prefix>\+?7|8|\+?38)?[\s(-]*(?P<phone>(?P<code>[09]\d{2})[\s)-]*\d{2}[\s-]*\d[\s-]\d{2}[\s-]*\d{2})($|\D)",
]
regex_fio_str = r"""([А-ЯЁЇІЄҐ][а-яёїієґ']{2,}\x20){2}[А-ЯЁЇІЄҐ][а-яёїієґ']{2,}"""

REGEX_NUMBER_COMPILE = [re.compile(regex_numbers) for regex_numbers in regex_numbers_str]
REGEX_FIO_COMPILE = re.compile(regex_fio_str)

__all__ = ['REGEX_NUMBER_COMPILE', 'REGEX_FIO_COMPILE', ]
