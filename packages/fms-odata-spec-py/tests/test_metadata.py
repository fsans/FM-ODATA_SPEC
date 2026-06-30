"""Tests for fms_odata_spec.metadata."""

from __future__ import annotations

import pytest

from fms_odata_spec.metadata import (
    SYSTEM_FIELDS,
    SYSTEM_TABLES,
    EdmAction,
    EdmEntitySet,
    EdmEntityType,
    EdmEnumMember,
    EdmEnumType,
    EdmProperty,
    FMServerVersion,
    FMAnnotations,
    ODataMetadata,
    extract_major_version,
    extract_major_version_from_metadata,
    parse_server_version,
    parse_version_string,
)


def test_system_fields() -> None:
    assert SYSTEM_FIELDS.ROWID == "ROWID"
    assert SYSTEM_FIELDS.ROWMODID == "ROWMODID"


def test_system_tables() -> None:
    assert SYSTEM_TABLES.TABLES == "FileMaker_Tables"
    assert SYSTEM_TABLES.FIELDS == "FileMaker_Fields"
    assert SYSTEM_TABLES.INDEXES == "FileMaker_Indexes"


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("21.1.2.500", FMServerVersion(21, 1, 2, "21.1.2.500")),
        ("26.0.1", FMServerVersion(26, 0, 1, "26.0.1")),
        ("  19.2.1  ", FMServerVersion(19, 2, 1, "19.2.1")),
        ("nope", None),
        ("", None),
    ],
)
def test_parse_version_string(raw: str, expected: object) -> None:
    assert parse_version_string(raw) == expected


def test_parse_server_version_strategy_1a() -> None:
    xml = '<Annotation Term="Org.OData.Core.V1.ProductVersion" String="26.0.1.500"/>'
    v = parse_server_version(xml)
    assert v is not None
    assert v.major == 26
    assert v.minor == 0
    assert v.patch == 1


def test_parse_server_version_strategy_1b_reversed_attrs() -> None:
    xml = '<Annotation String="21.1.2" Term="Org.OData.Core.V1.ProductVersion"/>'
    v = parse_server_version(xml)
    assert v is not None
    assert v.major == 21


def test_parse_server_version_strategy_1c_server_version() -> None:
    xml = '<Annotation Term="ServerVersion" String="OData Engine 26.0.1"/>'
    v = parse_server_version(xml)
    assert v is not None
    assert v.major == 26


def test_parse_server_version_strategy_1d_reversed() -> None:
    xml = '<Annotation String="OData Engine 26.0.1" Term="ServerVersion"/>'
    v = parse_server_version(xml)
    assert v is not None
    assert v.major == 26


def test_parse_server_version_strategy_2_generic_fallback() -> None:
    xml = '<Annotation Term="MyVersion" String="anything 22.3.1 here"/>'
    v = parse_server_version(xml)
    assert v is not None
    assert v.major == 22


def test_parse_server_version_ignores_odata_4_0() -> None:
    # The generic fallback must not match OData spec "4.0" (major < 17).
    xml = '<Annotation Term="Org.OData.Core.V1.Version" String="4.0"/>'
    assert parse_server_version(xml) is None


def test_parse_server_version_empty_or_none() -> None:
    assert parse_server_version("") is None
    assert parse_server_version(None) is None  # type: ignore[arg-type]


def test_parse_server_version_no_match() -> None:
    assert parse_server_version("<foo>bar</foo>") is None


def test_extract_major_version() -> None:
    assert extract_major_version("26.0.1.500") == "26"
    assert extract_major_version(None) is None
    assert extract_major_version("nope") is None


def test_extract_major_version_from_metadata() -> None:
    xml = '<Annotation Term="Org.OData.Core.V1.ProductVersion" String="22.1.0"/>'
    assert extract_major_version_from_metadata(xml) == "22"
    assert extract_major_version_from_metadata("<foo/>") is None


def test_edm_property_constructs() -> None:
    p = EdmProperty(name="id", type="Edm.Int32", is_key=True)
    assert p.name == "id"
    assert p.is_key is True
    assert p.nullable is None


def test_edm_entity_type_constructs() -> None:
    t = EdmEntityType(name="Customer", keys=["id"], properties=[])
    assert t.keys == ["id"]
    assert t.properties == []


def test_edm_entity_set_constructs() -> None:
    s = EdmEntitySet(name="Customers", entity_type="NS.Customer")
    assert s.entity_type == "NS.Customer"


def test_edm_action_constructs() -> None:
    a = EdmAction(name="MyScript", is_bound=False)
    assert a.is_bound is False
    assert a.script_id is None


def test_edm_enum_type_constructs() -> None:
    e = EdmEnumType(
        name="Status",
        members=[EdmEnumMember(name="open", value=1), EdmEnumMember(name="closed", value="2")],
    )
    assert len(e.members) == 2
    assert e.members[0].value == 1


def test_fm_annotations_constructs() -> None:
    a = FMAnnotations(product_version="26.0.1")
    assert a.product_version == "26.0.1"
    assert a.global_ is None
    assert a.auto_generated is None


def test_odata_metadata_constructs() -> None:
    m = ODataMetadata(
        namespace="NS",
        entity_types=[],
        entity_sets=[],
        actions=[],
        enum_types=[],
        raw="<xml/>",
    )
    assert m.namespace == "NS"
    assert m.raw == "<xml/>"
    assert m.product_version is None
