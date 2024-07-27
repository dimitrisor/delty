import datetime
import logging
import numbers
from typing import Any
from typing import Dict

# Default log record keys
SKIP_RECORD_KEYS = list(vars(logging.makeLogRecord({})))
# Additional keys, eg from django.server
SKIP_RECORD_KEYS += [
    "request",
    "server_time",
]


class Formatter(logging.Formatter):
    """
    Format log records according to the logfmt format.

    https://www.brandur.org/logfmt
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        params = {
            "timestamp": datetime.datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname.lower(),
            "name": record.name,
            "message": record.getMessage(),
            "path": record.pathname,
            "line_number": record.lineno,
        }

        if record.exc_info:
            # The builtin implementation is caching the exc info
            # for the next handlers, do the same.
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

            params["exc_text"] = record.exc_text

        params.update(self.get_extras(record))
        return " ".join(
            f"{key}={self.format_value(value)}" for key, value in params.items()
        )

    @classmethod
    def get_extras(cls, record: logging.LogRecord) -> Dict[str, Any]:
        """
        Return a dictionary of logger extra attributes, not in the SKIP_RECORD_KEYS.

        Example:
            log.error("foobar", user_id=1234) -> {user_id: 1234}
        """
        return {
            cls.normalize_key(key): value
            for key, value in record.__dict__.items()
            if key not in SKIP_RECORD_KEYS
        }

    @classmethod
    def normalize_key(cls, key: str) -> str:
        """Make sure no monkeys around."""
        return key.replace(" ", "_") if key else "_"

    @classmethod
    def format_string(cls, value: str) -> str:
        """Process the provided string with any necessary quoting and/or escaping."""
        needs_dquote_escaping = '"' in value
        needs_newline_escaping = "\n" in value
        needs_quoting = " " in value or "=" in value

        if needs_dquote_escaping:
            value = value.replace('"', '\\"')

        if needs_newline_escaping:
            value = value.replace("\n", "\\n")

        if needs_quoting:
            value = f'"{value}"'  # noqa: B028 -> logfmt needs the double quotes

        return value or '""'

    @classmethod
    def format_value(cls, value: Any) -> str:
        """Map the provided value to the proper logfmt formatted string."""
        if value is None:
            return ""

        if isinstance(value, bool):
            return "true" if value else "false"

        if isinstance(value, numbers.Number):
            return str(value)

        return cls.format_string(str(value))
