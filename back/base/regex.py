import re
from collections import namedtuple
from typing import List, Tuple, Type

from get_phone_view.settings import VIEW_OFFSET

NumberSelection = namedtuple('NumberSelection', ['start', 'phone', 'end'])


class RegexStorageAbstract:
    def load_number_regex(self) -> List[str]:
        raise NotImplementedError

    def load_persons_regex(self) -> List[str]:
        raise NotImplementedError


class FindRegexBase:
    storage: RegexStorageAbstract

    def __init__(self):
        self._phone_regex = self.storage.load_number_regex()
        self._person_regex = self.storage.load_persons_regex()

    @staticmethod
    def clear_phone(phone: str) -> str:
        return re.sub(r'\D', '', phone)

    @staticmethod
    def _selection_number(text, start, end):
        return NumberSelection(
            text[start - VIEW_OFFSET : start], text[start:end], text[end : end + VIEW_OFFSET]
        )

    def find_phone(self, text: str, phone: str) -> Tuple[bool, NumberSelection]:
        for regex in self._phone_regex:
            matches = re.compile(regex).finditer(text)
            for match in matches:
                number = match.group('phone')
                number_clear = self.clear_phone(number)
                if number_clear == phone:
                    selection_text = self._selection_number(text, *match.span())
                    return True, selection_text
            return False, NumberSelection('', phone, '')
