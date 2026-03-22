from __future__ import annotations

import time
from unittest.mock import patch

import httpx
import pytest
import respx

from lnb._auth import REFRESH_BUFFER_SECONDS, TokenManager
from lnb._exceptions import AuthenticationError

BASE_URL = "https://www.lenewblack.com/apis/wholesale/v2"
TOKEN_URL = f"{BASE_URL}/auth/token"

GOOD_TOKEN_RESPONSE = {
    "access_token": "test-access-token",
    "token_type": "Bearer",
    "expires_in": 3600,
}


class TestTokenManagerFetch:
    @respx.mock
    def test_fetches_token_on_first_call(self) -> None:
        respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=GOOD_TOKEN_RESPONSE)
        )
        tm = TokenManager("cid", "csecret", BASE_URL)
        assert tm.get_token() == "test-access-token"

    @respx.mock
    def test_reuses_cached_token(self) -> None:
        route = respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=GOOD_TOKEN_RESPONSE)
        )
        tm = TokenManager("cid", "csecret", BASE_URL)
        tm.get_token()
        tm.get_token()
        assert route.call_count == 1

    @respx.mock
    def test_refreshes_when_token_expired(self) -> None:
        route = respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=GOOD_TOKEN_RESPONSE)
        )
        tm = TokenManager("cid", "csecret", BASE_URL)
        tm.get_token()

        # Force expiry
        assert tm._token is not None
        tm._token.expires_at = time.monotonic() - 1

        tm.get_token()
        assert route.call_count == 2

    @respx.mock
    def test_refreshes_within_buffer(self) -> None:
        route = respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=GOOD_TOKEN_RESPONSE)
        )
        tm = TokenManager("cid", "csecret", BASE_URL)
        tm.get_token()

        # Set expiry to be within the buffer window
        assert tm._token is not None
        tm._token.expires_at = time.monotonic() + REFRESH_BUFFER_SECONDS - 1

        tm.get_token()
        assert route.call_count == 2


class TestTokenManagerErrors:
    @respx.mock
    def test_raises_auth_error_on_401(self) -> None:
        respx.post(TOKEN_URL).mock(return_value=httpx.Response(401))
        tm = TokenManager("bad", "creds", BASE_URL)
        with pytest.raises(AuthenticationError):
            tm.get_token()

    @respx.mock
    def test_raises_auth_error_on_500(self) -> None:
        respx.post(TOKEN_URL).mock(return_value=httpx.Response(500))
        tm = TokenManager("cid", "csecret", BASE_URL)
        with pytest.raises(AuthenticationError):
            tm.get_token()

    @respx.mock
    def test_raises_auth_error_on_network_failure(self) -> None:
        respx.post(TOKEN_URL).mock(side_effect=httpx.ConnectError("refused"))
        tm = TokenManager("cid", "csecret", BASE_URL)
        with pytest.raises(AuthenticationError):
            tm.get_token()
