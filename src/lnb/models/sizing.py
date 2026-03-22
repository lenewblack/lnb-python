from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class SizeEntry(LnbBaseModel):
    size: str = ""
    label: Optional[str] = None
    sort_order: int = Field(0, alias="sortOrder")


class SizingListItem(LnbBaseModel):
    id: str = ""
    name: Optional[str] = None
    updated_at: Optional[str] = Field(None, alias="updatedAt")


class Sizing(LnbBaseModel):
    id: str = ""
    name: Optional[str] = None
    sizes: List[SizeEntry] = Field(default_factory=list)
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
