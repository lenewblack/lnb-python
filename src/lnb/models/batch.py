from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from lnb.models._base import LnbBaseModel

T = TypeVar("T", bound=LnbBaseModel)


class BatchError(LnbBaseModel):
    """Describes a single failed item in a batch operation."""

    index: int = 0
    message: str = ""
    errors: Optional[Dict[str, Any]] = None


class BatchResult(Generic[T]):
    """Result of a batch create/update operation.

    Contains successfully processed items and per-item errors for failures.
    """

    def __init__(self, items: List[T], errors: List[BatchError]) -> None:
        self.items = items
        self.errors = errors

    @classmethod
    def from_raw(cls, model: Type[T], raw: Dict[str, Any]) -> "BatchResult[T]":
        body = raw.get("_body") if "_body" in raw else raw
        if not body:
            body = {}
        data = body.get("data", [])
        items = [model.model_validate(i.get("result") or i) for i in data if i.get("success")]
        errors_raw = [i for i in data if not i.get("success")]
        errors = [
            BatchError.model_validate({
                "index": idx,
                "message": str(i.get("errors", "")),
                "errors": i.get("errors"),
            })
            for idx, i in enumerate(errors_raw)
        ]
        return cls(items=items, errors=errors)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __repr__(self) -> str:
        return (
            f"BatchResult(items={len(self.items)}, errors={len(self.errors)})"
        )
