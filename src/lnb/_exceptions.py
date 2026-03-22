from __future__ import annotations

from typing import Any, Dict, Optional


class LnbError(Exception):
    """Base exception for all lnb SDK errors."""


class LnbApiError(LnbError):
    """HTTP error returned by the Le New Black API."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class AuthenticationError(LnbApiError):
    """401 - Invalid or expired credentials."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=401)


class NotFoundError(LnbApiError):
    """404 - Resource does not exist."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=404)


class ValidationError(LnbApiError):
    """422 - Request payload failed server-side validation."""

    def __init__(
        self,
        message: str,
        errors: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, status_code=422)
        self.errors = errors


class RateLimitError(LnbApiError):
    """429 - Too many requests."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=429)


class ConfigurationError(LnbError):
    """Raised for invalid SDK configuration (missing credentials, bad options, etc.)."""
