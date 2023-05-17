REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 'EXCEPTION_HANDLER': 'api.utils.custom_exception_handler',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'OSA extra',
    'DESCRIPTION': 'Извлекает именованные сущности из текстовых документов',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
