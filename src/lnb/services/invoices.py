from __future__ import annotations

from typing import Any, Dict, Generator, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.invoice import Invoice, InvoiceListItem
from lnb.services._base import BaseService


class InvoiceService(BaseService):
    _PATH = "invoices"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[InvoiceListItem]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(InvoiceListItem, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[InvoiceListItem, None, None]:
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        invoice_id: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Invoice:
        raw = self._request("GET", f"{self._PATH}/{invoice_id}", options=options)
        return self._parse(Invoice, raw)
