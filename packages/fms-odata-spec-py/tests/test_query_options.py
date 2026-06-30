"""Tests for fms_odata_spec.query_options."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from fms_odata_spec.query_options import (
    AggregateExpression,
    AggregateTransformation,
    GroupByExpression,
    GroupByTransformation,
    ODataCollection,
    ODataEntity,
    OrderByClause,
    QueryParams,
    QueryResult,
    escape_string_literal,
    format_literal,
)


def test_escape_string_literal_doubles_quotes() -> None:
    assert escape_string_literal("O'Brien") == "O''Brien"
    assert escape_string_literal("plain") == "plain"
    assert escape_string_literal("a'b'c") == "a''b''c"


@pytest.mark.parametrize(
    "value,expected",
    [
        ("hello", "'hello'"),
        ("O'Brien", "'O''Brien'"),
        (42, "42"),
        (3.14, "3.14"),
        (True, "true"),
        (False, "false"),
    ],
)
def test_format_literal_primitives(value: object, expected: str) -> None:
    assert format_literal(value) == expected  # type: ignore[arg-type]


def test_format_literal_datetime_aware_strips_microseconds() -> None:
    dt = datetime(2026, 6, 30, 12, 34, 56, 789000, tzinfo=timezone.utc)
    assert format_literal(dt) == "2026-06-30T12:34:56Z"


def test_format_literal_datetime_naive() -> None:
    dt = datetime(2026, 6, 30, 12, 34, 56, 789000)
    assert format_literal(dt) == "2026-06-30T12:34:56"


def test_format_literal_datetime_no_micros() -> None:
    dt = datetime(2026, 6, 30, 12, 34, 56, tzinfo=timezone.utc)
    assert format_literal(dt) == "2026-06-30T12:34:56Z"


def test_orderby_clause_defaults() -> None:
    c = OrderByClause(field="name")
    assert c.field == "name"
    assert c.direction is None


def test_orderby_clause_with_direction() -> None:
    c = OrderByClause(field="name", direction="desc")
    assert c.direction == "desc"


def test_aggregate_expression_constructs() -> None:
    a = AggregateExpression(field="price", function="sum", alias="total")
    assert a.field == "price"
    assert a.function == "sum"
    assert a.alias == "total"
    assert a.add is None


def test_groupby_expression_constructs() -> None:
    g = GroupByExpression(fields=["region"], aggregate=None)
    assert g.fields == ["region"]
    assert g.aggregate is None


def test_aggregate_transformation_discriminator() -> None:
    t: AggregateTransformation = AggregateTransformation(
        type="aggregate",
        expressions=[AggregateExpression(field="x", function="min", alias="mn")],
    )
    assert t.type == "aggregate"
    assert len(t.expressions) == 1


def test_groupby_transformation_discriminator() -> None:
    t: GroupByTransformation = GroupByTransformation(
        type="groupby",
        expression=GroupByExpression(fields=["a"]),
    )
    assert t.type == "groupby"
    assert t.expression.fields == ["a"]


def test_query_params_defaults_all_none() -> None:
    p = QueryParams()
    assert p.filter is None
    assert p.select is None
    assert p.orderby is None
    assert p.top is None
    assert p.skip is None
    assert p.expand is None
    assert p.count is None
    assert p.apply is None


def test_query_params_with_values() -> None:
    p = QueryParams(
        filter="name eq 'x'",
        select=["a", "b"],
        top=10,
        skip=5,
        expand=["rel"],
        count=True,
    )
    assert p.filter == "name eq 'x'"
    assert p.select == ["a", "b"]
    assert p.top == 10
    assert p.expand == ["rel"]
    assert p.count is True


def test_odata_collection_constructs() -> None:
    c = ODataCollection[int](odata_context="ctx", value=[1, 2, 3], odata_count=3)
    assert c.value == [1, 2, 3]
    assert c.odata_count == 3
    assert c.odata_next_link is None


def test_odata_entity_wraps_t() -> None:
    payload = {"id": 1, "name": "x"}
    e = ODataEntity[dict](odata_context="ctx", entity=payload, odata_etag="etag")
    assert e.entity == payload
    assert e.odata_etag == "etag"
    assert e.entity["id"] == 1


def test_query_result_constructs() -> None:
    r = QueryResult[int](value=[1, 2], count=2, next_link="link")
    assert r.value == [1, 2]
    assert r.count == 2
    assert r.next_link == "link"


def test_format_literal_datetime_negative_tz_with_micros() -> None:
    dt = datetime(2026, 6, 30, 12, 34, 56, 789000, tzinfo=timezone(timedelta(hours=-5)))
    assert format_literal(dt) == "2026-06-30T12:34:56-05:00"


def test_format_literal_datetime_negative_tz_no_micros() -> None:
    dt = datetime(2026, 6, 30, 12, 34, 56, tzinfo=timezone(timedelta(hours=-5)))
    assert format_literal(dt) == "2026-06-30T12:34:56-05:00"
