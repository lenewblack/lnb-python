from __future__ import annotations

from typing import Any, Dict, Generator, Optional

from lnb._pagination import ResultSet, paginate
from lnb._types import RequestOptions
from lnb.models.sales_document import SalesDocument, SalesDocumentListItem
from lnb.services._base import BaseService


class SalesDocumentService(BaseService):
    _PATH = "sales-documents"

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> ResultSet[SalesDocumentListItem]:
        raw = self._request("GET", self._PATH, params=filters, options=options)
        return ResultSet.from_raw(SalesDocumentListItem, raw)

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        *,
        options: Optional[RequestOptions] = None,
    ) -> Generator[SalesDocumentListItem, None, None]:
        yield from paginate(self.list, filters=filters, options=options)

    def get(
        self,
        document_id: str,
        *,
        options: Optional[RequestOptions] = None,
    ) -> SalesDocument:
        raw = self._request("GET", f"{self._PATH}/{document_id}", options=options)
        return self._parse(SalesDocument, raw)
