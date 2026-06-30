"""Tests for fms_odata_spec.scripts."""

from __future__ import annotations

import json

import pytest

from fms_odata_spec.scripts import (
    SCRIPT_ERROR_CODES,
    ScriptDescriptor,
    ScriptFmsidId,
    ScriptNameId,
    ScriptOptions,
    ScriptResult,
    parse_script_response,
    script_path_segment,
    script_request_body,
)


def test_script_error_codes() -> None:
    assert SCRIPT_ERROR_CODES.SUCCESS == 0
    assert SCRIPT_ERROR_CODES.RECORD_MISSING == 101
    assert SCRIPT_ERROR_CODES.NO_RECORDS_FOUND == 401


def test_script_path_segment_by_name() -> None:
    sid: ScriptNameId = ScriptNameId(type="name", name="MyScript")
    assert script_path_segment(sid) == "Script.MyScript"


def test_script_path_segment_by_fmsid() -> None:
    sid: ScriptFmsidId = ScriptFmsidId(type="fmsid", id=42)
    assert script_path_segment(sid) == "Script.FMSID:42"


def test_script_request_body_none_when_no_options() -> None:
    assert script_request_body(None) is None


def test_script_request_body_none_when_no_parameter() -> None:
    assert script_request_body(ScriptOptions()) is None


def test_script_request_body_with_string_parameter() -> None:
    body = script_request_body(ScriptOptions(parameter="hello"))
    assert body is not None
    assert json.loads(body) == {"scriptParameterValue": "hello"}


def test_script_request_body_with_dict_parameter() -> None:
    body = script_request_body(ScriptOptions(parameter={"k": 1}))
    assert body is not None
    assert json.loads(body) == {"scriptParameterValue": {"k": 1}}


def test_script_request_body_with_int_parameter() -> None:
    body = script_request_body(ScriptOptions(parameter=7))
    assert body is not None
    assert json.loads(body) == {"scriptParameterValue": 7}


def test_parse_script_response_nested_envelope() -> None:
    raw = {"scriptResult": {"code": 0, "resultParameter": "Hello World"}}
    r = parse_script_response(raw)
    assert r.code == 0
    assert r.result_parameter == "Hello World"
    assert r.raw is raw


def test_parse_script_response_nonzero_code() -> None:
    raw = {"scriptResult": {"code": 101, "resultParameter": "missing"}}
    r = parse_script_response(raw)
    assert r.code == 101
    assert r.result_parameter == "missing"


def test_parse_script_response_missing_code_defaults_zero() -> None:
    raw = {"scriptResult": {"resultParameter": "x"}}
    r = parse_script_response(raw)
    assert r.code == 0
    assert r.result_parameter == "x"


def test_parse_script_response_flat_fallback() -> None:
    raw = {"unrelated": 1}
    r = parse_script_response(raw)
    assert r.code == 0
    assert r.raw is raw


def test_parse_script_response_non_dict() -> None:
    assert parse_script_response(None).code == 0  # type: ignore[arg-type]
    assert parse_script_response("string").code == 0  # type: ignore[arg-type]
    assert parse_script_response(42).code == 0  # type: ignore[arg-type]


def test_script_descriptor_constructs() -> None:
    d = ScriptDescriptor(name="MyScript", is_bound=True, fmsid="123")
    assert d.is_bound is True
    assert d.fmsid == "123"


def test_script_options_defaults() -> None:
    o = ScriptOptions()
    assert o.parameter is None
    assert o.cancel_event is None
