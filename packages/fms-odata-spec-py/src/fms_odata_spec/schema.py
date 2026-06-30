"""Schema modification (DDL) types for the FileMaker OData API.

Mirrors ``src/schema.ts`` from ``@fms-odata/spec-ts``.

@see docs/10-schema-modification.md
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Literal, Optional

__all__ = [
    "FMFieldType",
    "FMFieldDefault",
    "FMFieldDefinition",
    "CreateTableParams",
    "AddFieldsParams",
    "FIELD_TYPES",
    "FIELD_DEFAULTS",
    "ParsedFieldType",
    "parse_field_type",
]

#: FileMaker field types for table creation.
FMFieldType = Literal[
    "NUMERIC",
    "DECIMAL",
    "INT",
    "DATE",
    "TIME",
    "TIMESTAMP",
    "VARCHAR",
    "CHARACTER VARYING",
    "BLOB",
    "VARBINARY",
    "LONGVARBINARY",
    "BINARY VARYING",
]

#: Default value expressions for fields.
#:
#: The TS type is a union of named literals with ``string`` (so any string is
#: allowed). In Python ``Literal[..., str]`` collapses to ``str`` anyway, so we
#: type this as ``str``; the named defaults are still enumerated in
#: :data:`FIELD_DEFAULTS` for runtime lookup.
FMFieldDefault = str


@dataclass
class FMFieldDefinition:
    """Field definition for table creation or adding fields."""

    #: Field name. Required.
    name: str
    #: Field type. Required. May include length: ``"VARCHAR(200)"`` or repetitions: ``"INT[4]"``.
    type: str
    #: Whether the field is a primary key. Default: ``False``.
    primary: bool = False
    #: Whether the field requires unique values. Default: ``False``.
    unique: bool = False
    #: Whether the field allows null values. Default: ``True``.
    nullable: bool = True
    #: Whether the field is a global field. Default: ``False``.
    global_: bool = False
    #: Default value expression.
    default: Optional[FMFieldDefault] = None
    #: Relative path for secure external storage (BLOB fields only).
    external_secure_path: Optional[str] = None

    def to_odata_dict(self) -> dict:
        """Return the field definition with the original OData wire key ``global``.

        The Python field is named ``global_`` because ``global`` is a keyword.
        """
        out = {
            "name": self.name,
            "type": self.type,
            "primary": self.primary,
            "unique": self.unique,
            "nullable": self.nullable,
            "global": self.global_,
        }
        if self.default is not None:
            out["default"] = self.default
        if self.external_secure_path is not None:
            out["externalSecurePath"] = self.external_secure_path
        return out


@dataclass
class CreateTableParams:
    """Parameters for creating a table."""

    table_name: str
    fields: List[FMFieldDefinition] = field(default_factory=list)

    def to_odata_dict(self) -> dict:
        return {
            "tableName": self.table_name,
            "fields": [f.to_odata_dict() for f in self.fields],
        }


@dataclass
class AddFieldsParams:
    """Parameters for adding fields to an existing table."""

    table_name: str
    fields: List[FMFieldDefinition] = field(default_factory=list)

    def to_odata_dict(self) -> dict:
        return {
            "tableName": self.table_name,
            "fields": [f.to_odata_dict() for f in self.fields],
        }


#: All supported field types.
FIELD_TYPES: List[FMFieldType] = [
    "NUMERIC", "DECIMAL", "INT", "DATE", "TIME", "TIMESTAMP",
    "VARCHAR", "CHARACTER VARYING", "BLOB", "VARBINARY", "LONGVARBINARY",
    "BINARY VARYING",
]

#: All supported default value expressions.
FIELD_DEFAULTS: List[str] = [
    "USER", "USERNAME", "CURRENT_USER",
    "CURRENT_DATE", "CURDATE",
    "CURRENT_TIME", "CURTIME",
    "CURRENT_TIMESTAMP", "CURTIMESTAMP",
]


@dataclass(frozen=True)
class ParsedFieldType:
    """Result of :func:`parse_field_type`."""

    base_type: str
    length: Optional[int] = None
    repetitions: Optional[int] = None


_LENGTH_RE = re.compile(r"\((\d+)\)")
_REP_RE = re.compile(r"\[(\d+)\]")
_STRIP_LENGTH_RE = re.compile(r"\(.*?\)")
_STRIP_REP_RE = re.compile(r"\[.*?\]")


def parse_field_type(type_str: str) -> ParsedFieldType:
    """Parse a field type string to extract the base type, length, and repetitions.

    Handles patterns like ``"VARCHAR(200)"``, ``"INT[4]"``, ``"VARCHAR(200)[4]"``.
    """
    length_match = _LENGTH_RE.search(type_str)
    rep_match = _REP_RE.search(type_str)
    base_type = _STRIP_REP_RE.sub("", _STRIP_LENGTH_RE.sub("", type_str)).strip()
    return ParsedFieldType(
        base_type=base_type,
        length=int(length_match.group(1)) if length_match else None,
        repetitions=int(rep_match.group(1)) if rep_match else None,
    )
