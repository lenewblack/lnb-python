from __future__ import annotations

from typing import Optional

from pydantic import Field

from lnb.models._base import LnbBaseModel


class FileObject(LnbBaseModel):
    id: str = ""
    filename: Optional[str] = None
    mime_type: Optional[str] = Field(None, alias="mimeType")
    size: Optional[int] = None
    url: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
