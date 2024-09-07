"""
WSGI config for delty project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

import app.env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.default")

application = get_wsgi_application()

# Add default credentials for the dramatiq dashboard only for the local environment
if settings.ENVIRONMENT == "local":
    os.environ.setdefault("DRAMATIQ_WSGI_AUTH_CREDENTIALS", "admin:admin")

if app.env.get_str("DRAMATIQ_WSGI_AUTH_CREDENTIALS"):
    import dramatiq_dashboard
    from wsgi_basic_auth import BasicAuth

    dashboard_middleware = dramatiq_dashboard.make_wsgi_middleware("/dramatiq")
    application = dashboard_middleware(application)
    application = BasicAuth(
        application,
        realm="dramatiq",
        include_paths=["/dramatiq"],
        env_prefix="DRAMATIQ_",
    )
