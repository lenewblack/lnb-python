from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class OrderLine(LnbBaseModel):
    model: str = ""
    fabric_code: str = Field("", alias="fabricCode")
    size: str = ""
    quantity: int = 0
    unit_price: Optional[float] = Field(None, alias="unitPrice")
    ean13: Optional[str] = None
    sku: Optional[str] = None


class OrderListItem(LnbBaseModel):
    reference: str = ""
    status: Optional[str] = None
    retailer_id: Optional[str] = Field(None, alias="retailerId")
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")


class Order(LnbBaseModel):
    reference: str = ""
    status: Optional[str] = None
    retailer_id: Optional[str] = Field(None, alias="retailerId")
    retailer_name: Optional[str] = Field(None, alias="retailerName")
    lines: List[OrderLine] = Field(default_factory=list)
    notes: Optional[str] = None
    shipping_address: Optional[Dict[str, Any]] = Field(None, alias="shippingAddress")
    billing_address: Optional[Dict[str, Any]] = Field(None, alias="billingAddress")
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")


class OrderStatusUpdate(LnbBaseModel):
    reference: str = ""
    status: str = ""
    updated_at: Optional[str] = Field(None, alias="updatedAt")
