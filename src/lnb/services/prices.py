from __future__ import annotations

from typing import Any, Dict, Generator, List, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.batch import BatchResult
from lnb.models.price import Price, PriceListItem
from lnb.services._base import BaseService


class PriceService(BaseService):
    _PATH = "prices"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[PriceListItem]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(PriceListItem, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[PriceListItem, None, None]:
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        model: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Price:
        raw = self._request("GET", f"{self._PATH}/{model}", options=options)
        return self._parse(Price, raw)

    def upsert(
        self,
        payload: Dict[str, Any],
        *,
        options: Optional[RequestOptions] = None,
    ) -> Price:
        raw = self._request("POST", self._PATH, json=payload, options=options)
        return self._parse(Price, raw)

    def batch_upsert(
        self,
        items: List[Dict[str, Any]],
        *,
        options: Optional[RequestOptions] = None,
    ) -> BatchResult[Price]:
        raw = self._request(
            "POST", f"{self._PATH}/batch", json={"items": items}, options=options
        )
        return BatchResult.from_raw(Price, raw)
