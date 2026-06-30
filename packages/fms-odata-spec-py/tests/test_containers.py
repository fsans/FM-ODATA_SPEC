"""Tests for fms_odata_spec.containers."""

from __future__ import annotations

import base64

import pytest

from fms_odata_spec.containers import (
    CONTAINER_BINARY_MIME_TYPES,
    ContainerDownload,
    ContainerUploadInput,
    FMContainerAnnotations,
    build_content_disposition,
    sniff_container_mime,
    to_base64,
)


def test_container_binary_mime_types_complete() -> None:
    assert set(CONTAINER_BINARY_MIME_TYPES) == {
        "image/png", "image/jpeg", "image/gif", "image/tiff", "application/pdf",
    }


@pytest.mark.parametrize(
    "magic,expected",
    [
        (b"\x89PNG", "image/png"),
        (b"\xff\xd8\xff\xe0", "image/jpeg"),
        (b"GIF8", "image/gif"),
        (b"II*\x00", "image/tiff"),
        (b"MM\x00*", "image/tiff"),
        (b"%PDF", "application/pdf"),
        (b"XXXX", None),
        (b"abc", None),  # too short
        (b"", None),
    ],
)
def test_sniff_container_mime(magic: bytes, expected: object) -> None:
    assert sniff_container_mime(magic) == expected  # type: ignore[arg-type]


def test_build_content_disposition_ascii() -> None:
    assert build_content_disposition("file.txt") == "inline; filename=file.txt"


def test_build_content_disposition_non_ascii() -> None:
    out = build_content_disposition("café.pdf")
    assert out.startswith("inline; filename*=UTF-8''")
    assert "caf" in out  # encoded form present


def test_to_base64_roundtrip() -> None:
    data = b"hello world"
    encoded = to_base64(data)
    assert base64.b64decode(encoded) == data


def test_to_base64_empty() -> None:
    assert to_base64(b"") == ""


def test_to_base64_rejects_non_bytes() -> None:
    with pytest.raises(TypeError):
        to_base64("not bytes")  # type: ignore[arg-type]


def test_container_upload_input_constructs() -> None:
    u = ContainerUploadInput(data=b"\x89PNG", content_type="image/png", filename="x.png")
    assert u.data == b"\x89PNG"
    assert u.encoding is None


def test_container_download_constructs() -> None:
    d = ContainerDownload(data=b"x", content_type="text/plain", filename="a.txt")
    assert d.data == b"x"
    assert d.filename == "a.txt"


def test_fm_container_annotations_to_odata_dict() -> None:
    a = FMContainerAnnotations(filename="x.png", content_type="image/png", data="b64")
    d = a.to_odata_dict()
    assert d == {
        "@com.filemaker.odata.Filename": "x.png",
        "@com.filemaker.odata.ContentType": "image/png",
        "data": "b64",
    }
