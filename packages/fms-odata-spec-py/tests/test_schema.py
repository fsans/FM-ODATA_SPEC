"""Tests for fms_odata_spec.schema."""

from __future__ import annotations

import pytest

from fms_odata_spec.schema import (
    FIELD_DEFAULTS,
    FIELD_TYPES,
    AddFieldsParams,
    CreateTableParams,
    FMFieldDefinition,
    ParsedFieldType,
    parse_field_type,
)


def test_field_types_complete() -> None:
    assert "VARCHAR" in FIELD_TYPES
    assert "BINARY VARYING" in FIELD_TYPES
    assert len(FIELD_TYPES) == 12


def test_field_defaults_complete() -> None:
    assert "CURRENT_TIMESTAMP" in FIELD_DEFAULTS
    assert "USER" in FIELD_DEFAULTS


def test_field_definition_defaults() -> None:
    f = FMFieldDefinition(name="id", type="INT")
    assert f.primary is False
    assert f.unique is False
    assert f.nullable is True
    assert f.global_ is False
    assert f.default is None


def test_field_definition_to_odata_dict_uses_global_key() -> None:
    f = FMFieldDefinition(name="g", type="INT", global_=True, default="USER")
    d = f.to_odata_dict()
    assert d["global"] is True  # not "global_"
    assert d["default"] == "USER"
    assert "externalSecurePath" not in d  # not present


def test_field_definition_to_odata_dict_with_external_path() -> None:
    f = FMFieldDefinition(
        name="pic", type="BLOB", external_secure_path="secure/storage"
    )
    d = f.to_odata_dict()
    assert d["externalSecurePath"] == "secure/storage"


def test_create_table_params_to_odata_dict() -> None:
    p = CreateTableParams(
        table_name="T",
        fields=[FMFieldDefinition(name="id", type="INT", primary=True)],
    )
    d = p.to_odata_dict()
    assert d["tableName"] == "T"
    assert d["fields"][0]["name"] == "id"
    assert d["fields"][0]["primary"] is True


def test_add_fields_params_to_odata_dict() -> None:
    p = AddFieldsParams(table_name="T", fields=[])
    assert p.to_odata_dict() == {"tableName": "T", "fields": []}


@pytest.mark.parametrize(
    "type_str,expected",
    [
        ("VARCHAR(200)", ParsedFieldType(base_type="VARCHAR", length=200)),
        ("INT[4]", ParsedFieldType(base_type="INT", repetitions=4)),
        ("VARCHAR(200)[4]", ParsedFieldType(base_type="VARCHAR", length=200, repetitions=4)),
        ("BLOB", ParsedFieldType(base_type="BLOB")),
    ],
)
def test_parse_field_type(type_str: str, expected: ParsedFieldType) -> None:
    assert parse_field_type(type_str) == expected
