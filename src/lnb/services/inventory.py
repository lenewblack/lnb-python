from __future__ import annotations

from typing import Any, Dict, List, Optional

from lnb._pagination import ResultSet
from lnb._types import RequestOptions
from lnb.models.batch import BatchResult
from lnb.models.inventory import InventoryItem
from lnb.services._base import BaseService


class InventoryService(BaseService):
    _PATH = "inventory"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[InventoryItem]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(InventoryItem, raw)

    # --- Single get ---

    def get_by_data(
        self,
        model: str,
        fabric_code: str,
        size: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> InventoryItem:
        raw = self._request(
            "GET",
            f"{self._PATH}/by-data/{model}/{fabric_code}/{size}",
            options=options,
        )
        return self._parse(InventoryItem, raw)

    def get_by_ean(
        self,
        ean13: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> InventoryItem:
        raw = self._request(
            "GET", f"{self._PATH}/by-ean/{ean13}", options=options
        )
        return self._parse(InventoryItem, raw)

    def get_by_sku(
        self,
        sku: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> InventoryItem:
        raw = self._request(
            "GET", f"{self._PATH}/by-sku/{sku}", options=options
        )
        return self._parse(InventoryItem, raw)

    # --- Single set ---

    def set_by_data(
        self,
        model: str,
        fabric_code: str,
        size: str,
        quantity: int,
        *,
        options: Optional[RequestOptions] = None,
    ) -> InventoryItem:
        raw = self._request(
            "PUT",
            f"{self._PATH}/by-data/{model}/{fabric_code}/{size}",
            json={"quantity": quantity},
            options=options,
        )
        return self._parse(InventoryItem, raw)

    def set_by_ean(
        self,
        ean13: str,
        quantity: int,
        *,
        options: Optional[RequestOptions] = None,
    ) -> InventoryItem:
        raw = self._request(
            "PUT",
            f"{self._PATH}/by-ean/{ean13}",
            json={"quantity": quantity},
            options=options,
        )
        return self._parse(InventoryItem, raw)

    def set_by_sku(
        self,
        sku: str,
        quantity: int,
        *,
        options: Optional[RequestOptions] = None,
    ) -> InventoryItem:
        raw = self._request(
            "PUT",
            f"{self._PATH}/by-sku/{sku}",
            json={"quantity": quantity},
            options=options,
        )
        return self._parse(InventoryItem, raw)

    # --- Batch set ---

    def batch_set_by_data(
        self,
        items: List[Dict[str, Any]],
        *,
        options: Optional[RequestOptions] = None,
    ) -> BatchResult[InventoryItem]:
        raw = self._request(
            "PUT",
            f"{self._PATH}/by-data/batch",
            json={"items": items},
            options=options,
        )
        return BatchResult.from_raw(InventoryItem, raw)

    def batch_set_by_ean(
        self,
        items: List[Dict[str, Any]],
        *,
        options: Optional[RequestOptions] = None,
    ) -> BatchResult[InventoryItem]:
        raw = self._request(
            "PUT",
            f"{self._PATH}/by-ean/batch",
            json={"items": items},
            options=options,
        )
        return BatchResult.from_raw(InventoryItem, raw)

    def batch_set_by_sku(
        self,
        items: List[Dict[str, Any]],
        *,
        options: Optional[RequestOptions] = None,
    ) -> BatchResult[InventoryItem]:
        raw = self._request(
            "PUT",
            f"{self._PATH}/by-sku/batch",
            json={"items": items},
            options=options,
        )
        return BatchResult.from_raw(InventoryItem, raw)
