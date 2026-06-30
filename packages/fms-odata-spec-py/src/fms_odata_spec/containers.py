"""Container field types and helpers for the FileMaker OData API.

Mirrors ``src/containers.ts`` from ``@fms-odata/spec-ts``.

@see docs/07-containers.md
"""

from __future__ import annotations

import base64
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional

__all__ = [
    "ContainerBinaryMimeType",
    "CONTAINER_BINARY_MIME_TYPES",
    "ContainerEncoding",
    "ContainerUploadInput",
    "ContainerDownload",
    "FMContainerAnnotations",
    "sniff_container_mime",
    "build_content_disposition",
    "to_base64",
]

#: MIME types supported for binary container upload.
ContainerBinaryMimeType = Literal[
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/tiff",
    "application/pdf",
]

#: All supported binary MIME types.
CONTAINER_BINARY_MIME_TYPES: List[ContainerBinaryMimeType] = [
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/tiff",
    "application/pdf",
]

#: Upload encoding mode.
ContainerEncoding = Literal["binary", "base64"]


@dataclass
class ContainerUploadInput:
    """Input for uploading container data.

    The TS ``data: Blob | ArrayBuffer | Uint8Array`` is typed as ``bytes`` in
    Python (no Blob in the stdlib). Callers reading from a file should pass
    ``bytes`` directly.
    """

    data: bytes
    #: MIME type. Auto-detected from magic bytes if omitted for binary mode.
    content_type: Optional[str] = None
    #: Filename to store in the container.
    filename: Optional[str] = None
    #: Encoding mode. Default: ``"binary"``.
    encoding: Optional[ContainerEncoding] = None


@dataclass
class ContainerDownload:
    """Container download result."""

    data: bytes
    content_type: str
    filename: Optional[str] = None


@dataclass
class FMContainerAnnotations:
    """FileMaker-specific container annotations for base64 JSON body.

    The TS interface uses dotted/``@``-prefixed keys
    (``@com.filemaker.odata.Filename``) which are not valid Python identifiers.
    The dataclass fields are therefore ``filename`` / ``content_type`` /
    ``data``; use :meth:`to_odata_dict` to emit the original wire keys for JSON
    serialization.
    """

    filename: str
    content_type: str
    #: base64-encoded payload.
    data: str

    def to_odata_dict(self) -> Dict[str, Any]:
        """Return the annotations as a dict with the original OData wire keys."""
        return {
            "@com.filemaker.odata.Filename": self.filename,
            "@com.filemaker.odata.ContentType": self.content_type,
            "data": self.data,
        }


def sniff_container_mime(bytes_data: bytes) -> Optional[ContainerBinaryMimeType]:
    """Sniff the MIME type from file magic bytes.

    Returns one of the supported binary types, or ``None`` if unrecognized.
    """
    if len(bytes_data) < 4:
        return None
    b = bytes_data
    # PNG: 89 50 4E 47
    if b[0] == 0x89 and b[1] == 0x50 and b[2] == 0x4E and b[3] == 0x47:
        return "image/png"
    # JPEG: FF D8 FF
    if b[0] == 0xFF and b[1] == 0xD8 and b[2] == 0xFF:
        return "image/jpeg"
    # GIF: 47 49 46 38
    if b[0] == 0x47 and b[1] == 0x49 and b[2] == 0x46 and b[3] == 0x38:
        return "image/gif"
    # TIFF: 49 49 2A 00 or 4D 4D 00 2A
    if (b[0] == 0x49 and b[1] == 0x49 and b[2] == 0x2A and b[3] == 0x00) or (
        b[0] == 0x4D and b[1] == 0x4D and b[2] == 0x00 and b[3] == 0x2A
    ):
        return "image/tiff"
    # PDF: 25 50 44 46
    if b[0] == 0x25 and b[1] == 0x50 and b[2] == 0x44 and b[3] == 0x46:
        return "application/pdf"
    return None


_ASCII_RE = re.compile(r"^[\x20-\x7E]+$")


def build_content_disposition(filename: str) -> str:
    """Build a Content-Disposition header value for container upload.

    Uses unquoted form for ASCII, RFC 5987 for non-ASCII.
    """
    if _ASCII_RE.match(filename):
        return f"inline; filename={filename}"
    # RFC 5987 for non-ASCII
    from urllib.parse import quote

    encoded = quote(filename)
    return f"inline; filename*=UTF-8''{encoded}"


def to_base64(data: bytes) -> str:
    """Convert binary data to a base64 string."""
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError(f"to_base64 expects bytes-like, got {type(data).__name__}")
    return base64.b64encode(data).decode("ascii")
