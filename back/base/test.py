from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class BaseTestView:
    url: str
    auth_user: User
    databases = {"default", "osa_extra"}

    @classmethod
    def setUpTestData(cls):
        cls.auth_user = User.objects.create_user(
            'user',
            'user@email.com',
            'user',
        )

    def setUp(self) -> None:
        self.client = APIClient()

    @staticmethod
    def get_token(user) -> str:
        refresh = RefreshToken.for_user(user)
        return f'Bearer {refresh.access_token}'

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token(self.auth_user))
