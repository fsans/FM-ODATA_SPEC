"""Tests for fms_odata_spec.batch."""

from __future__ import annotations

from concurrent.futures import Future

from fms_odata_spec.batch import (
    BatchHandle,
    BatchOpResult,
    BatchOperation,
    BatchRequest,
    BatchResult,
    Changeset,
    generate_boundary,
)


def test_generate_boundary_has_prefix_and_uuid() -> None:
    b = generate_boundary()
    assert b.startswith("batch_")
    # uuid4 hex is 32 chars + 4 hyphens = 36; prefix + underscore = 6
    assert len(b) == 6 + 36

    b2 = generate_boundary("custom")
    assert b2.startswith("custom_")


def test_generate_boundary_is_unique() -> None:
    boundaries = {generate_boundary() for _ in range(100)}
    assert len(boundaries) == 100


def test_batch_operation_defaults() -> None:
    op = BatchOperation(op="list", entity_set="Customers")
    assert op.op == "list"
    assert op.entity_set == "Customers"
    assert op.key is None
    assert op.body is None
    assert op.query is None
    assert op.content_id is None


def test_batch_operation_with_all_fields() -> None:
    op = BatchOperation(
        op="create",
        entity_set="Customers",
        body={"name": "x"},
        content_id=1,
    )
    assert op.body == {"name": "x"}
    assert op.content_id == 1


def test_changeset_constructs() -> None:
    cs = Changeset(operations=[BatchOperation(op="create", entity_set="T")])
    assert len(cs.operations) == 1


def test_batch_request_defaults_empty() -> None:
    r = BatchRequest()
    assert r.retrieve_ops == []
    assert r.changesets == []


def test_batch_op_result_constructs() -> None:
    r: BatchOpResult[dict] = BatchOpResult(status=200, headers={"X": "y"}, ok=True, body={"k": 1})
    assert r.ok is True
    assert r.body == {"k": 1}


def test_batch_result_defaults() -> None:
    r = BatchResult()
    assert r.responses == []
    assert r.ok is False


def test_batch_handle_holds_future() -> None:
    fut: Future[BatchOpResult[int]] = Future()
    h: BatchHandle[int] = BatchHandle(future=fut)
    assert h.future is fut
