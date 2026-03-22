from __future__ import annotations

from typing import Any, Dict, Generator, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.fabric import Fabric, FabricListItem
from lnb.services._base import BaseService


class FabricService(BaseService):
    _PATH = "fabrics"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[FabricListItem]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(FabricListItem, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[FabricListItem, None, None]:
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        code: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Fabric:
        raw = self._request("GET", f"{self._PATH}/{code}", options=options)
        return self._parse(Fabric, raw)
