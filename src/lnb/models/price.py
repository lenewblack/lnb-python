from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class PriceLine(LnbBaseModel):
    model: str = ""
    fabric_code: Optional[str] = Field(None, alias="fabricCode")
    size: Optional[str] = None
    wholesale_price: Optional[float] = Field(None, alias="wholesalePrice")
    retail_price: Optional[float] = Field(None, alias="retailPrice")
    currency: Optional[str] = None


class Price(LnbBaseModel):
    model: str = ""
    lines: List[PriceLine] = Field(default_factory=list)
    currency: Optional[str] = None
    updated_at: Optional[str] = Field(None, alias="updatedAt")


class PriceListItem(LnbBaseModel):
    model: str = ""
    currency: Optional[str] = None
    updated_at: Optional[str] = Field(None, alias="updatedAt")
