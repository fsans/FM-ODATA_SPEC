"""Authentication types and helpers for the FileMaker OData API.

Mirrors ``src/auth.ts`` from ``@fms-odata/spec-ts``.

@see docs/04-authentication.md
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Awaitable, Callable, Dict, Literal, Optional, Union

__all__ = [
    "FMAuthScheme",
    "FMAuthToken",
    "FMAuthTokenProvider",
    "FMBasicAuthConfig",
    "FMIDAuthConfig",
    "FMAuthConfig",
    "FMAuthHeaders",
    "basic_auth",
    "fmid_auth",
    "normalize_auth_token",
]

#: Authentication scheme supported by FileMaker OData.
FMAuthScheme = Literal["Basic", "FMID"]

#: Static auth token string (e.g. ``"Basic dXNlcjpwYXNz"`` or ``"FMID <token>"``).
FMAuthToken = str

#: Token provider function. Returns the auth header value.
#:
#: May return a coroutine to support token refresh (e.g. Claris ID token
#: expiry). The :func:`basic_auth` / :func:`fmid_auth` helpers themselves stay
#: synchronous (they only build header strings), matching the TS helpers which
#: also do not await.
FMAuthTokenProvider = Callable[[], Union[str, Awaitable[str]]]


@dataclass(frozen=True)
class FMBasicAuthConfig:
    """Configuration for Basic auth (FileMaker Server on-premise)."""

    scheme: Literal["Basic"]
    account: str
    password: str

    def __post_init__(self) -> None:
        if self.scheme != "Basic":
            raise ValueError(f"FMBasicAuthConfig.scheme must be 'Basic', got {self.scheme!r}")


@dataclass(frozen=True)
class FMIDAuthConfig:
    """Configuration for FMID auth (FileMaker Cloud)."""

    scheme: Literal["FMID"]
    token: str
    #: Optional refresh callback invoked on 401 responses.
    on_unauthorized: Optional[Callable[[], Awaitable[str]]] = None

    def __post_init__(self) -> None:
        if self.scheme != "FMID":
            raise ValueError(f"FMIDAuthConfig.scheme must be 'FMID', got {self.scheme!r}")


#: Union of auth configurations, discriminated by the ``scheme`` field.
FMAuthConfig = Union[FMBasicAuthConfig, FMIDAuthConfig]


@dataclass
class FMAuthHeaders:
    """Standard auth-related headers."""

    Authorization: str
    OData_Version: Optional[Literal["4.0"]] = None
    OData_MaxVersion: Optional[Literal["4.0"]] = None

    def to_dict(self) -> Dict[str, str]:
        """Return the headers as a plain dict, dropping unset entries."""
        result: Dict[str, str] = {"Authorization": self.Authorization}
        if self.OData_Version is not None:
            result["OData-Version"] = self.OData_Version
        if self.OData_MaxVersion is not None:
            result["OData-MaxVersion"] = self.OData_MaxVersion
        return result


def basic_auth(account: str, password: str) -> str:
    """Build a Basic auth header value from account and password."""
    raw = f"{account}:{password}".encode("utf-8")
    return f"Basic {base64.b64encode(raw).decode('ascii')}"


def fmid_auth(token: str) -> str:
    """Build an FMID auth header value from a Claris ID token."""
    return f"FMID {token}"


def normalize_auth_token(token: str) -> str:
    """Normalize a token string: if it already has a scheme prefix, use as-is."""
    if token.startswith(("Basic ", "FMID ", "Bearer ")):
        return token
    # Default to Bearer for bare tokens (callers should use basic_auth() or
    # fmid_auth() helpers).
    return f"Bearer {token}"
