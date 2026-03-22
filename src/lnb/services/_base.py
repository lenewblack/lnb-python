from __future__ import annotations

from typing import Any, Dict, List, Optional, Type, TypeVar

from lnb._http import HttpTransport
from lnb._types import RequestOptions
from lnb.models._base import LnbBaseModel

M = TypeVar("M", bound=LnbBaseModel)


class BaseService:
    """Base class for all resource services."""

    def __init__(self, transport: HttpTransport) -> None:
        self._transport = transport

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Any] = None,
        options: Optional[RequestOptions] = None,
    ) -> Any:
        return self._transport.request(
            method,
            path,
            params=params,
            json=json,
            data=data,
            files=files,
            options=options,
        )

    def _parse(self, model: Type[M], data: Any) -> M:
        return model.model_validate(data)

    def _parse_list(self, model: Type[M], data: List[Any]) -> List[M]:
        return [model.model_validate(item) for item in data]
