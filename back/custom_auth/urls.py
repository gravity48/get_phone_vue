from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

app_name = 'custom_auth'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
]
