import os

import dj_database_url

from .settings import *
from .settings import BASE_DIR


SECRET_KEY = os.environ.get('SECRET_KEY') or os.environ.get('SECRET') or SECRET_KEY
DEBUG = os.environ.get('DJANGO_DEBUG', '').lower() == 'true'

render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
custom_hosts = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [
    host.strip()
    for host in [render_hostname, *custom_hosts.split(',')]
    if host and host.strip()
]

csrf_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in csrf_origins.split(',')
    if origin.strip()
]
if render_hostname:
    CSRF_TRUSTED_ORIGINS.append(f'https://{render_hostname}')

if not ALLOWED_HOSTS and not DEBUG:
    ALLOWED_HOSTS = ['.onrender.com']

if 'django_browser_reload' in INSTALLED_APPS:
    INSTALLED_APPS.remove('django_browser_reload')

MIDDLEWARE = [
    middleware
    for middleware in MIDDLEWARE
    if middleware != 'django_browser_reload.middleware.BrowserReloadMiddleware'
]
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    security_index = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
    MIDDLEWARE.insert(security_index + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STORAGES = {
    **globals().get('STORAGES', {}),
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

database_url = os.environ.get('DATABASE_URL')
if database_url:
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=database_url.startswith('postgres'),
        )
    }
elif os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING'):
    connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
    parameters = {
        pair.split('=')[0]: pair.split('=')[1]
        for pair in connection_string.split(' ')
        if '=' in pair
    }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parameters['dbname'],
            'HOST': parameters['host'],
            'USER': parameters['user'],
            'PASSWORD': parameters['password'],
        }
    }

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'true').lower() == 'true'
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '0'))
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend',
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'true').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') or os.environ.get('EMAIL_PASSWORD', '')
