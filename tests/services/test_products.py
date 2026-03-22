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


class TestProductList:
    @respx.mock
    def test_returns_result_set(self, client: LnbClient) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(
                200,
                json=make_list_response([PRODUCT_LIST_ITEM], total_items=1),
            )
        )
        result = client.products.list()
        assert isinstance(result, ResultSet)
        assert len(result) == 1
        assert isinstance(result.items[0], ProductListItem)
        assert result.items[0].model == "SHIRT-001"

    @respx.mock
    def test_passes_filters_as_query_params(self, client: LnbClient) -> None:
        route = respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(
                200, json=make_list_response([])
            )
        )
        client.products.list({"collection": "SS24"})
        assert route.calls[0].request.url.params["collection"] == "SS24"

    @respx.mock
    def test_paginate_yields_all_items(self, client: LnbClient) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            side_effect=[
                httpx.Response(
                    200,
                    json={
                        "data": [PRODUCT_LIST_ITEM],
                        "currentPage": 1, "pageSize": 1, "totalItems": 2,
                        "totalPages": 2, "hasMore": True,
                    },
                ),
                httpx.Response(
                    200,
                    json={
                        "data": [{"model": "SHIRT-002"}],
                        "currentPage": 2, "pageSize": 1, "totalItems": 2,
                        "totalPages": 2, "hasMore": False,
                    },
                ),
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
        with pytest.raises(ValidationError) as exc_info:
            client.products.upsert({})
        assert exc_info.value.errors == {"model": ["required"]}


class TestProductBatchUpsert:
    @respx.mock
    def test_returns_batch_result(self, client: LnbClient) -> None:
        respx.post(f"{BASE_URL}/products/batch").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [PRODUCT_DETAIL],
                    "errors": [],
                },
            )
        )
        result = client.products.batch_upsert([{"model": "SHIRT-001"}])
        assert isinstance(result, BatchResult)
        assert len(result.items) == 1
        assert not result.has_errors

    @respx.mock
    def test_reports_partial_errors(self, client: LnbClient) -> None:
        respx.post(f"{BASE_URL}/products/batch").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [PRODUCT_DETAIL],
                    "errors": [{"index": 1, "message": "Invalid model"}],
                },
            )
        )
        result = client.products.batch_upsert([
            {"model": "SHIRT-001"},
            {"model": ""},
        ])
        assert result.has_errors
        assert result.errors[0].index == 1
