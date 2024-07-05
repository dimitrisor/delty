from typing import Any


class ServiceException(Exception):
    """Base Exception class."""

    default_status_code = 503
    default_code = 9999
    default_title = "Unknown Error"
    default_detail = "Something went wrong."

    def __init__(
        self,
        status_code: int | None = None,
        code: int | None = None,
        title: str | None = None,
        detail: str | None = None,
        **meta: Any,  # noqa: ANN401
    ):
        """Exception class constructor.

        Args:
            status_code: The HTTP status code.
            code: The error code.
            title: The error title.
            detail: The error details description.
            **meta: Additional metadata.
        """
        if status_code is None:
            status_code = self.default_status_code

        if code is None:
            code = self.default_code

        if title is None:
            title = self.default_title

        if detail is None:
            detail = self.default_detail

        self.status_code = status_code
        self.code = code
        self.title = title
        self.detail = detail
        self.meta = meta

    def as_dict(self) -> dict[str, Any]:
        """Return the exception arguments as a dictionary."""
        return {
            "status_code": self.status_code,
            "code": self.code,
            "title": self.title,
            "detail": self.detail,
            "meta": self.meta,
        }

    def __repr__(self) -> str:
        """Exception representation str."""
        params = [
            f"status_code={self.status_code!r}",
            f"code={self.code!r}",
            f"title={self.title!r}",
            f"detail={self.detail!r}",
        ]
        params.extend(f"{key}={value!r}" for key, value in self.meta.items())
        return f"{self.__class__.__name__}({', '.join(params)})"

    def __str__(self) -> str:
        """Return the exception representation str."""
        return repr(self)
