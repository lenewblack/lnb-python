from __future__ import annotations

from typing import Any, Dict, Generator, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.selection import Selection, SelectionListItem
from lnb.services._base import BaseService


class SelectionService(BaseService):
    _PATH = "selections"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[SelectionListItem]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(SelectionListItem, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[SelectionListItem, None, None]:
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        selection_id: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Selection:
        raw = self._request("GET", f"{self._PATH}/{selection_id}", options=options)
        return self._parse(Selection, raw)

    def upsert(
        self,
        payload: Dict[str, Any],
        *,
        options: Optional[RequestOptions] = None,
    ) -> Selection:
        raw = self._request("POST", self._PATH, json=payload, options=options)
        return self._parse(Selection, raw)
