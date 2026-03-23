from __future__ import annotations

from typing import Any, Callable, Dict, Generator, Generic, Iterator, List, Optional, Type, TypeVar

from lnb.models._base import LnbBaseModel
from lnb.models.pagination import PaginationMeta

T = TypeVar("T", bound=LnbBaseModel)


class ResultSet(Generic[T]):
    """A single page of API results with pagination metadata.

    Iterable and supports len(). Access metadata via .meta.
    """

    def __init__(self, items: List[T], meta: PaginationMeta) -> None:
        self.items = items
        self.meta = meta

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __repr__(self) -> str:
        return (
            f"ResultSet(count={len(self.items)}, "
            f"page={self.meta.current_page}/{self.meta.total_pages})"
        )

    @classmethod
    def from_raw(cls, model: Type[T], raw: Dict[str, Any]) -> "ResultSet[T]":
        """Deserialize a raw API response dict into a typed ResultSet.

        The API returns a plain JSON array as the body with pagination
        metadata in response headers (X-Pagination-*).
        """
        body = raw.get("_body") or []
        headers = raw.get("_headers", {})

        items = [model.model_validate(i) for i in (body if isinstance(body, list) else [])]

        def _int(key: str, default: int) -> int:
            val = headers.get(key) or headers.get(key.lower())
            try:
                return int(val) if val is not None else default
            except (ValueError, TypeError):
                return default

        def _bool(key: str, default: bool) -> bool:
            val = headers.get(key) or headers.get(key.lower())
            if val is None:
                return default
            return str(val).lower() == "true"

        meta = PaginationMeta.model_validate({
            "currentPage": _int("X-Pagination-Current-Page", 1),
            "pageSize": _int("X-Pagination-Page-Size", len(items)),
            "totalItems": _int("X-Pagination-Total-Items", len(items)),
            "totalPages": _int("X-Pagination-Total-Pages", 1),
            "hasMore": _bool("X-Pagination-Has-More", False),
        })
        return cls(items=items, meta=meta)


def paginate(
    list_fn: Callable[..., ResultSet[T]],
    filters: Optional[Dict[str, Any]] = None,
    *,
    options: Optional[Any] = None,
) -> Generator[T, None, None]:
    """Auto-paginating generator that yields individual items across all pages.

    Injects ``page=N`` into *filters* on each call and stops when
    ``meta.has_more`` is False.

    Example::

        for product in paginate(client.products.list):
            print(product.model)
    """
    params: Dict[str, Any] = dict(filters or {})
    page = 1

    while True:
        result = list_fn({**params, "page": page}, options=options)

        yield from result.items

        if not result.meta.has_more:
            break
        page += 1
