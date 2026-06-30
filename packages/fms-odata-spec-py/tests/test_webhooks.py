"""Tests for fms_odata_spec.webhooks."""

from __future__ import annotations

from fms_odata_spec.webhooks import WebhookCreateParams, WebhookData, webhook_path


def test_webhook_path() -> None:
    assert webhook_path("MyDB", "Add") == "/MyDB/Webhook.Add"
    assert webhook_path("MyDB", "GetAll") == "/MyDB/Webhook.GetAll"


def test_webhook_create_params_to_odata_dict() -> None:
    p = WebhookCreateParams(
        webhook="https://example.com/hook",
        table_name="Customers",
        endpoint_headers={"X-Token": "abc"},
        notify_schema_changes=True,
        select="id,name",
        filter="status eq 'open'",
        max_failed_attempts=3,
    )
    d = p.to_odata_dict()
    assert d["webhook"] == "https://example.com/hook"
    assert d["tableName"] == "Customers"
    assert d["endpointHeaders"] == {"X-Token": "abc"}
    assert d["notifySchemaChanges"] is True
    assert d["select"] == "id,name"
    assert d["filter"] == "status eq 'open'"
    assert d["maxFailedAttempts"] == 3


def test_webhook_create_params_minimal() -> None:
    p = WebhookCreateParams(webhook="u", table_name="t")
    d = p.to_odata_dict()
    assert d == {"webhook": "u", "tableName": "t"}


def test_webhook_data_to_odata_dict() -> None:
    w = WebhookData(
        id="abc",
        webhook="https://example.com/hook",
        table_name="Customers",
        query_headers={"X": "y"},
    )
    d = w.to_odata_dict()
    assert d["id"] == "abc"
    assert d["queryHeaders"] == {"X": "y"}
    assert d["tableName"] == "Customers"
