from __future__ import annotations

from pydantic import Field

from lnb.models._base import LnbBaseModel


class PaginationMeta(LnbBaseModel):
    """Pagination metadata returned with list responses."""

    current_page: int = Field(alias="currentPage", default=1)
    page_size: int = Field(alias="pageSize", default=0)
    total_items: int = Field(alias="totalItems", default=0)
    total_pages: int = Field(alias="totalPages", default=1)
    has_more: bool = Field(alias="hasMore", default=False)
