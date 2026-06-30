"""Tests for the public API surface of fms_odata_spec."""

from __future__ import annotations

import fms_odata_spec


def test_version_string() -> None:
    assert fms_odata_spec.__version__ == "0.1.0"


def test_all_exported_names_resolve() -> None:
    """Every name in __all__ must be an attribute on the package."""
    missing = [name for name in fms_odata_spec.__all__ if not hasattr(fms_odata_spec, name)]
    assert missing == [], f"Missing exported names: {missing}"


def test_all_contains_version() -> None:
    assert "__version__" in fms_odata_spec.__all__
