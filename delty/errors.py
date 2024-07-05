from delty.exceptions import ServiceException


class ValidationException(ServiceException):
    """Validation Exception."""

    default_status_code = 422
    default_title = "Validation Failed"


class NotFoundException(ServiceException):
    """Not Found Exception."""

    default_status_code = 404
    default_title = "Not Found"


# class ValidationException(ServiceException):
#     """Validation Exception."""
#
#     default_status_code = 422
#     default_title = "Validation Failed"


class WebPageUnreachable(ValidationException):
    default_detail = "Failed to reach the desired page."
    default_code = 6006
