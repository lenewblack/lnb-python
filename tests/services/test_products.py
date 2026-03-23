from __future__ import annotations

import httpx
import pytest
import respx

from lnb._exceptions import NotFoundError, ValidationError
from lnb._pagination import ResultSet
from lnb.client import LnbClient
from lnb.models.batch import BatchResult
from lnb.models.product import Product, ProductListItem, ProductVariant
from tests.conftest import BASE_URL, make_list_response

PRODUCT_DETAIL: dict = {
    "model": "SHIRT-001",
    "name": "Test Shirt",
    "collection": "SS24",
    "variants": [{"fabricCode": "RED", "ean13": "1234567890123"}],
    "sizes": [{"size": "S", "sortOrder": 1}],
    "unknownFutureField": "should be ignored",
}

PRODUCT_LIST_ITEM: dict = {"model": "SHIRT-001", "name": "Test Shirt", "updatedAt": "2024-01-01"}

# Batch API response format: body is {"data": [{success, result|errors}, ...]}
BATCH_SUCCESS_RESPONSE: dict = {
    "data": [{"success": True, "result": PRODUCT_DETAIL}],
}
BATCH_PARTIAL_RESPONSE: dict = {
    "data": [
        {"success": True, "result": PRODUCT_DETAIL},
        {"success": False, "errors": {"model": ["is required"]}},
    ],
}


class TestProductList:
    @respx.mock
    def test_returns_result_set(self, client: LnbClient) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            return_value=make_list_response([PRODUCT_LIST_ITEM], total_items=1)
        )
        result = client.products.list()
        assert isinstance(result, ResultSet)
        assert len(result) == 1
        assert isinstance(result.items[0], ProductListItem)
        assert result.items[0].model == "SHIRT-001"

    @respx.mock
    def test_passes_filters_as_query_params(self, client: LnbClient) -> None:
        route = respx.get(f"{BASE_URL}/products").mock(
            return_value=make_list_response([])
        )
        client.products.list({"collection": "SS24"})
        assert route.calls[0].request.url.params["collection"] == "SS24"

    @respx.mock
    def test_paginate_yields_all_items(self, client: LnbClient) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            side_effect=[
                make_list_response([PRODUCT_LIST_ITEM], current_page=1, total_pages=2, has_more=True),
                make_list_response([{"model": "SHIRT-002"}], current_page=2, total_pages=2),
            ]
        )
        items = list(client.products.paginate())
        assert len(items) == 2
        assert items[0].model == "SHIRT-001"
        assert items[1].model == "SHIRT-002"


class TestProductGet:
    @respx.mock
    def test_returns_product(self, client: LnbClient) -> None:
        respx.get(f"{BASE_URL}/products/SHIRT-001").mock(
            return_value=httpx.Response(200, json=PRODUCT_DETAIL)
        )
        product = client.products.get("SHIRT-001")
        assert isinstance(product, Product)
        assert product.model == "SHIRT-001"
        assert len(product.variants) == 1
        assert product.variants[0].fabric_code == "RED"

    @respx.mock
    def test_ignores_unknown_fields(self, client: LnbClient) -> None:
        respx.get(f"{BASE_URL}/products/SHIRT-001").mock(
            return_value=httpx.Response(200, json=PRODUCT_DETAIL)
        )
        product = client.products.get("SHIRT-001")
        assert not hasattr(product, "unknownFutureField")

    @respx.mock
    def test_raises_not_found(self, client: LnbClient) -> None:
        respx.get(f"{BASE_URL}/products/MISSING").mock(
            return_value=httpx.Response(404, json={"message": "Not found"})
        )
        with pytest.raises(NotFoundError):
            client.products.get("MISSING")


class TestProductGetVariant:
    @respx.mock
    def test_returns_variant(self, client: LnbClient) -> None:
        respx.get(f"{BASE_URL}/products/SHIRT-001/variants/RED").mock(
            return_value=httpx.Response(
                200, json={"fabricCode": "RED", "ean13": "1234567890123"}
            )
        )
        variant = client.products.get_variant("SHIRT-001", "RED")
        assert isinstance(variant, ProductVariant)
        assert variant.fabric_code == "RED"


class TestProductUpsert:
    @respx.mock
    def test_returns_product(self, client: LnbClient) -> None:
        respx.post(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(200, json=PRODUCT_DETAIL)
        )
        product = client.products.upsert({"model": "SHIRT-001", "name": "Test Shirt"})
        assert isinstance(product, Product)
        assert product.model == "SHIRT-001"

    @respx.mock
    def test_raises_validation_error(self, client: LnbClient) -> None:
        respx.post(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(
                422,
                json={"message": "Validation failed", "errors": {"model": ["required"]}},
            )
        )
        with pytest.raises(ValidationError):
            client.products.upsert({})


class TestProductBatchUpsert:
    @respx.mock
    def test_returns_batch_result(self, client: LnbClient) -> None:
        respx.post(f"{BASE_URL}/multi/products").mock(
            return_value=httpx.Response(200, json=BATCH_SUCCESS_RESPONSE)
        )
        result = client.products.batch_upsert([{"model": "SHIRT-001"}])
        assert isinstance(result, BatchResult)
        assert len(result.items) == 1
        assert not result.has_errors

    @respx.mock
    def test_reports_partial_errors(self, client: LnbClient) -> None:
        respx.post(f"{BASE_URL}/multi/products").mock(
            return_value=httpx.Response(200, json=BATCH_PARTIAL_RESPONSE)
        )
        result = client.products.batch_upsert([
            {"model": "SHIRT-001"},
            {"model": ""},
        ])
        assert len(result.items) == 1
        assert result.has_errors
        assert len(result.errors) == 1
