from __future__ import annotations

from typing import Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class InventoryItem(LnbBaseModel):
    model: Optional[str] = None
    fabric_code: Optional[str] = Field(None, alias="fabricCode")
    size: Optional[str] = None
    ean13: Optional[str] = None
    sku: Optional[str] = None
    quantity: int = 0
    updated_at: Optional[str] = Field(None, alias="updatedAt")
