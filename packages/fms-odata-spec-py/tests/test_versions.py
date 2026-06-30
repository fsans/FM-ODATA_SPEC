"""Tests for fms_odata_spec.versions."""

from __future__ import annotations

import pytest

from fms_odata_spec import versions
from fms_odata_spec.versions import (
    FM_VERSION_MATRIX,
    FM_VERSION_NAMES,
    ODATA_PROTOCOL_VERSION,
    has_feature,
    has_query_option,
    min_version_for_feature,
)


def test_protocol_version_is_4_0() -> None:
    assert ODATA_PROTOCOL_VERSION == "4.0"


def test_version_names_cover_all_majors() -> None:
    assert set(FM_VERSION_NAMES) == {"19", "21", "22", "26", "future"}
    assert FM_VERSION_NAMES["26"] == "Claris FileMaker 2026"


def test_matrix_has_all_versions() -> None:
    assert set(FM_VERSION_MATRIX) == {"19", "21", "22", "26", "future"}


@pytest.mark.parametrize(
    "version,feature,expected",
    [
        ("19", "webhooks", False),
        ("21", "webhooks", True),
        ("26", "scripts_by_fmsid", True),
        ("19", "scripts_by_fmsid", False),
        ("26", "auth_basic", True),
        ("19", "auth_fmid", False),
        ("21", "auth_fmid", True),
        ("future", "ai_annotation", True),
    ],
)
def test_has_feature(version: str, feature: str, expected: bool) -> None:
    assert has_feature(version, feature) is expected  # type: ignore[arg-type]


def test_has_feature_unknown_version_returns_false() -> None:
    assert has_feature("99", "webhooks") is False  # type: ignore[arg-type]


def test_has_feature_unknown_feature_returns_false() -> None:
    assert has_feature("26", "nonexistent_feature") is False


@pytest.mark.parametrize(
    "version,option,expected",
    [
        ("19", "apply", False),
        ("22", "apply", True),
        ("26", "filter", True),
        ("19", "search", False),
        ("26", "compute", False),
    ],
)
def test_has_query_option(version: str, option: str, expected: bool) -> None:
    assert has_query_option(version, option) is expected  # type: ignore[arg-type]


def test_min_version_for_feature() -> None:
    assert min_version_for_feature("webhooks") == "21"
    assert min_version_for_feature("scripts_by_fmsid") == "26"
    assert min_version_for_feature("auth_basic") == "19"
    assert min_version_for_feature("ai_annotation") == "26"


def test_min_version_for_unknown_feature_returns_none() -> None:
    assert min_version_for_feature("nonexistent") is None


def test_version_info_fields() -> None:
    info = FM_VERSION_MATRIX["26"]
    assert info.major == "26"
    assert info.name == "Claris FileMaker 2026"
    assert info.release_year == 2026
    assert info.status == "current"
    assert info.features.scripts_by_fmsid is True
    assert info.query_options.apply is True


def test_feature_flags_is_frozen() -> None:
    flags = FM_VERSION_MATRIX["19"].features
    with pytest.raises(Exception):
        flags.webhooks = True  # type: ignore[misc]
