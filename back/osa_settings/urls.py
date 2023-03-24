from django.urls import path, re_path
from . import views

app_name = 'OSA_settings'

urlpatterns = [
    path('', views.OSASettingsView.as_view(), name='index'),
]
