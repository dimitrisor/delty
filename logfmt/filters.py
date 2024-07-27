import logging
import re
from typing import Any
from typing import Dict


class GunicornFilter(logging.Filter):
    def __init__(self):
        super().__init__()

    def filter(self, record: logging.LogRecord) -> bool:
        """Extracts data from the log message and adds it to the log record."""
        log_message = record.getMessage()

        if not log_message:
            return True

        if parsed_data := self._parse_log_message(log_message):
            record.msg = "Completed"
            parsed_data.pop("timestamp", None)
            for key, value in parsed_data.items():
                record.__dict__[key] = value

        return True

    def _parse_log_message(self, log_message: str) -> Dict[Any, Any]:
        """Parses the log message and returns a dictionary of the parsed data."""
        regex_pattern = (
            r'(?P<remote_addr>\S+) - - \[(?P<timestamp>.*?)\] "(?P<method>\S+) (?P<path>.*?) HTTP/\d\.\d" '  # noqa
            r'(?P<status_code>\d+) (?P<response_size>\d+) "(?P<referrer>.*?)" '
            r'"(?P<user_agent>.*?)"'
        )

        if match := re.match(regex_pattern, log_message):
            return match.groupdict()

        return {}
