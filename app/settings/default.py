from app import env
from app.settings.base import *  # noqa

DEBUG = False

SECRET_KEY = env.get_str("SECRET_KEY")

ALLOWED_HOSTS = env.get_list("ALLOWED_HOSTS", default=[])

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGIN_REGEXES = env.get_list("CORS_ALLOWED_ORIGIN_REGEXES", default=[])

LOG_LEVEL = env.get_str("LOG_LEVEL", default="INFO")

EXPOSE_COMMANDS_OVER_HTTP = False
