from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from lnb._auth import TokenManager
from lnb._exceptions import (
    AuthenticationError,
    LnbApiError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from lnb._retry import RetryStrategy
from lnb._types import RequestOptions


class HttpTransport:
    """Low-level HTTP client wrapping httpx with retry logic and error mapping."""

    def __init__(
        self,
        base_url: str,
        token_manager: TokenManager,
        timeout: float,
        max_retries: int,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._token_manager = token_manager
        self._retry = RetryStrategy(max_retries=max_retries)
        self._client = http_client or httpx.Client(timeout=timeout)
        self._owns_client = http_client is None

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Any] = None,
        options: Optional[RequestOptions] = None,
    ) -> Any:
        """Execute an authenticated HTTP request with retry logic.

        Returns the decoded JSON body, or None for empty responses.
        Raises an LnbApiError subclass on non-2xx responses.
        """
        url = f"{self._base_url}/{path.lstrip('/')}"
        opts = options or {}
        last_exc: Optional[Exception] = None

        for attempt in self._retry.attempts():
            token = self._token_manager.get_token()
            headers: Dict[str, str] = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                **opts.get("extra_headers", {}),
            }
            timeout = opts.get("timeout", None)

            try:
                response = self._client.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    data=data,
                    files=files,
                    headers=headers,
                    timeout=timeout,
                )
            except httpx.RequestError as exc:
                last_exc = exc
                if attempt.is_last:
                    raise LnbApiError(f"Network error: {exc}") from exc
                attempt.wait_before_network_retry()
                continue

            if response.is_success:
                if not response.content:
                    return None
                return response.json()

            retry_after = response.headers.get("Retry-After")
            if attempt.should_retry(response.status_code, retry_after):
                continue

            self._raise_for_status(response)

        # Should be unreachable, but satisfies the type checker
        raise LnbApiError("Retry loop exhausted without result")

    def _raise_for_status(self, response: httpx.Response) -> None:
        status = response.status_code
        try:
            body: Dict[str, Any] = response.json()
        except Exception:
            body = {}

        message: str = body.get("message", f"HTTP {status}")

        if status == 401:
            raise AuthenticationError(message)
        if status == 404:
            raise NotFoundError(message)
        if status == 422:
            raise ValidationError(message, errors=body.get("errors"))
        if status == 429:
            raise RateLimitError(message)
        raise LnbApiError(message, status_code=status, body=body)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()
