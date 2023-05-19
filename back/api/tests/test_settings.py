from django.test import TestCase
from django.urls import reverse

from api.models import SettingsModel
from base.test import BaseTestView


class SettingsTest(BaseTestView, TestCase):
    settings: SettingsModel
    url = reverse('settings')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.settings = SettingsModel.objects.create(
            id=1,
            db_ip='127.0.0.1',
            db_port=5432,
            db_login='admin',
            db_password='admin',
        )

    def test_010_get_settings(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token(self.auth_user))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_020_update_settings(self):
        valid_data = {
            'ip': '127.0.0.1',
        }
        self.auth()
        response = self.client.put(self.url, valid_data)
        self.assertEqual(response.status_code, 200)


class ExtensionsViewTest(BaseTestView, TestCase):
    url = reverse('extensions')

    def test_010_get_extensions(self):
        self.auth()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class StatusViewTest(BaseTestView, TestCase):
    url = reverse('status')

    def test_010_get_status(self):
        self.auth()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
