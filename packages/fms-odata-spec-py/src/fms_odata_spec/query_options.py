"""Query option types and literal-formatting helpers for the FileMaker OData API.

Mirrors ``src/query-options.ts`` from ``@fms-odata/spec-ts``.

@see docs/03-query-options.md
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Generic, List, Literal, Optional, TypeVar, Union

__all__ = [
    "QueryOption",
    "UnsupportedQueryOption",
    "FilterComparisonOp",
    "FilterLogicalOp",
    "FilterStringFunction",
    "FilterDateTimeFunction",
    "FilterNumericFunction",
    "FilterFunction",
    "UnsupportedFilterFunction",
    "SortDirection",
    "OrderByClause",
    "AggregateFunction",
    "AggregateExpression",
    "GroupByExpression",
    "ApplyTransformation",
    "QueryParams",
    "ODataCollection",
    "ODataEntity",
    "QueryResult",
    "escape_string_literal",
    "format_literal",
]

#: Supported system query options.
QueryOption = Literal[
    "$filter", "$select", "$orderby", "$top", "$skip",
    "$expand", "$count", "$apply", "$search", "$compute",
]

#: Query options not supported by FileMaker.
UnsupportedQueryOption = Literal["$search", "$compute"]

#: Supported $filter comparison operators.
FilterComparisonOp = Literal["eq", "ne", "gt", "ge", "lt", "le"]

#: Supported $filter logical operators.
FilterLogicalOp = Literal["and", "or", "not"]

#: Supported $filter string functions.
FilterStringFunction = Literal[
    "startswith", "endswith", "contains", "length", "tolower", "toupper",
    "trim", "substring", "indexof", "concat",
]

#: Supported $filter date/time functions.
FilterDateTimeFunction = Literal[
    "year", "month", "day", "hour", "minute", "second", "date", "time",
]

#: Supported $filter numeric functions.
FilterNumericFunction = Literal["round", "floor", "ceiling"]

#: All supported $filter built-in functions.
FilterFunction = Union[FilterStringFunction, FilterDateTimeFunction, FilterNumericFunction]

#: Explicitly unsupported $filter functions.
UnsupportedFilterFunction = Literal[
    "fractionalseconds", "isof", "geo.distance", "geo.length",
    "geo.intersects", "any", "all",
]

#: Sort direction for $orderby.
SortDirection = Literal["asc", "desc"]

#: $apply aggregate function.
AggregateFunction = Literal["sum", "min", "max", "average", "countdistinct"]

T = TypeVar("T")


@dataclass
class OrderByClause:
    """$orderby clause."""

    field: str
    direction: Optional[SortDirection] = None


@dataclass
class AggregateExpression:
    """$apply aggregate expression."""

    field: str
    function: AggregateFunction
    alias: str
    #: Optional offset added to the field value before aggregation.
    add: Optional[int] = None


@dataclass
class GroupByExpression:
    """$apply groupby expression."""

    fields: List[str]
    aggregate: Optional[List[AggregateExpression]] = None


@dataclass
class AggregateTransformation:
    """$apply aggregate transformation."""

    type: Literal["aggregate"]
    expressions: List[AggregateExpression]


@dataclass
class GroupByTransformation:
    """$apply groupby transformation."""

    type: Literal["groupby"]
    expression: GroupByExpression


#: $apply transformation (either aggregate-only or groupby with optional aggregate),
#: discriminated by the ``type`` Literal field.
ApplyTransformation = Union[AggregateTransformation, GroupByTransformation]


@dataclass
class QueryParams:
    """Query parameters for a record query."""

    filter: Optional[str] = None
    select: Optional[List[str]] = None
    orderby: Optional[List[OrderByClause]] = None
    top: Optional[int] = None
    skip: Optional[int] = None
    expand: Optional[Union[str, List[str]]] = None
    count: Optional[bool] = None
    apply: Optional[str] = None


@dataclass
class ODataCollection(Generic[T]):
    """Standard OData response envelope for a collection."""

    odata_context: str
    value: List[T]
    odata_count: Optional[int] = None
    odata_next_link: Optional[str] = None


@dataclass
class ODataEntity(Generic[T]):
    """Standard OData response envelope for a single entity.

    The TS type is ``{ '@odata.context': string; '@odata.etag'?: string } & T``
    (an intersection). Python has no intersection type, so the entity payload
    is carried in the :attr:`entity` field of type ``T``. Callers access entity
    fields via ``envelope.entity.<field>``.
    """

    odata_context: str
    entity: T
    odata_etag: Optional[str] = None


@dataclass
class QueryResult(Generic[T]):
    """Query result (simplified)."""

    value: List[T]
    count: Optional[int] = None
    next_link: Optional[str] = None


def escape_string_literal(s: str) -> str:
    """Escape single quotes in OData string literals.

    OData requires ``'O''Brien'`` (doubled quotes) for names containing
    apostrophes.
    """
    return s.replace("'", "''")


def format_literal(value: Union[str, int, float, bool, datetime]) -> str:
    """Format a primitive value as an OData literal for use in $filter.

    Strings are single-quoted with escaped internal quotes. Numbers and
    booleans are raw. Datetimes are ISO-8601 with microseconds stripped
    (matching the TS ``Date.toISOString()`` behaviour with millis removed).
    """
    if isinstance(value, bool):
        # bool is a subclass of int; check first.
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return f"'{escape_string_literal(value)}'"
    if isinstance(value, datetime):
        iso = value.isoformat()
        # Strip microseconds: "...xxx" -> drop the fractional seconds part.
        # isoformat() yields e.g. "2026-06-30T12:34:56.789000+00:00" or
        # "2026-06-30T12:34:56.789000" (naive) or with 'Z' replaced below.
        if "." in iso:
            head, _rest = iso.split(".", 1)
            # Reattach timezone suffix if present in the original.
            # The fractional part is everything after '.'; the tz suffix is the
            # trailing '+'/'-'/'Z' portion of that.
            frac_and_tz = _rest
            tz = ""
            for sep in ("+", "-", "Z"):
                idx = frac_and_tz.find(sep)
                if idx != -1:
                    tz = frac_and_tz[idx:]
                    break
            iso = head + tz
        # Replace trailing +00:00 with Z for parity with TS toISOString().
        if iso.endswith("+00:00"):
            iso = iso[:-6] + "Z"
        return iso
    return str(value)
