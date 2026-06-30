"""Tests for fms_odata_spec.errors."""

from __future__ import annotations

import pytest

from fms_odata_spec.errors import (
    FMAuthError,
    FMNotFoundError,
    FMODataError,
    FMScriptError,
    FMValidationError,
    ODataErrorBody,
    ODataErrorDetail,
    ODataErrorInner,
    RequestRef,
    is_fm_odata_error,
    is_fm_script_error,
)


def test_fm_odata_error_carries_status_and_code() -> None:
    e = FMODataError("boom", status=500, code="X100")
    assert e.status == 500
    assert e.code == "X100"
    assert str(e) == "boom"
    assert e.name == "FMODataError"
    assert e.odata_error is None
    assert e.request is None


def test_fm_odata_error_with_request_ref() -> None:
    req = RequestRef(method="GET", url="https://x/y")
    e = FMODataError("boom", status=500, request=req)
    assert e.request is not None
    assert e.request.method == "GET"
    assert e.request.url == "https://x/y"


def test_fm_script_error_status_is_200() -> None:
    e = FMScriptError("script failed", script_error=101, script_result="missing")
    assert e.status == 200  # script errors return HTTP 200 with error in body
    assert e.code == "101"
    assert e.script_error == 101
    assert e.script_result == "missing"
    assert e.name == "FMScriptError"
    assert isinstance(e, FMODataError)


def test_fm_auth_error_status_401() -> None:
    e = FMAuthError("nope")
    assert e.status == 401
    assert isinstance(e, FMODataError)


def test_fm_not_found_error_status_404() -> None:
    e = FMNotFoundError("missing")
    assert e.status == 404


def test_fm_validation_error_status_400() -> None:
    body = ODataErrorBody(
        error=ODataErrorInner(code="V1", message="bad", details=[ODataErrorDetail(code="D", message="d")])
    )
    e = FMValidationError("bad", odata_error=body)
    assert e.status == 400
    assert e.odata_error is not None
    assert e.odata_error.error.details[0].code == "D"


def test_is_fm_odata_error_true_for_subclasses() -> None:
    assert is_fm_odata_error(FMAuthError("x")) is True
    assert is_fm_odata_error(FMScriptError("x", script_error=1)) is True
    assert is_fm_odata_error(ValueError("x")) is False


def test_is_fm_script_error_distinguishes() -> None:
    assert is_fm_script_error(FMScriptError("x", script_error=1)) is True
    assert is_fm_script_error(FMAuthError("x")) is False
    assert is_fm_script_error(ValueError("x")) is False


def test_errors_are_raisable_and_catchable() -> None:
    with pytest.raises(FMODataError):
        raise FMAuthError("nope")
    with pytest.raises(FMScriptError):
        raise FMScriptError("s", script_error=3)
