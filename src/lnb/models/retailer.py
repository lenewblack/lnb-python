from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class RetailerListItem(LnbBaseModel):
    id: str = ""
    name: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    updated_at: Optional[str] = Field(None, alias="updatedAt")


class Retailer(LnbBaseModel):
    id: str = ""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
