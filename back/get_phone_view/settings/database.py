import os

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASE_ROUTERS = ['get_phone_view.routers.OsaExtraRouter', 'get_phone_view.routers.DefaultRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["POSTGRES_DB"],
        'USER': os.environ["POSTGRES_USER"],
        'PASSWORD': os.environ["POSTGRES_PASSWORD"],
        'HOST': os.environ["POSTGRES_HOST"],
        'PORT': os.environ["POSTGRES_PORT"],
    },
    'osa_extra': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["STORAGE_DB_NAME"],
        'USER': os.environ["STORAGE_DB_USER"],
        'PASSWORD': os.environ["STORAGE_DB_PASSWORD"],
        'HOST': os.environ["STORAGE_DB_HOST"],
        'PORT': os.environ["STORAGE_DB_PORT"],
    },
}
