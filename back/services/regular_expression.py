import re
from typing import List

regex_numbers_str = [
    r"(^|\D|\n)(?P<prefix>\+?7|8|\+?38)?[\s(-]*(?P<phone>(?P<code>[09]\d{2})[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2})($|\D)",
    r"(^|\D|\n)(?P<prefix>\+?38)?[\s(-]*(?P<phone>(?P<code>0\d{2})\d[\s)-]*\d{2}[\s-]*\d{2}[\s-]*\d{2})($|\D)",
    r"(^|\D|\n)(?P<prefix>\+?7|8|\+?38)?[\s(-]*(?P<phone>(?P<code>[09]\d{2})[\s)-]*\d{2}[\s-]*\d[\s-]\d{2}[\s-]*\d{2})($|\D)",
]
regex_fio_str = r"""([А-ЯЁЇІЄҐ][а-яёїієґ']{2,}\x20){2}[А-ЯЁЇІЄҐ][а-яёїієґ']{2,}"""


class RegexStorage:
    def load_number_regex(self) -> List[str]:
        ...

    def load_persons_regex(self) -> List[str]:
        ...


class FindRegex:
    storage = RegexStorage()

    def __init__(self):
        self.regex_ = self.storage.load_number_regex()

    def find(self, target, regex_list) -> str:
        ...
