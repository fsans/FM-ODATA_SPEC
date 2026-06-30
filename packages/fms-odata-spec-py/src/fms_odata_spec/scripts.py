"""Script execution types and response parsing for the FileMaker OData API.

Mirrors ``src/scripts.ts`` from ``@fms-odata/spec-ts``.

@see docs/06-scripts.md
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Dict, Literal, Optional, Union

__all__ = [
    "ScriptScope",
    "ScriptOptions",
    "ScriptNameId",
    "ScriptFmsidId",
    "ScriptIdentifier",
    "ScriptResultInner",
    "ScriptResultEnvelope",
    "ScriptResult",
    "ScriptDescriptor",
    "SCRIPT_ERROR_CODES",
    "script_path_segment",
    "script_request_body",
    "parse_script_response",
]

#: Script invocation scope.
ScriptScope = Literal["database", "entitySet", "record"]


@dataclass
class ScriptOptions:
    """Options for running a script.

    The TS ``signal?: AbortSignal`` field has no direct stdlib Python
    equivalent; it is replaced with ``cancel_event?: threading.Event`` as a
    placeholder for cancellation. Downstream async runtimes can adapt.
    """

    parameter: Optional[Union[str, int, float, Dict[str, Any]]] = None
    cancel_event: Optional[threading.Event] = None


@dataclass(frozen=True)
class ScriptNameId:
    """Script identifier by name."""

    type: Literal["name"]
    name: str


@dataclass(frozen=True)
class ScriptFmsidId:
    """Script identifier by FMSID."""

    type: Literal["fmsid"]
    id: int


#: Script identifier: either name or FMSID, discriminated by ``type``.
ScriptIdentifier = Union[ScriptNameId, ScriptFmsidId]


@dataclass
class ScriptResultInner:
    """Inner ``scriptResult`` object from the OData API."""

    code: int
    result_parameter: Optional[str] = None


@dataclass
class ScriptResultEnvelope:
    """Script result from the OData API."""

    script_result: ScriptResultInner


@dataclass
class ScriptResult:
    """Parsed script result."""

    #: Exit Script code (0 = success).
    code: int
    #: Raw response data.
    raw: Any
    #: Text result from Exit Script step.
    result_parameter: Optional[str] = None


@dataclass
class ScriptDescriptor:
    """Script descriptor from metadata."""

    name: str
    is_bound: bool
    fmsid: Optional[str] = None
    parameter_type: Optional[str] = None
    return_type: Optional[str] = None


#: Common FileMaker script error codes.
SCRIPT_ERROR_CODES = SimpleNamespace(
    SUCCESS=0,
    RECORD_MISSING=101,
    NO_RECORDS_FOUND=401,
    USER_CANCELED=1,
    FILE_MISSING=3,
    FILE_INACCESSIBLE=4,
    PASSWORD_REQUIRED=212,
)


def script_path_segment(id: ScriptIdentifier) -> str:
    """Build the URL path segment for a script invocation."""
    if id.type == "name":
        return f"Script.{id.name}"
    return f"Script.FMSID:{id.id}"


def script_request_body(options: Optional[ScriptOptions] = None) -> Optional[str]:
    """Build the request body for a script invocation.

    Returns ``None`` for no-parameter scripts (empty body).
    """
    if options is None or options.parameter is None:
        return None
    return json.dumps({"scriptParameterValue": options.parameter})


def parse_script_response(raw: Any) -> ScriptResult:
    """Parse the raw JSON response from a script invocation into a :class:`ScriptResult`.

    FMS returns a nested envelope::

        {"scriptResult": {"code": 0, "resultParameter": "Hello World"}}

    This helper extracts ``code`` and ``resultParameter`` from the nested
    object. A non-zero code indicates a script error.
    """
    if raw is None or not isinstance(raw, dict):
        return ScriptResult(code=0, raw=raw)

    script_result = raw.get("scriptResult")
    if isinstance(script_result, dict):
        nested = script_result
        code = nested.get("code")
        result_parameter = nested.get("resultParameter")
        return ScriptResult(
            code=int(code) if code is not None else 0,
            result_parameter=(
                str(result_parameter) if result_parameter is not None else None
            ),
            raw=raw,
        )

    # Fallback for older FMS versions that may use flat shape.
    return ScriptResult(code=0, raw=raw)
