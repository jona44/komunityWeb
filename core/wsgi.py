import os
from django.core.wsgi import get_wsgi_application

is_production = any(
    key in os.environ
    for key in ('RENDER', 'RENDER_EXTERNAL_HOSTNAME', 'WEBSITE_HOSTNAME')
)
settings_module = 'core.deployment' if is_production else 'core.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module )

application = get_wsgi_application()
