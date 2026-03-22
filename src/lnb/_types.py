from __future__ import annotations

from typing import Dict, Optional

from typing_extensions import NotRequired, TypedDict


class RequestOptions(TypedDict, total=False):
    """Per-request overrides that can be passed to any service method."""

    timeout: NotRequired[Optional[float]]
    extra_headers: NotRequired[Dict[str, str]]
