from __future__ import annotations

from typing import Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class FabricListItem(LnbBaseModel):
    code: str = ""
    name: Optional[str] = None
    updated_at: Optional[str] = Field(None, alias="updatedAt")


class Fabric(LnbBaseModel):
    code: str = ""
    name: Optional[str] = None
    description: Optional[str] = None
    composition: Optional[str] = None
    color_code: Optional[str] = Field(None, alias="colorCode")
    color_name: Optional[str] = Field(None, alias="colorName")
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
