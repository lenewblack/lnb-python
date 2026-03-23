from __future__ import annotations

from typing import Optional

from lnb.models._base import LnbBaseModel


class ApiVersion(LnbBaseModel):
    """API version information returned by the /version endpoint."""

    version: str = ""
    release_date: Optional[str] = None
