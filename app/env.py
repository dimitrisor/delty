import json
import os


def get_bool(name: str, default: bool = False) -> bool:
    """Get a boolean value from environment variable.

    If the environment variable is not set or value is not one or "true"
    or "false", the default value is returned instead.
    """
    if name not in os.environ:
        return default
    if os.environ[name].lower() in ["true", "yes", "1"]:
        return True
    elif os.environ[name].lower() in ["false", "no", "0"]:
        return False
    else:
        return default


def get_str(name: str, default: str | None = None) -> str | None:
    """Get a string value from environment variable.

    If the environment variable is not set, the default value is
    returned instead.
    """
    return os.environ.get(name, default)


def get_int(name: str, default: int | None = None) -> int | None:
    """Get an integer value from environment variable.

    If the environment variable is not set, or if it is not an integer,
    the default value is returned instead.
    """
    try:
        res = os.environ.get(name, default)
        if res is not None:
            return int(res)
    except (ValueError, TypeError):
        pass

    return default


def get_json(name: str) -> dict:
    """Get a json value from environment variable.

    If the environment variable is not set, return an empty dict.
    """
    if raw_json := get_str(name, default=None):
        return json.loads(raw_json)
    return {}


def get_list(name: str, separator: str = ",", default: list | None = None) -> list:
    """Get a list of string values from environment variable.

    If the environment variable is not set, the default value is
    returned instead.
    """
    if default is None:
        default = []

    if name not in os.environ:
        return default

    return list(filter(None, map(str.strip, os.environ[name].split(separator))))
