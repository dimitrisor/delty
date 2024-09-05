import dj_database_url

ENVIRONMENT = "test"
from app.settings.base import *  # noqa

DEBUG = False
STATICFILES_STORAGE = ""
DATABASES = {
    "default": dj_database_url.config(
        default="postgres://delty_user:delty_pass@localhost:5432/delty",
        conn_max_age=600,
    )
}

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.stub.StubBroker",
    "OPTIONS": {},
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Pipelines",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "django_dramatiq.middleware.AdminMiddleware",
    ],
}

DELTY_FILE_STORAGE = "delty.tests.utils.TempFileSystemStorage"
