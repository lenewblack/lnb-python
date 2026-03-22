from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class ProductVariant(LnbBaseModel):
    fabric_code: str = Field(alias="fabricCode", default="")
    fabric_name: Optional[str] = Field(None, alias="fabricName")
    color_name: Optional[str] = Field(None, alias="colorName")
    ean13: Optional[str] = None
    sku: Optional[str] = None
    alternatives: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
    extra: Optional[Dict[str, Any]] = None


class ProductSize(LnbBaseModel):
    size: str = ""
    label: Optional[str] = None
    sort_order: int = Field(0, alias="sortOrder")


class ProductListItem(LnbBaseModel):
    """Lightweight product representation returned in list responses."""

    model: str = ""
    name: Optional[str] = None
    collection: Optional[str] = None
    brand: Optional[str] = None
    updated_at: Optional[str] = Field(None, alias="updatedAt")
    created_at: Optional[str] = Field(None, alias="createdAt")


class Product(LnbBaseModel):
    """Full product representation returned by get/upsert endpoints."""

    model: str = ""
    name: Optional[str] = None
    description: Optional[str] = None
    collection: Optional[str] = None
    brand: Optional[str] = None
    gender: Optional[str] = None
    fabric_composition: Optional[str] = Field(None, alias="fabricComposition")
    care_instructions: Optional[str] = Field(None, alias="careInstructions")
    variants: List[ProductVariant] = Field(default_factory=list)
    sizes: List[ProductSize] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
