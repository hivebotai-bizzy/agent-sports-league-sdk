"""Custom exceptions for the ASL SDK."""


class ASLException(Exception):
    """Base exception for all ASL SDK errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(ASLException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, status_code=401)


class RateLimitError(ASLException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int | None = None) -> None:
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class ValidationError(ASLException):
    """Raised when request validation fails."""

    def __init__(self, message: str, field: str | None = None) -> None:
        super().__init__(message, status_code=400)
        self.field = field


class NotFoundError(ASLException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404)


class APIError(ASLException):
    """Raised when the API returns an unexpected error."""

    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message, status_code=status_code)
