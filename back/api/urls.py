from django.contrib.auth.models import User
from django.urls import path, include
from api.views.v1.jwt import JwtToken, TokenRefresh
from api.views.v1.project_view import ProjSettingsListCreateView, ProjSettingsDetailView
from api.views.v1.settings import SettingsView, ExtensionsView, DocStatusViewSet

#
# router = routers.DefaultRouter()
# router.register(r'extensions', views.ExtensionsViewSet, 'Extensions')
# router.register(r'doc_status', views.DocStatusViewSet, 'DocStatus')
# router.register(r'proj_settings_list', views.ProjectSettingListView, 'ProjSettingsList')
#
# urlpatterns = router.urls


settings_urls = [
    path('database/', SettingsView.as_view(), name='settings'),
    path('extensions/', ExtensionsView.as_view(), name='extensions'),
    path('status/', DocStatusViewSet.as_view(), name='status'),
]

jwt_urls = [
    path('token/', JwtToken.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefresh.as_view(), name='token_refresh'),
]

project_urls = [
    path('projects/', ProjSettingsListCreateView.as_view(), name='projects'),
    path('projects/<uuid:pk>/', ProjSettingsDetailView.as_view(), name='project_detail'),
]

generic_patterns = [
    # path('database/', views.DataBaseViewSet.as_view(), name='database'),
    # path('proj_settings/', views.ProjectSettingsView.as_view(), name='proj_settings'),
    # path('proj_control/', views.ProjectStartView.as_view(), name='proj_control'),
    # path('phones/', views.PhonesView.as_view(), name='phones_view'),
    # path('directories/', views.DirectoriesView.as_view(), name='directories'),
]

urlpatterns = [
    path('settings/', include(settings_urls)),
    path('jwt/', include(jwt_urls)),
    path('project/', include(project_urls)),
]
