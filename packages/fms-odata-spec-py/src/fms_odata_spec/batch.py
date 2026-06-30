"""Batch request types for the FileMaker OData API.

Mirrors ``src/batch.ts`` from ``@fms-odata/spec-ts``.

@see docs/08-batch.md
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar, Union

__all__ = [
    "BatchOpType",
    "BatchOperation",
    "Changeset",
    "BatchRequest",
    "BatchOpResult",
    "BatchResult",
    "BatchHandle",
    "generate_boundary",
]

#: Batch operation type.
BatchOpType = Literal["list", "get", "create", "patch", "put", "delete"]

T = TypeVar("T")


@dataclass
class BatchOperation:
    """A single operation in a batch request."""

    #: Operation type.
    op: BatchOpType
    #: Entity set (table) name.
    entity_set: str
    #: Record key (for get, patch, put, delete).
    key: Optional[Union[str, int]] = None
    #: Request body (for create, patch, put).
    body: Optional[Dict[str, Any]] = None
    #: Query parameters (for list, get).
    query: Optional[Dict[str, Any]] = None
    #: Content-ID for referencing within changeset.
    content_id: Optional[int] = None


@dataclass
class Changeset:
    """A changeset is a group of atomic write operations."""

    operations: List[BatchOperation] = field(default_factory=list)


@dataclass
class BatchRequest:
    """A batch request consists of retrieve operations and changesets."""

    #: Retrieve operations (GET) -- executed outside changesets.
    retrieve_ops: List[BatchOperation] = field(default_factory=list)
    #: Changesets (atomic write groups).
    changesets: List[Changeset] = field(default_factory=list)


@dataclass
class BatchOpResult(Generic[T]):
    """Result of a single batch operation."""

    status: int
    headers: Dict[str, str]
    ok: bool
    body: Optional[T] = None
    #: Content-ID if specified in the request.
    content_id: Optional[int] = None


@dataclass
class BatchResult:
    """Overall batch result."""

    responses: List[BatchOpResult[Any]] = field(default_factory=list)
    ok: bool = False


@dataclass
class BatchHandle(Generic[T]):
    """Handle for tracking a queued operation's result.

    The TS ``promise: Promise<BatchOpResult<T>>`` is mapped to a
    :class:`concurrent.futures.Future`. This is a types-only package, so no
    event loop is wired up; downstream code is responsible for resolving the
    future.
    """

    future: "Future[BatchOpResult[T]]"  # noqa: F821  -- forward ref to concurrent.futures.Future


def generate_boundary(prefix: str = "batch") -> str:
    """Generate a unique boundary string for multipart MIME.

    Uses :func:`uuid.uuid4` for uniqueness.
    """
    return f"{prefix}_{uuid.uuid4()}"
