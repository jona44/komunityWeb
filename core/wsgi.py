import os
from django.core.wsgi import get_wsgi_application

# If DJANGO_SETTINGS_MODULE is already set (e.g. by Render env vars), respect it.
# Otherwise, auto-detect production by checking environment keys Render always injects.
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    is_production = any(
        key in os.environ
        for key in ('RENDER', 'RENDER_EXTERNAL_HOSTNAME', 'WEBSITE_HOSTNAME', 'DJANGO_ENV')
    )
    os.environ['DJANGO_SETTINGS_MODULE'] = 'core.deployment' if is_production else 'core.settings'

application = get_wsgi_application()
