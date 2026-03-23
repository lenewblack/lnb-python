from __future__ import annotations

from typing import Any, Dict, Optional
from unittest.mock import MagicMock

import pytest

from lnb._pagination import ResultSet, paginate
from lnb.models._base import LnbBaseModel
from lnb.models.pagination import PaginationMeta


class Item(LnbBaseModel):
    id: int
    name: str = ""


def make_raw(
    items: list,
    current_page: int = 1,
    total_pages: int = 1,
    has_more: bool = False,
    total_items: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build a raw transport response in the {_body, _headers} format the API uses."""
    n = len(items)
    return {
        "_body": items,
        "_headers": {
            "X-Pagination-Current-Page": str(current_page),
            "X-Pagination-Page-Size": str(page_size if page_size is not None else n),
            "X-Pagination-Total-Items": str(total_items if total_items is not None else n),
            "X-Pagination-Total-Pages": str(total_pages),
            "X-Pagination-Has-More": str(has_more).lower(),
        },
    }


class TestResultSet:
    def test_iterable(self) -> None:
        raw = make_raw([{"id": 1}, {"id": 2}])
        rs = ResultSet.from_raw(Item, raw)
        assert [i.id for i in rs] == [1, 2]

    def test_len(self) -> None:
        raw = make_raw([{"id": 1}, {"id": 2}])
        rs = ResultSet.from_raw(Item, raw)
        assert len(rs) == 2

    def test_from_raw_reads_body_list(self) -> None:
        raw = make_raw([{"id": 1}, {"id": 2}])
        rs = ResultSet.from_raw(Item, raw)
        assert len(rs) == 2
        assert rs.items[0].id == 1

    def test_from_raw_empty(self) -> None:
        raw = make_raw([])
        rs = ResultSet.from_raw(Item, raw)
        assert len(rs) == 0

    def test_from_raw_ignores_unknown_fields(self) -> None:
        raw = make_raw([{"id": 1, "unknownField": "ignored"}])
        rs = ResultSet.from_raw(Item, raw)
        assert not hasattr(rs.items[0], "unknownField")

    def test_pagination_meta_from_headers(self) -> None:
        raw = make_raw(
            [{"id": 1}],
            current_page=3,
            total_pages=10,
            has_more=True,
            total_items=200,
            page_size=20,
        )
        rs = ResultSet.from_raw(Item, raw)
        assert rs.meta.current_page == 3
        assert rs.meta.total_pages == 10
        assert rs.meta.has_more is True
        assert rs.meta.total_items == 200

    def test_has_more_false_stops_pagination(self) -> None:
        raw = make_raw([{"id": 1}], has_more=False)
        rs = ResultSet.from_raw(Item, raw)
        assert rs.meta.has_more is False


class TestPaginate:
    def test_single_page(self) -> None:
        raw1 = make_raw([{"id": 1}, {"id": 2}], has_more=False)
        list_fn = MagicMock(return_value=ResultSet.from_raw(Item, raw1))

        items = list(paginate(list_fn))
        assert len(items) == 2
        assert list_fn.call_count == 1

    def test_multiple_pages(self) -> None:
        raw1 = make_raw([{"id": 1}], current_page=1, total_pages=2, has_more=True)
        raw2 = make_raw([{"id": 2}], current_page=2, total_pages=2, has_more=False)
        list_fn = MagicMock(side_effect=[
            ResultSet.from_raw(Item, raw1),
            ResultSet.from_raw(Item, raw2),
        ])

        items = list(paginate(list_fn))
        assert len(items) == 2
        assert items[0].id == 1
        assert items[1].id == 2
        assert list_fn.call_count == 2

    def test_passes_filters(self) -> None:
        raw = make_raw([])
        list_fn = MagicMock(return_value=ResultSet.from_raw(Item, raw))

        list(paginate(list_fn, filters={"status": "active"}))

        called_params = list_fn.call_args[0][0]
        assert called_params["status"] == "active"
        assert called_params["page"] == 1

    def test_injects_page_number(self) -> None:
        raw1 = make_raw([{"id": 1}], has_more=True, total_pages=2)
        raw2 = make_raw([{"id": 2}], has_more=False, total_pages=2)
        list_fn = MagicMock(side_effect=[
            ResultSet.from_raw(Item, raw1),
            ResultSet.from_raw(Item, raw2),
        ])

        list(paginate(list_fn))

        assert list_fn.call_args_list[0][0][0]["page"] == 1
        assert list_fn.call_args_list[1][0][0]["page"] == 2
