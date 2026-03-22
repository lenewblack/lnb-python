from __future__ import annotations

from typing import Any, Dict, Generator, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.order import Order, OrderListItem, OrderStatusUpdate
from lnb.services._base import BaseService


class OrderService(BaseService):
    _PATH = "orders"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[OrderListItem]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(OrderListItem, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[OrderListItem, None, None]:
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        reference: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Order:
        raw = self._request("GET", f"{self._PATH}/{reference}", options=options)
        return self._parse(Order, raw)

    def upsert(
        self,
        payload: Dict[str, Any],
        *,
        options: Optional[RequestOptions] = None,
    ) -> Order:
        raw = self._request("POST", self._PATH, json=payload, options=options)
        return self._parse(Order, raw)

    def update_status(
        self,
        reference: str,
        status: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> OrderStatusUpdate:
        raw = self._request(
            "PUT",
            f"{self._PATH}/{reference}/status",
            json={"status": status},
            options=options,
        )
        return self._parse(OrderStatusUpdate, raw)

    def archive(
        self,
        reference: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Order:
        raw = self._request(
            "PUT",
            f"{self._PATH}/{reference}/archive",
            options=options,
        )
        return self._parse(Order, raw)
