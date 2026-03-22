from __future__ import annotations

from typing import Optional
from unittest.mock import MagicMock

import pytest

from lnb._pagination import ResultSet, paginate
from lnb.models._base import LnbBaseModel
from lnb.models.pagination import PaginationMeta


class Item(LnbBaseModel):
    id: int
    name: str = ""


def make_meta(
    current_page: int = 1,
    total_pages: int = 1,
    has_more: bool = False,
    total_items: int = 1,
    page_size: int = 20,
) -> PaginationMeta:
    return PaginationMeta.model_validate({
        "currentPage": current_page,
        "pageSize": page_size,
        "totalItems": total_items,
        "totalPages": total_pages,
        "hasMore": has_more,
    })


class TestResultSet:
    def test_iterable(self) -> None:
        items = [Item(id=1), Item(id=2)]
        rs = ResultSet(items=items, meta=make_meta())
        assert list(rs) == items

    def test_len(self) -> None:
        rs = ResultSet(items=[Item(id=1), Item(id=2)], meta=make_meta())
        assert len(rs) == 2

    def test_from_raw_data_key(self) -> None:
        raw = {
            "data": [{"id": 1}, {"id": 2}],
            "currentPage": 1,
            "pageSize": 2,
            "totalItems": 2,
            "totalPages": 1,
            "hasMore": False,
        }
        rs = ResultSet.from_raw(Item, raw)
        assert len(rs) == 2
        assert rs.items[0].id == 1

    def test_from_raw_items_key(self) -> None:
        raw = {
            "items": [{"id": 3}],
            "currentPage": 1,
            "pageSize": 1,
            "totalItems": 1,
            "totalPages": 1,
            "hasMore": False,
        }
        rs = ResultSet.from_raw(Item, raw)
        assert rs.items[0].id == 3

    def test_from_raw_empty(self) -> None:
        raw = {
            "data": [],
            "currentPage": 1,
            "pageSize": 20,
            "totalItems": 0,
            "totalPages": 0,
            "hasMore": False,
        }
        rs = ResultSet.from_raw(Item, raw)
        assert len(rs) == 0

    def test_from_raw_ignores_unknown_fields(self) -> None:
        raw = {
            "data": [{"id": 1, "unknownField": "ignored"}],
            "currentPage": 1,
            "pageSize": 1,
            "totalItems": 1,
            "totalPages": 1,
            "hasMore": False,
        }
        rs = ResultSet.from_raw(Item, raw)
        assert not hasattr(rs.items[0], "unknownField")


class TestPaginate:
    def test_single_page(self) -> None:
        page1 = ResultSet(
            items=[Item(id=1), Item(id=2)],
            meta=make_meta(current_page=1, total_pages=1, has_more=False, total_items=2),
        )
        list_fn = MagicMock(return_value=page1)

        items = list(paginate(list_fn))
        assert len(items) == 2
        assert list_fn.call_count == 1

    def test_multiple_pages(self) -> None:
        page1 = ResultSet(
            items=[Item(id=1)],
            meta=make_meta(current_page=1, total_pages=2, has_more=True, total_items=2),
        )
        page2 = ResultSet(
            items=[Item(id=2)],
            meta=make_meta(current_page=2, total_pages=2, has_more=False, total_items=2),
        )
        list_fn = MagicMock(side_effect=[page1, page2])

        items = list(paginate(list_fn))
        assert len(items) == 2
        assert items[0].id == 1
        assert items[1].id == 2
        assert list_fn.call_count == 2

    def test_passes_filters(self) -> None:
        page = ResultSet(items=[], meta=make_meta())
        list_fn = MagicMock(return_value=page)

        list(paginate(list_fn, filters={"status": "active"}))

        called_params = list_fn.call_args[0][0]
        assert called_params["status"] == "active"
        assert called_params["page"] == 1

    def test_injects_page_number(self) -> None:
        page1 = ResultSet(
            items=[Item(id=1)],
            meta=make_meta(has_more=True, total_pages=3),
        )
        page2 = ResultSet(
            items=[Item(id=2)],
            meta=make_meta(current_page=2, has_more=False, total_pages=3),
        )
        list_fn = MagicMock(side_effect=[page1, page2])

        list(paginate(list_fn))

        first_call_params = list_fn.call_args_list[0][0][0]
        second_call_params = list_fn.call_args_list[1][0][0]
        assert first_call_params["page"] == 1
        assert second_call_params["page"] == 2
