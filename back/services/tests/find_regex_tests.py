from unittest import TestCase

from faker import Faker

from services.regular_expression import FindRegex


class FindRegexTest(TestCase):
    def setUp(self) -> None:
        self.fake = Faker(['ru_Ru', 'uk_UA'])
        self.service = FindRegex()

    def test_010_find_ua_number(self):
        ua_phone = self.fake.numerify('+38 0## ###-##-##')
        paragraph = f'{self.fake.text()} {ua_phone} {self.fake.text()}'
        ua_phone = self.service.clear_phone(ua_phone)
        ua_phone = ua_phone[2:]
        status, _ = self.service.find_phone(paragraph, ua_phone)
        self.assertEqual(status, True)

    def test_020_find_ru_number(self):
        ru_phone = self.fake.numerify('+7 9## ###-##-##')
        paragraph = f'{self.fake.text()} {ru_phone} {self.fake.text()}'
        ru_phone = self.service.clear_phone(ru_phone)
        ru_phone = ru_phone[1:]
        status, _ = self.service.find_phone(paragraph, ru_phone)
        self.assertEqual(status, True)

    def test_030_find_in_more_phone(self):
        ru_phone = self.fake.unique.numerify('+7 9## ### ## ##')
        phones_fake = [self.fake.unique.numerify('+7 9## ### ## ## ') for _ in range(10)]
        paragraph_fake = [self.fake.text() for _ in range(10)]
        paragraph_fake[-1] = f'{paragraph_fake[-1][2]} {ru_phone} {paragraph_fake[-1][2:]}'
        paragraph_list = [x for y in zip(phones_fake, paragraph_fake) for x in y]
        paragraph = ''.join(paragraph_list)
        ru_phone = self.service.clear_phone(ru_phone)
        ru_phone = ru_phone[1:]
        status, _ = self.service.find_phone(paragraph, ru_phone)
        self.assertEqual(status, True)

    def test_040_view_offset_number_in_middle(self):
        ru_phone = self.fake.numerify('+7 9## ### ## ##')
        paragraph = f'{self.fake.text()} {ru_phone}{self.fake.text()}'
        clear_phone = self.service.clear_phone(ru_phone)[1:]
        status, selection = self.service.find_phone(paragraph, clear_phone)
        self.assertEqual(status, True)

    def test_050_view_offset_number_in_start(self):
        ua_phone = self.fake.numerify('+38 0## ###-##-##')
        paragraph = f'{ua_phone} {self.fake.text()}'
        clear_phone = self.service.clear_phone(ua_phone)[2:]
        status, selection = self.service.find_phone(paragraph, clear_phone)
        self.assertTrue(status)
        self.assertEqual(selection.start, '')

    def test_060_view_offset_number_in_end(self):
        ua_phone = self.fake.numerify('+38 0## ###-##-##')
        paragraph = f'{self.fake.text()}{ua_phone}'
        clear_phone = self.service.clear_phone(ua_phone)[2:]
        status, selection = self.service.find_phone(paragraph, clear_phone)
        self.assertTrue(status)
        self.assertEqual(selection.end, '')
