from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, "User")
router.register(r'extensions', views.ExtensionsViewSet, 'Extensions')
router.register(r'doc_status', views.DocStatusViewSet, 'DocStatus')
router.register(r'proj_settings_list', views.ProjectSettingListView, 'ProjSettingsList')

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('database/', views.DataBaseViewSet.as_view(), name='database'),
    path('proj_settings/', views.ProjectSettingsView.as_view(), name='proj_settings'),
    path('proj_control/', views.ProjectStartView.as_view(), name='proj_control'),
    path('phones/', views.PhonesView.as_view(), name='phones_view'),
    path('directories/', views.DirectoriesView.as_view(), name='directories'),
    path('', include(router.urls)),
]
