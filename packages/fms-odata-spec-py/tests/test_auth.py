"""Tests for fms_odata_spec.auth."""

from __future__ import annotations

import base64

import pytest

from fms_odata_spec.auth import (
    FMAuthHeaders,
    FMBasicAuthConfig,
    FMIDAuthConfig,
    basic_auth,
    fmid_auth,
    normalize_auth_token,
)


def test_basic_auth_encodes_account_password() -> None:
    expected = "Basic " + base64.b64encode(b"admin:secret").decode("ascii")
    assert basic_auth("admin", "secret") == expected


def test_basic_auth_unicode() -> None:
    raw = "user:päss".encode("utf-8")
    expected = "Basic " + base64.b64encode(raw).decode("ascii")
    assert basic_auth("user", "päss") == expected


def test_fmid_auth_prefixes_token() -> None:
    assert fmid_auth("abc123") == "FMID abc123"


@pytest.mark.parametrize(
    "token,expected",
    [
        ("Basic abc", "Basic abc"),
        ("FMID xyz", "FMID xyz"),
        ("Bearer t0k", "Bearer t0k"),
        ("baretoken", "Bearer baretoken"),
    ],
)
def test_normalize_auth_token(token: str, expected: str) -> None:
    assert normalize_auth_token(token) == expected


def test_basic_auth_config_constructs() -> None:
    cfg = FMBasicAuthConfig(scheme="Basic", account="a", password="b")
    assert cfg.scheme == "Basic"
    assert cfg.account == "a"
    assert cfg.password == "b"


def test_basic_auth_config_rejects_wrong_scheme() -> None:
    # The Literal type prevents passing "FMID" at static-analysis time; the
    # runtime __post_init__ guard catches it too. Bypass the type checker via
    # object.__setattr__ to exercise the guard.
    cfg = FMBasicAuthConfig.__new__(FMBasicAuthConfig)
    object.__setattr__(cfg, "scheme", "FMID")
    object.__setattr__(cfg, "account", "a")
    object.__setattr__(cfg, "password", "b")
    with pytest.raises(ValueError):
        cfg.__post_init__()


def test_fmid_auth_config_constructs() -> None:
    cfg = FMIDAuthConfig(scheme="FMID", token="t")
    assert cfg.scheme == "FMID"
    assert cfg.token == "t"
    assert cfg.on_unauthorized is None


def test_fmid_auth_config_with_refresh() -> None:
    async def refresh() -> str:
        return "new"

    cfg = FMIDAuthConfig(scheme="FMID", token="t", on_unauthorized=refresh)
    assert cfg.on_unauthorized is refresh


def test_auth_headers_to_dict_drops_unset() -> None:
    h = FMAuthHeaders(Authorization="Basic x")
    assert h.to_dict() == {"Authorization": "Basic x"}


def test_auth_headers_to_dict_includes_odata_headers() -> None:
    h = FMAuthHeaders(
        Authorization="Basic x",
        OData_Version="4.0",
        OData_MaxVersion="4.0",
    )
    d = h.to_dict()
    assert d == {
        "Authorization": "Basic x",
        "OData-Version": "4.0",
        "OData-MaxVersion": "4.0",
    }
