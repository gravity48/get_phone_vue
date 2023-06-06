import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from api.models import DocumentsModel, DocStatusModel, ParagraphsModel, TelephonesModel
from base.test import BaseTestView
from index.models import UserRequestsList


class SettingsTest(BaseTestView, TestCase):
    url = reverse('phones')

    @classmethod
    def setUpTestData(cls):
        super(SettingsTest, cls).setUpTestData()
        status = DocStatusModel.objects.create(
            status_name='success',
        )
        doc = DocumentsModel.objects.create(
            status=status,
            filename='123.doc',
            filepath='/mnt/123.doc',
        )
        paragraph = ParagraphsModel.objects.create(
            doc=doc,
            text='paragraph 9835689823 text',
        )
        phones_list = []
        for item in range(100):
            phones_list.append(
                TelephonesModel(paragraph=paragraph, number='9835689823', number_integer=9835689823)
            )
        TelephonesModel.objects.bulk_create(phones_list)

    def test_010_get_phones_data(self):
        self.auth()
        data = [
            {
                'phone': '9804443223',
            },
            {
                'phone': '9804445421',
            },
            {'phone': '9835689823'},
        ]
        response = self.client.post(
            self.url, data=json.dumps(data, indent=2), content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_020_post_phone_detail_view(self):
        request_instance = UserRequestsList(
            filter_params={},
            user=self.auth_user,
            validate_data=['9804443223', '9804445421', '9835689823'],
            request_type=UserRequestsList.RequestType.PHONE_REQUEST,
        )
        request_instance.save()
        self.auth()
        valid_data = {
            'number': '9835689823',
            'page_id': 2,
        }
        request = self.client.post(f'{self.url}{request_instance.id}/', valid_data)
        self.assertEqual(request.status_code, 200)
        request_instance = UserRequestsList.objects.get(pk=request_instance.id)
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token(self.another_user))
        valid_data = {
            'number': '9835689823',
            'page_id': 3,
        }
        request = self.client.post(f'{self.url}{request_instance.id}/', valid_data)
        self.assertEqual(request.status_code, 200)
        request_instance = UserRequestsList.objects.get(pk=request_instance.id)
