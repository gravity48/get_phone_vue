from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@extend_schema_view(
    post=extend_schema(
        tags=[
            _('jwt'),
        ]
    )
)
class JwtToken(TokenObtainPairView):
    ...


@extend_schema_view(
    post=extend_schema(
        tags=[
            _('jwt'),
        ]
    )
)
class TokenRefresh(TokenRefreshView):
    ...
