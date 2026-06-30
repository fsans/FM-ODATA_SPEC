"""Error types for the FileMaker OData API.

Mirrors ``src/errors.ts`` from ``@fms-odata/spec-ts``.

@see docs/13-quirks.md (for real-world error behaviors)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any, List, Optional

__all__ = [
    "ODataErrorDetail",
    "ODataErrorInner",
    "ODataErrorInnerError",
    "ODataErrorBody",
    "RequestRef",
    "FMODataError",
    "FMScriptError",
    "FMAuthError",
    "FMNotFoundError",
    "FMValidationError",
    "is_fm_odata_error",
    "is_fm_script_error",
]

# TypeGuard is 3.10+ in typing. On 3.9 fall back to a no-op alias so the
# annotations still parse (with ``from __future__ import annotations`` they
# are never evaluated at runtime anyway).
if sys.version_info >= (3, 10):
    from typing import TypeGuard
else:  # pragma: no cover - exercised only on 3.9
    try:
        from typing_extensions import TypeGuard  # type: ignore[import-not-found]
    except ImportError:
        from typing import Any as TypeGuard  # type: ignore[assignment]


@dataclass
class ODataErrorDetail:
    """A single detail entry inside an OData error body."""

    code: str
    message: str
    target: Optional[str] = None


@dataclass
class ODataErrorInnerError:
    """The ``innererror`` member of an OData error body."""

    type: str
    message: str


@dataclass
class ODataErrorInner:
    """The ``error`` member of an OData error body."""

    code: str
    message: str
    target: Optional[str] = None
    details: List[ODataErrorDetail] = field(default_factory=list)
    innererror: Optional[ODataErrorInnerError] = None


@dataclass
class ODataErrorBody:
    """OData standard error response body."""

    error: ODataErrorInner


@dataclass
class RequestRef:
    """Reference to the request that caused an error."""

    method: str
    url: str


class FMODataError(Exception):
    """Base error class for all FileMaker OData errors."""

    #: HTTP status code.
    status: int
    #: OData error code (if available).
    code: Optional[str]
    #: OData error object (if available in response body).
    odata_error: Optional[ODataErrorBody]
    #: The request that caused the error.
    request: Optional[RequestRef]

    def __init__(
        self,
        message: str,
        *,
        status: int,
        code: Optional[str] = None,
        odata_error: Optional[ODataErrorBody] = None,
        request: Optional[RequestRef] = None,
    ) -> None:
        super().__init__(message)
        # ``name`` is set for parity with the TS class (which sets ``this.name``);
        # the idiomatic Python check is ``isinstance`` via the ``is_*`` helpers.
        self.name = type(self).__name__
        self.status = status
        self.code = code
        self.odata_error = odata_error
        self.request = request


class FMScriptError(FMODataError):
    """Error thrown when a FileMaker script returns a non-zero exit code."""

    #: Script error code (from ``scriptResult.code``).
    script_error: int
    #: Script result parameter (from ``scriptResult.resultParameter``).
    script_result: Optional[str]

    def __init__(
        self,
        message: str,
        *,
        script_error: int,
        script_result: Optional[str] = None,
        request: Optional[RequestRef] = None,
    ) -> None:
        super().__init__(
            message,
            status=200,  # Script errors return HTTP 200 with error in body
            code=str(script_error),
            request=request,
        )
        self.script_error = script_error
        self.script_result = script_result


class FMAuthError(FMODataError):
    """Authentication error (HTTP 401)."""

    def __init__(self, message: str, request: Optional[RequestRef] = None) -> None:
        super().__init__(message, status=401, request=request)


class FMNotFoundError(FMODataError):
    """Not found error (HTTP 404)."""

    def __init__(self, message: str, request: Optional[RequestRef] = None) -> None:
        super().__init__(message, status=404, request=request)


class FMValidationError(FMODataError):
    """Validation error (HTTP 400)."""

    def __init__(
        self,
        message: str,
        odata_error: Optional[ODataErrorBody] = None,
        request: Optional[RequestRef] = None,
    ) -> None:
        super().__init__(message, status=400, odata_error=odata_error, request=request)


def is_fm_odata_error(err: Any) -> "TypeGuard[FMODataError]":
    """Check if an error is a FileMaker OData error."""
    return isinstance(err, FMODataError)


def is_fm_script_error(err: Any) -> "TypeGuard[FMScriptError]":
    """Check if an error is a FileMaker script error."""
    return isinstance(err, FMScriptError)
