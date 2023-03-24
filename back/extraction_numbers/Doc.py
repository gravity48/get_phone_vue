import pullenti
from pullenti_wrapper.processor import Processor, PERSON
import re
import natasha
from natasha import NamesExtractor, MorphVocab, PER, Segmenter, NewsNERTagger, NewsEmbedding, NewsMorphTagger, \
    NewsSyntaxParser
import extraction_numbers.re_named_entities as re_named_entities


class Doc:
    def __init__(self, doc_line, docname, pulleti_processor=None, stop_regex=None):
        self._doc_line = doc_line
        self._paragraph_list = re.split('\n{2,}', self._doc_line)
        self.docname = docname
        if pulleti_processor: self.pulleti_processor = pulleti_processor
        if stop_regex: self.stop_regex = stop_regex
        self.regex_list_phone = []
        for regex_numbers in re_named_entities.regex_numbers_str:
            self.regex_list_phone.append(re.compile(regex_numbers))
        self.regex_fio = re.compile(re_named_entities.regex_fio_str)

    def __str__(self):
        return self._doc_line

    def get_paragraphs(self):
        return self._paragraph_list

    def extractions_numbers(self, numbers_map):
        for item, paragraph in enumerate(self._paragraph_list):
            self.__extract_number_by_regex(numbers_map, paragraph, item)
        pass

    def extractions_persons_data(self, persons_map):
        for item, paragraph in enumerate(self._paragraph_list):
            # self._extract_person_natasha(persons_data_map, paragraph, item)
            self._extract_person_regex(persons_map, paragraph, item)
            # self._extract_persons_pulleti(persons_data_map, paragraph, item)
        pass

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
        result = self.pulleti_processor(paragraph)
        for match in result.matches:
            try:
                person = {
                    'first': match.referent.firstname,
                    'middle': match.referent.middlename,
                    'last': match.referent.lastname,
                }
            except AttributeError:
                continue
            if None in person.values():
                continue
            elif self.name_filter(person):
                persons_data_map[item].append(person)
        pass

    def _extract_person_natasha(self, persons_data_map, paragraph, item):
        morph_vocab = MorphVocab()
        names_extractor = NamesExtractor(morph_vocab)
        segmenter = Segmenter()
        emb = NewsEmbedding()
        doc_natasha = natasha.Doc(paragraph)
        ner_tagger = NewsNERTagger(emb)
        doc_natasha.segment(segmenter)
        doc_natasha.tag_ner(ner_tagger)
        for span in doc_natasha.spans:
            if span.type == PER:
                span.normalize(morph_vocab)
                span.extract_fact(names_extractor)
                try:
                    personal_data = span.fact.as_dict.values()
                except AttributeError:
                    continue
                if len(personal_data) == 3:
                    persons_data_map[item].append(span.fact.as_dict)
        pass

    def _extract_person_regex(self, persons_data_map, paragraph, item):
        match = self.regex_fio.search(paragraph)
        if match is not None:
            # self._extract_person_natasha(persons_data_map,paragraph, item)
            self._extract_persons_pulleti(persons_data_map, paragraph, item)

    @staticmethod
    def clean_number(number):
        '''
        PREVIOUS NUMBER CLEAN
        number_clear = re.sub(r'(^(\+?7|8|\+?38)|\D)', '', number)
        '''
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
        '''
        PREVIOUS REGULAR EXPRESSIONS
        re.compile(r"(?P<prefix>\+?7|8|\+?38)?[\s(-]*(?P<code>[09]\d{2})[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}"),
        re.compile(r"(?P<prefix>\+?38)?[\s(-]*(?P<code>0\d{2})\d[\s)-]*\d{2}[\s-]*\d{2}[\s-]*\d{2}")]
        '''
        for regex in self.regex_list_phone:
            self.__execute_regex(regex, paragraph, item, number_map)
        pass

    pass
