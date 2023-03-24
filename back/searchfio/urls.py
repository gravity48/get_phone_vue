from django.urls import path, re_path
from . import views

app_name = 'search_fio'

urlpatterns = [
    path('', views.SearchfioView.as_view(), name='index'),
    #path('/download_excel', views.DownloadExcelView.as_view(), name='download_excel'),
]
