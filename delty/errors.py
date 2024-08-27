from delty.exceptions import ServiceException


class ValidationException(ServiceException):
    """Validation Exception."""

    default_status_code = 422
    default_title = "Validation Failed"


class NotFoundException(ServiceException):
    """Not Found Exception."""

    default_status_code = 404
    default_title = "Not Found"


class WebPageUnreachable(ValidationException):
    default_detail = "Failed to reach the desired page."
    default_code = 6006


class CssSelectorHtmlElementNotFound(ValidationException):
    default_detail = "No HTML element found for that css selector."
    default_code = 6006


class CrawlingJobAlreadyExists(ValidationException):
    default_detail = "Crawling job already exists."
    default_code = 6007


class S3ContentStoringFailed(ValidationException):
    default_detail = "Failed to store element content to S3."
    default_code = 6008
