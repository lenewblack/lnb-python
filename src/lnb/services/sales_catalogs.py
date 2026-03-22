from __future__ import annotations

from typing import Any, Dict, Generator, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.sales_catalog import SalesCatalog, SalesCatalogListItem
from lnb.services._base import BaseService


class SalesCatalogService(BaseService):
    _PATH = "sales-catalogs"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[SalesCatalogListItem]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(SalesCatalogListItem, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[SalesCatalogListItem, None, None]:
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        catalog_id: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> SalesCatalog:
        raw = self._request("GET", f"{self._PATH}/{catalog_id}", options=options)
        return self._parse(SalesCatalog, raw)
