from __future__ import annotations

from typing import Any, Dict, Generator, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.retailer import Retailer, RetailerListItem
from lnb.services._base import BaseService


class RetailerService(BaseService):
    _PATH = "retailers"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[RetailerListItem]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(RetailerListItem, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[RetailerListItem, None, None]:
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        retailer_id: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Retailer:
        raw = self._request("GET", f"{self._PATH}/{retailer_id}", options=options)
        return self._parse(Retailer, raw)

    def upsert(
        self,
        payload: Dict[str, Any],
        *,
        options: Optional[RequestOptions] = None,
    ) -> Retailer:
        raw = self._request("POST", self._PATH, json=payload, options=options)
        return self._parse(Retailer, raw)
