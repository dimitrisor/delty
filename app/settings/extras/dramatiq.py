from urllib.parse import urlparse

from app import env

# Redis is used as a broker for dramatiq
REDIS_URL_PARSED = urlparse(env.get_str("REDIS_URL", "redis://localhost:6379/3"))

try:
    # Not very pretty...
    redis_db = int(REDIS_URL_PARSED.path.strip("/"))  # type: ignore
except Exception:
    redis_db = 0


DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "db": redis_db,
        "host": REDIS_URL_PARSED.hostname,
        "port": REDIS_URL_PARSED.port,
        "username": REDIS_URL_PARSED.username,
        "password": REDIS_URL_PARSED.password,
        "ssl": REDIS_URL_PARSED.scheme == "rediss",
        "ssl_cert_reqs": None,
    },
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

# Defines which database should be used to persist Task objects when the
# AdminMiddleware is enabled.  The default value is "default".
DRAMATIQ_TASKS_DATABASE = "default"
