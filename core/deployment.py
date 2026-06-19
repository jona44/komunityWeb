import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR


# -------------------------------------------------------------------
# Core secrets — must be set as env vars on Render
# -------------------------------------------------------------------
SECRET_KEY = os.environ['SECRET']

DEBUG = False

# -------------------------------------------------------------------
# Hosts — Render injects RENDER_EXTERNAL_HOSTNAME automatically
# -------------------------------------------------------------------
RENDER_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'komunityweb.onrender.com')

ALLOWED_HOSTS = [
    RENDER_HOSTNAME,
    'komunityweb.onrender.com',
    '127.0.0.1',
    'localhost',
]

CSRF_TRUSTED_ORIGINS = [
    f'https://{RENDER_HOSTNAME}',
    'https://komunityweb.onrender.com',
]

# -------------------------------------------------------------------
# Middleware — add WhiteNoise right after SecurityMiddleware
# -------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # serves static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django_browser_reload is intentionally excluded in production
]

# -------------------------------------------------------------------
# Static files — WhiteNoise compressed storage
# -------------------------------------------------------------------
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# -------------------------------------------------------------------
# Database — Render provides DATABASE_URL automatically
# -------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        env='DATABASE_URL',
        conn_max_age=600,
    )
}

# -------------------------------------------------------------------
# Email — use real SMTP in production
# -------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'manyadzatocky@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')  # Set manually in Render dashboard

# -------------------------------------------------------------------
# CORS — restrict in production to known origins
# -------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    f'https://{RENDER_HOSTNAME}',
]

# -------------------------------------------------------------------
# Security hardening
# -------------------------------------------------------------------
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
