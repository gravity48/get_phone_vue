import re
from collections import defaultdict
from typing import Pattern, List, Dict
from pullenti_wrapper.processor import Processor
from .stop_words import STOP_WORDS_COMPILE
from .re_named_entities import REGEX_NUMBER_COMPILE, REGEX_FIO_COMPILE


class Doc:
    stop_regex: Pattern = STOP_WORDS_COMPILE
    regex_list_phone: List[Pattern] = REGEX_NUMBER_COMPILE
    regex_fio: Pattern = REGEX_FIO_COMPILE

    def __init__(self, doc_line, pulleti_processor: Processor):
        self._doc_line: str = doc_line
        self._paragraph_list: List[str] = re.split('\n{2,}', self._doc_line)
        self.pulleti_processor = pulleti_processor

    def __str__(self):
        return self._doc_line

    def get_paragraphs(self) -> List[str]:
        return self._paragraph_list

    def get_numbers_map(self) -> Dict[int, List[str]]:
        numbers_map = defaultdict(list)
        for item, paragraph in enumerate(self._paragraph_list):
            self.__extract_number_by_regex(numbers_map, paragraph, item)
        return numbers_map

    def get_person_map(self) -> Dict[int, List[str]]:
        persons_map = defaultdict(list)
        for item, paragraph in enumerate(self._paragraph_list):
            # self._extract_person_natasha(persons_data_map, paragraph, item)
            self._extract_person_regex(persons_map, paragraph, item)
        return persons_map

    def extractions_numbers(self, numbers_map):
        for item, paragraph in enumerate(self._paragraph_list):
            self.__extract_number_by_regex(numbers_map, paragraph, item)

    def extractions_persons_data(self, persons_map):
        for item, paragraph in enumerate(self._paragraph_list):
            # self._extract_person_natasha(persons_data_map, paragraph, item)
            self._extract_person_regex(persons_map, paragraph, item)
            # self._extract_persons_pulleti(persons_data_map, paragraph, item)

    def name_filter(self, person: dict):
        person_string = ''
        for value in person.values():
            if len(value) < 2:
                return False
            person_string += f'{value} '
        if self.stop_regex.search(person_string):
            return False
        return True

    def _extract_persons_pulleti(self, persons_data_map, paragraph, item):
        try:
            result = self.pulleti_processor(paragraph)
            for match in result.matches:
                person = {
                    'first': match.referent.firstname,
                    'middle': match.referent.middlename,
                    'last': match.referent.lastname,
                }
                if None in person.values():
                    continue
                elif self.name_filter(person):
                    persons_data_map[item].append(person)
        except AttributeError:
            return

    def _extract_person_regex(self, persons_data_map, paragraph, item):
        match = self.regex_fio.search(paragraph)
        if match is not None:
            # self._extract_person_natasha(persons_data_map,paragraph, item)
            self._extract_persons_pulleti(persons_data_map, paragraph, item)

    @staticmethod
    def clean_number(number):
        """
        PREVIOUS NUMBER CLEAN
        number_clear = re.sub(r'(^(\+?7|8|\+?38)|\D)', '', number)
        """
        number_clear = re.sub(r'\D', '', number)
        return number_clear

    @staticmethod
    def is_registered(code):
        match = re.search(r'9\d{2}|0[1-9]\d', code)
        if match is None:
            return False
        else:
            return True



    def __execute_regex(self, regex, paragraph, item, number_map):
        result = regex.finditer(paragraph)
        for match in result:
            code = match.group('code')
            if self.is_registered(code):
                number = match.group('phone')
                number_clear = self.clean_number(number)
                if number_clear not in number_map[item]:
                    number_map[item].append(number_clear)
        pass

    def __extract_number_by_regex(self, number_map, paragraph, item):
        """
        PREVIOUS REGULAR EXPRESSIONS
        re.compile(r"(?P<prefix>\+?7|8|\+?38)?[\s(-]*(?P<code>[09]\d{2})[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}"),
        re.compile(r"(?P<prefix>\+?38)?[\s(-]*(?P<code>0\d{2})\d[\s)-]*\d{2}[\s-]*\d{2}[\s-]*\d{2}")]
        """
        for regex in self.regex_list_phone:
            self.__execute_regex(regex, paragraph, item, number_map)

    pass
