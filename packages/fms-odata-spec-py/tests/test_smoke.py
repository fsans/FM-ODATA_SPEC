"""Smoke test for the package skeleton (will be expanded per module)."""

from __future__ import annotations


def test_package_imports() -> None:
    import fms_odata_spec

    assert hasattr(fms_odata_spec, "__version__")
    assert fms_odata_spec.__version__ == "0.1.0"
