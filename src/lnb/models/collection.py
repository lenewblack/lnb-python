from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class CollectionListItem(LnbBaseModel):
    code: str = ""
    name: Optional[str] = None
    year: Optional[int] = None
    season: Optional[str] = None
    updated_at: Optional[str] = Field(None, alias="updatedAt")


class Collection(LnbBaseModel):
    code: str = ""
    name: Optional[str] = None
    year: Optional[int] = None
    season: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
