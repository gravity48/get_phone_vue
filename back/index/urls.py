from django.urls import path, re_path
from django.conf.urls.static import static
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.IndexViewApi.as_view(), name='index'),
    path('phones/', views.IndexViewApi.as_view(), name='index'),
    path('training/', views.IndexViewApi.as_view(), name='index'),
    path('settings/', views.IndexViewApi.as_view(), name='index'),
]
