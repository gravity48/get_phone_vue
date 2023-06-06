import re
from typing import List

from base.regex import RegexStorageAbstract, FindRegexBase


class FileRegexStorage(RegexStorageAbstract):
    def load_number_regex(self) -> List[str]:
        return [
            r"(^|\D|\n)(?P<prefix>\+?7|8|\+?38)?[\s(-]*(?P<phone>(?P<code>[09]\d{2})[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2})($|\D)",
            r"(^|\D|\n)(?P<prefix>\+?38)?[\s(-]*(?P<phone>(?P<code>0\d{2})\d[\s)-]*\d{2}[\s-]*\d{2}[\s-]*\d{2})($|\D)",
            r"(^|\D|\n)(?P<prefix>\+?7|8|\+?38)?[\s(-]*(?P<phone>(?P<code>[09]\d{2})[\s)-]*\d{2}[\s-]*\d[\s-]\d{2}[\s-]*\d{2})($|\D)",
        ]

    def load_persons_regex(self) -> List[str]:
        return [
            r"""([А-ЯЁЇІЄҐ][а-яёїієґ']{2,}\x20){2}[А-ЯЁЇІЄҐ][а-яёїієґ']{2,}""",
        ]


class FindRegex(FindRegexBase):
    storage = FileRegexStorage()
