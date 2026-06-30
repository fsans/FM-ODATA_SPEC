"""Metadata types and $metadata parsing helpers for the FileMaker OData API.

Mirrors ``src/metadata.ts`` from ``@fms-odata/spec-ts``.

@see docs/05-metadata.md
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import List, Literal, Optional, Union

__all__ = [
    "FMBooleanAnnotations",
    "FMValueAnnotations",
    "FMAnnotations",
    "EdmProperty",
    "EdmEntityType",
    "EdmEntitySet",
    "EdmAction",
    "EdmEnumMember",
    "EdmEnumType",
    "ODataMetadata",
    "SYSTEM_FIELDS",
    "ImmutableIdType",
    "SYSTEM_TABLES",
    "FMServerVersion",
    "parse_version_string",
    "parse_server_version",
    "extract_major_version",
    "extract_major_version_from_metadata",
]


@dataclass
class FMBooleanAnnotations:
    """FileMaker-specific boolean field annotations."""

    auto_generated: Optional[bool] = None
    index: Optional[bool] = None
    version_id: Optional[bool] = None
    global_: Optional[bool] = None
    calculation: Optional[bool] = None
    summary: Optional[bool] = None
    computed: Optional[bool] = None


@dataclass
class FMValueAnnotations:
    """FileMaker-specific value annotations."""

    max_repetitions: Optional[int] = None
    external_secure_path: Optional[str] = None
    best_row_id: Optional[str] = None
    row_version: Optional[str] = None
    table_id: Optional[str] = None
    field_id: Optional[str] = None
    script_id: Optional[str] = None
    fm_comment: Optional[str] = None
    ai_annotation: Optional[str] = None


@dataclass
class FMAnnotations(FMBooleanAnnotations, FMValueAnnotations):
    """All FileMaker metadata annotations.

    Combines :class:`FMBooleanAnnotations` and :class:`FMValueAnnotations` and
    adds the product/server version annotations. ``global`` is exposed as
    ``global_`` because ``global`` is a Python keyword.
    """

    #: Product version (from Org.OData.Core.V1.ProductVersion).
    product_version: Optional[str] = None
    #: Server version annotation (Claris 2026+).
    server_version: Optional[str] = None


@dataclass
class EdmProperty:
    """Edm property (field) in an entity type."""

    name: str
    type: str
    nullable: Optional[bool] = None
    max_length: Optional[int] = None
    is_key: Optional[bool] = None
    repetitions: Optional[int] = None
    annotations: Optional[FMAnnotations] = None


@dataclass
class EdmEntityType:
    """Edm entity type (table definition)."""

    name: str
    keys: List[str]
    properties: List[EdmProperty]
    table_id: Optional[str] = None
    comment: Optional[str] = None


@dataclass
class EdmEntitySet:
    """Edm entity set (table occurrence)."""

    name: str
    entity_type: str


@dataclass
class EdmAction:
    """Edm action (FileMaker script)."""

    name: str
    is_bound: bool
    script_id: Optional[str] = None
    parameter_type: Optional[str] = None
    return_type: Optional[str] = None


@dataclass
class EdmEnumMember:
    """A member of an Edm enum type (FileMaker value list entry)."""

    name: str
    value: Union[str, int]


@dataclass
class EdmEnumType:
    """Edm enum type (FileMaker value list)."""

    name: str
    members: List[EdmEnumMember] = field(default_factory=list)


@dataclass
class ODataMetadata:
    """Parsed OData metadata document."""

    namespace: str
    entity_types: List[EdmEntityType]
    entity_sets: List[EdmEntitySet]
    actions: List[EdmAction]
    enum_types: List[EdmEnumType]
    raw: str
    product_version: Optional[str] = None
    server_version: Optional[str] = None


#: FileMaker system fields.
SYSTEM_FIELDS = SimpleNamespace(ROWID="ROWID", ROWMODID="ROWMODID")

#: FileMaker immutable ID types.
ImmutableIdType = Literal["FMTID", "FMFID", "FMSID"]

#: FileMaker system tables.
SYSTEM_TABLES = SimpleNamespace(
    TABLES="FileMaker_Tables",
    FIELDS="FileMaker_Fields",
    INDEXES="FileMaker_Indexes",
)


@dataclass(frozen=True)
class FMServerVersion:
    """Parsed FileMaker Server version with major, minor, patch, and raw string."""

    major: int
    minor: int
    patch: int
    #: Raw string exactly as found in the XML, e.g. ``"21.1.2.500"``.
    raw: str


_VERSION_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")


def parse_version_string(raw: str) -> Optional[FMServerVersion]:
    """Extract a three-part semver from a raw version string.

    Handles strings that may contain a build number (e.g.
    ``"21.1.2.500"`` -> ``major=21, minor=1, patch=2``).
    Returns ``None`` if the string doesn't contain a parseable version.
    """
    if not raw:
        return None
    m = _VERSION_RE.search(raw.strip())
    if not m:
        return None
    return FMServerVersion(
        major=int(m.group(1)),
        minor=int(m.group(2)),
        patch=int(m.group(3)),
        raw=raw.strip(),
    )


# Regex strategies for parse_server_version, aligned with fms-odata-mcp
# (src/fm-version.ts). Each captures the String attribute value.
_STRATEGY_1A = re.compile(
    r'''Term\s*=\s*["']Org\.OData\.Core\.V1\.ProductVersion["'][^>]*?String\s*=\s*["']([^"']+)["']'''
)
_STRATEGY_1B = re.compile(
    r'''String\s*=\s*["']([^"']+)["'][^>]*?Term\s*=\s*["']Org\.OData\.Core\.V1\.ProductVersion["']'''
)
_STRATEGY_1C = re.compile(
    r'''Term\s*=\s*["']ServerVersion["'][^>]*?String\s*=\s*["']([^"']+)["']''',
    re.IGNORECASE,
)
_STRATEGY_1D = re.compile(
    r'''String\s*=\s*["']([^"']+)["'][^>]*?Term\s*=\s*["']ServerVersion["']''',
    re.IGNORECASE,
)
_STRATEGY_2 = re.compile(
    r'''Term\s*=\s*["'][^"']*Version[^"']*["'][^>]*?String\s*=\s*["'][^"']*?(\d{2,}\.\d+\.\d+(?:\.\d+)?)[^"']*?["']''',
    re.IGNORECASE,
)


def parse_server_version(metadata_xml: str) -> Optional[FMServerVersion]:
    """Parse the FileMaker Server version from an OData $metadata XML string.

    Detection reads the $metadata XML using 4 strategies in priority order:

    1a. ``<Annotation Term="Org.OData.Core.V1.ProductVersion" String="x.x.x.build"/>``
    1b. Same as 1a but with reversed attribute order (String before Term)
    1c. ``<Annotation Term="ServerVersion" String="OData Engine 26.0.1"/>`` (FM 26+)
    1d. Same as 1c but with reversed attribute order
    2.  Generic fallback: any annotation whose term contains "Version" and whose
        String value contains a version with major >= 17 (avoids false positives
        from OData spec "4.0")

    Returns ``None`` if no strategy yields a parseable version.

    This implementation is aligned with the proven detection logic from
    fms-odata-mcp (src/fm-version.ts).
    """
    if not metadata_xml or not isinstance(metadata_xml, str):
        return None

    for pattern in (_STRATEGY_1A, _STRATEGY_1B):
        m = pattern.search(metadata_xml)
        if m:
            v = parse_version_string(m.group(1))
            if v:
                return v

    for pattern in (_STRATEGY_1C, _STRATEGY_1D):
        m = pattern.search(metadata_xml)
        if m:
            v = parse_version_string(m.group(1))
            if v and v.major >= 17:
                return v

    m = _STRATEGY_2.search(metadata_xml)
    if m:
        v = parse_version_string(m.group(1))
        if v and v.major >= 17:
            return v

    return None


def extract_major_version(product_version: Optional[str]) -> Optional[str]:
    """Extract the FileMaker Server major version string from a product version string.

    Convenience wrapper around :func:`parse_version_string`.
    Returns ``None`` if the version cannot be determined.
    """
    if not product_version:
        return None
    v = parse_version_string(product_version)
    return str(v.major) if v else None


def extract_major_version_from_metadata(metadata_xml: str) -> Optional[str]:
    """Extract the FileMaker Server major version from a $metadata XML string.

    Uses :func:`parse_server_version` internally and returns just the major
    version number as a string, or ``None`` if the version cannot be determined.
    """
    v = parse_server_version(metadata_xml)
    return str(v.major) if v else None
