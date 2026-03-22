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
        items = [model.model_validate(i) for i in raw.get("items", [])]
        errors = [BatchError.model_validate(e) for e in raw.get("errors", [])]
        return cls(items=items, errors=errors)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __repr__(self) -> str:
        return (
            f"BatchResult(items={len(self.items)}, errors={len(self.errors)})"
        )
