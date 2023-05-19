import json

from django.test import TestCase
from django.urls import reverse

from api.models import ProjectsSettings
from base.test import BaseTestView


class ProjectListTest(BaseTestView, TestCase):
    url = reverse('projects')
    created: ProjectsSettings

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.created = ProjectsSettings.objects.create(
            proj_type=ProjectsSettings.ProjTypeChoices.SEARCH,
            options={
                'proj': 123,
            },
            is_start=False,
        )

    def test_010_get_proj_list(self):
        self.auth()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_020_create_proj(self):
        options = {
            'proj': 'cool',
        }
        data = {
            'proj_type': "SR",
            'options': json.dumps(options),
            'is_start': False,
        }
        self.auth()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)

    def test_030_retrieve(self):
        self.auth()
        response = self.client.get(f'{self.url}{self.created.id}/')
        self.assertEqual(response.status_code, 200)

    def test_040_update(self):
        data = {
            'is_start': True,
        }
        self.auth()
        response = self.client.put(f'{self.url}{self.created.id}/', data)
        self.assertEqual(response.status_code, 200)

    def test_050_delete(self):
        self.auth()
        response = self.client.delete(f'{self.url}{self.created.id}/')
        self.assertEqual(response.status_code, 204)
