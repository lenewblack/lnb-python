from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest
import respx

from lnb._auth import TokenManager
from lnb._exceptions import (
    AuthenticationError,
    LnbApiError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from lnb._http import HttpTransport

BASE_URL = "https://www.lenewblack.com/apis/wholesale/v2"


def make_transport(max_retries: int = 0) -> HttpTransport:
    """Create a transport with a pre-seeded token manager (no real HTTP auth)."""
    tm = MagicMock(spec=TokenManager)
    tm.get_token.return_value = "mock-token"
    return HttpTransport(
        base_url=BASE_URL,
        token_manager=tm,
        timeout=5.0,
        max_retries=max_retries,
    )


class TestHttpTransportSuccess:
    @respx.mock
    def test_get_returns_json(self) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(200, json={"data": []})
        )
        transport = make_transport()
        result = transport.request("GET", "/products")
        assert result == {"data": []}

    @respx.mock
    def test_post_with_json_body(self) -> None:
        route = respx.post(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(200, json={"model": "A001"})
        )
        transport = make_transport()
        result = transport.request("POST", "/products", json={"model": "A001"})
        assert result == {"model": "A001"}

    @respx.mock
    def test_empty_response_returns_none(self) -> None:
        respx.delete(f"{BASE_URL}/products/X").mock(
            return_value=httpx.Response(204)
        )
        transport = make_transport()
        result = transport.request("DELETE", "/products/X")
        assert result is None

    @respx.mock
    def test_bearer_token_sent(self) -> None:
        route = respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(200, json={})
        )
        transport = make_transport()
        transport.request("GET", "/products")
        assert route.calls[0].request.headers["Authorization"] == "Bearer mock-token"

    @respx.mock
    def test_extra_headers_forwarded(self) -> None:
        route = respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(200, json={})
        )
        transport = make_transport()
        transport.request("GET", "/products", options={"extra_headers": {"X-Foo": "bar"}})
        assert route.calls[0].request.headers["X-Foo"] == "bar"


class TestHttpTransportErrors:
    @respx.mock
    def test_401_raises_auth_error(self) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(401, json={"message": "Unauthorized"})
        )
        transport = make_transport()
        with pytest.raises(AuthenticationError):
            transport.request("GET", "/products")

    @respx.mock
    def test_404_raises_not_found(self) -> None:
        respx.get(f"{BASE_URL}/products/X").mock(
            return_value=httpx.Response(404, json={"message": "Not found"})
        )
        transport = make_transport()
        with pytest.raises(NotFoundError):
            transport.request("GET", "/products/X")

    @respx.mock
    def test_422_raises_validation_error(self) -> None:
        respx.post(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(
                422, json={"message": "Validation failed", "errors": {"model": ["required"]}}
            )
        )
        transport = make_transport()
        with pytest.raises(ValidationError) as exc_info:
            transport.request("POST", "/products", json={})
        assert exc_info.value.errors == {"model": ["required"]}

    @respx.mock
    def test_429_raises_rate_limit_error(self) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(429, json={"message": "Too many requests"})
        )
        transport = make_transport()
        with pytest.raises(RateLimitError):
            transport.request("GET", "/products")

    @respx.mock
    def test_500_raises_api_error(self) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(500, json={"message": "Internal error"})
        )
        transport = make_transport()
        with pytest.raises(LnbApiError) as exc_info:
            transport.request("GET", "/products")
        assert exc_info.value.status_code == 500


class TestHttpTransportRetry:
    @respx.mock
    def test_retries_on_503_then_succeeds(self) -> None:
        route = respx.get(f"{BASE_URL}/products")
        route.side_effect = [
            httpx.Response(503),
            httpx.Response(200, json={"data": []}),
        ]
        transport = make_transport(max_retries=2)
        with patch("time.sleep"):  # skip real sleep
            result = transport.request("GET", "/products")
        assert result == {"data": []}
        assert route.call_count == 2

    @respx.mock
    def test_raises_after_max_retries(self) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(503, json={"message": "unavailable"})
        )
        transport = make_transport(max_retries=2)
        with patch("time.sleep"):
            with pytest.raises(LnbApiError):
                transport.request("GET", "/products")

    @respx.mock
    def test_does_not_retry_on_404(self) -> None:
        route = respx.get(f"{BASE_URL}/products/X").mock(
            return_value=httpx.Response(404, json={"message": "not found"})
        )
        transport = make_transport(max_retries=3)
        with pytest.raises(NotFoundError):
            transport.request("GET", "/products/X")
        assert route.call_count == 1

    @respx.mock
    def test_retries_on_network_error(self) -> None:
        route = respx.get(f"{BASE_URL}/products")
        route.side_effect = [
            httpx.ConnectError("refused"),
            httpx.Response(200, json={"data": []}),
        ]
        transport = make_transport(max_retries=2)
        with patch("time.sleep"):
            result = transport.request("GET", "/products")
        assert result == {"data": []}
