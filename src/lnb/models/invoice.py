from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class InvoiceLine(LnbBaseModel):
    description: Optional[str] = None
    quantity: int = 0
    unit_price: Optional[float] = Field(None, alias="unitPrice")
    total: Optional[float] = None


class InvoiceListItem(LnbBaseModel):
    id: str = ""
    reference: Optional[str] = None
    retailer_id: Optional[str] = Field(None, alias="retailerId")
    total: Optional[float] = None
    currency: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")


class Invoice(LnbBaseModel):
    id: str = ""
    reference: Optional[str] = None
    retailer_id: Optional[str] = Field(None, alias="retailerId")
    retailer_name: Optional[str] = Field(None, alias="retailerName")
    lines: List[InvoiceLine] = Field(default_factory=list)
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
