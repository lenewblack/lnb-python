from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LnbBaseModel(BaseModel):
    """Base class for all Le New Black API response models.

    - extra="ignore": silently discard unknown API fields so new API fields
      don't break existing code.
    - populate_by_name=True: allow both alias (camelCase) and Python name
      (snake_case) when constructing models.
    """

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        str_strip_whitespace=True,
    )
