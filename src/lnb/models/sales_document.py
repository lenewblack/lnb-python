from __future__ import annotations

from typing import Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class SalesDocumentListItem(LnbBaseModel):
    id: str = ""
    type: Optional[str] = None
    reference: Optional[str] = None
    retailer_id: Optional[str] = Field(None, alias="retailerId")
    created_at: Optional[str] = Field(None, alias="createdAt")


class SalesDocument(LnbBaseModel):
    id: str = ""
    type: Optional[str] = None
    reference: Optional[str] = None
    retailer_id: Optional[str] = Field(None, alias="retailerId")
    retailer_name: Optional[str] = Field(None, alias="retailerName")
    url: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
