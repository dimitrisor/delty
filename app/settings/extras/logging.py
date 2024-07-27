LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "logfmt": {"()": "logfmt.formatter.Formatter"},
        "debug": {
            "format": "{asctime} {levelname} {name}.{funcName}: {message}",
            "style": "{",
        },
    },
    "filters": {
        "gunicorn_filter": {
            "()": "logfmt.filters.GunicornFilter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "logfmt",
        },
        "console_gunicorn": {
            "class": "logging.StreamHandler",
            "formatter": "logfmt",
            "filters": ["gunicorn_filter"],
        },
        "console_debug": {
            "class": "logging.StreamHandler",
            "formatter": "debug",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        },
        "gunicorn": {
            "handlers": ["console_gunicorn"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "propagate": False,
            "level": "INFO",
        },
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console_debug"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
