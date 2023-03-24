from django.urls import path, re_path
from . import views

app_name = 'search_numbers'

urlpatterns = [
    path('', views.SearchNumbersView.as_view(), name='index'),
    path('download_excel/', views.DownloadExcelView.as_view(), name='download_excel'),
]
