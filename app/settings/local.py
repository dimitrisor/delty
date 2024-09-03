from app import env
from app.settings.base import *  # noqa

DEBUG = env.get_bool("DEBUG", default=True)
ENVIRONMENT = "local"
