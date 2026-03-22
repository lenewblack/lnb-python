from __future__ import annotations

from typing import Any, Dict, Generator, List, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.batch import BatchResult
from lnb.models.product import Product, ProductListItem, ProductVariant
from lnb.services._base import BaseService


class ProductService(BaseService):
    _PATH = "products"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[ProductListItem]:
        """Return a single page of products. Use :meth:`paginate` to iterate all."""
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(ProductListItem, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[ProductListItem, None, None]:
        """Yield every product across all pages automatically."""
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        model: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Product:
        """Fetch a single product by its model reference."""
        raw = self._request("GET", f"{self._PATH}/{model}", options=options)
        return self._parse(Product, raw)

    def get_variant(
        self,
        model: str,
        fabric_code: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ProductVariant:
        """Fetch a specific variant (fabric) of a product."""
        raw = self._request(
            "GET",
            f"{self._PATH}/{model}/variants/{fabric_code}",
            options=options,
        )
        return self._parse(ProductVariant, raw)

    def upsert(
        self,
        payload: Dict[str, Any],
        *,
        options: Optional[RequestOptions] = None,
    ) -> Product:
        """Create or update a product."""
        raw = self._request("POST", self._PATH, json=payload, options=options)
        return self._parse(Product, raw)

    def update_variant(
        self,
        model: str,
        fabric_code: str,
        payload: Dict[str, Any],
        *,
        options: Optional[RequestOptions] = None,
    ) -> ProductVariant:
        """Update a specific variant of a product."""
        raw = self._request(
            "PUT",
            f"{self._PATH}/{model}/variants/{fabric_code}",
            json=payload,
            options=options,
        )
        return self._parse(ProductVariant, raw)

    def set_variant_alternatives(
        self,
        model: str,
        fabric_code: str,
        alternatives: List[str],
        *,
        options: Optional[RequestOptions] = None,
    ) -> ProductVariant:
        """Set the alternative variants (colour alternatives) for a variant."""
        raw = self._request(
            "PUT",
            f"{self._PATH}/{model}/variants/{fabric_code}/alternatives",
            json={"alternatives": alternatives},
            options=options,
        )
        return self._parse(ProductVariant, raw)

    def batch_upsert(
        self,
        items: List[Dict[str, Any]],
        *,
        options: Optional[RequestOptions] = None,
    ) -> BatchResult[Product]:
        """Create or update multiple products in a single request."""
        raw = self._request(
            "POST",
            f"{self._PATH}/batch",
            json={"items": items},
            options=options,
        )
        return BatchResult.from_raw(Product, raw)
