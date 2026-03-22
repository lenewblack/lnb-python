from __future__ import annotations

import threading
import time
from typing import Optional

import httpx

from lnb._exceptions import AuthenticationError

REFRESH_BUFFER_SECONDS = 60


class _TokenResponse:
    __slots__ = ("access_token", "expires_at")

    def __init__(self, access_token: str, expires_in: int) -> None:
        self.access_token = access_token
        self.expires_at = time.monotonic() + expires_in


class TokenManager:
    """Thread-safe OAuth2 client credentials token manager.

    Automatically fetches and refreshes the Bearer token used for all API
    requests. Proactively refreshes 60 seconds before the actual expiry.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str,
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_url = f"{base_url.rstrip('/')}/auth/token"
        self._token: Optional[_TokenResponse] = None
        self._lock = threading.Lock()

    def get_token(self) -> str:
        """Return a valid Bearer token, refreshing if necessary."""
        with self._lock:
            if self._needs_refresh():
                self._refresh()
            assert self._token is not None  # satisfied by _refresh()
            return self._token.access_token

    def _needs_refresh(self) -> bool:
        if self._token is None:
            return True
        return time.monotonic() >= (self._token.expires_at - REFRESH_BUFFER_SECONDS)

    def _refresh(self) -> None:
        try:
            response = httpx.post(
                self._token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                },
                timeout=10.0,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise AuthenticationError(
                f"Token refresh failed with status {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:
            raise AuthenticationError(
                f"Token refresh network error: {exc}"
            ) from exc

        data = response.json()
        self._token = _TokenResponse(
            access_token=data["access_token"],
            expires_in=int(data.get("expires_in", 3600)),
        )
