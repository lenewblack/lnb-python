from __future__ import annotations

from typing import Any, Dict, Generator, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.sizing import Sizing, SizingListItem
from lnb.services._base import BaseService


class SizingService(BaseService):
    _PATH = "sizings"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[SizingListItem]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(SizingListItem, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[SizingListItem, None, None]:
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        sizing_id: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Sizing:
        raw = self._request("GET", f"{self._PATH}/{sizing_id}", options=options)
        return self._parse(Sizing, raw)
