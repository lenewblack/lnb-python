from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class SelectionListItem(LnbBaseModel):
    id: str = ""
    name: Optional[str] = None
    retailer_id: Optional[str] = Field(None, alias="retailerId")
    updated_at: Optional[str] = Field(None, alias="updatedAt")


class Selection(LnbBaseModel):
    id: str = ""
    name: Optional[str] = None
    retailer_id: Optional[str] = Field(None, alias="retailerId")
    retailer_name: Optional[str] = Field(None, alias="retailerName")
    models: List[str] = Field(default_factory=list)
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
