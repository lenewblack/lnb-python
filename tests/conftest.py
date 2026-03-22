from __future__ import annotations

from typing import Any, Dict
from unittest.mock import MagicMock

import httpx
import pytest
import respx

from lnb._auth import TokenManager
from lnb._http import HttpTransport
from lnb.client import LnbClient

BASE_URL = "https://www.lenewblack.com/apis/wholesale/v2"
TOKEN_URL = f"{BASE_URL}/auth/token"

TOKEN_RESPONSE: Dict[str, Any] = {
    "access_token": "test-token",
    "token_type": "Bearer",
    "expires_in": 3600,
}


def make_meta(
    current_page: int = 1,
    total_pages: int = 1,
    has_more: bool = False,
    total_items: int = 0,
    page_size: int = 20,
) -> Dict[str, Any]:
    return {
        "currentPage": current_page,
        "pageSize": page_size,
        "totalItems": total_items,
        "totalPages": total_pages,
        "hasMore": has_more,
    }


def make_list_response(
    data: list,
    **meta_kwargs: Any,
) -> Dict[str, Any]:
    return {"data": data, **make_meta(**meta_kwargs)}


@pytest.fixture
def mock_transport() -> HttpTransport:
    """HttpTransport with a pre-seeded token (no network auth call)."""
    tm = MagicMock(spec=TokenManager)
    tm.get_token.return_value = "test-token"
    return HttpTransport(
        base_url=BASE_URL,
        token_manager=tm,
        timeout=5.0,
        max_retries=0,
    )


@pytest.fixture
def client(mock_transport: HttpTransport) -> LnbClient:
    """LnbClient pre-wired with a mock transport."""
    c = LnbClient.__new__(LnbClient)
    c._transport = mock_transport
    c._token_manager = MagicMock()
    c._products = None
    c._orders = None
    c._inventory = None
    c._prices = None
    c._collections = None
    c._fabrics = None
    c._retailers = None
    c._files = None
    c._sales_documents = None
    c._sales_catalogs = None
    c._selections = None
    c._sizings = None
    c._invoices = None
    return c
