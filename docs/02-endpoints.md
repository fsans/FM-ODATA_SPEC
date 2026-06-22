# 02 — Endpoint Reference

This document lists every OData API endpoint exposed by FileMaker Server and FileMaker Cloud, organized by category.

## URL base

```
https://<host>/fmi/odata/v4
```

All endpoints below are relative to this base unless otherwise noted.

## Discovery and metadata

### Get database names

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/fmi/odata/v4` |
| Auth | Required |
| Response | JSON list of database names and their endpoint URLs |

Returns a list of all hosted databases accessible to the authenticated account.

### Get list of tables

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/<database>` |
| Auth | Required |
| Response | JSON list of tables (entity sets) in the database |

### Get list of system table values

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/<database>/<system-table>` |
| Auth | Required |
| Response | JSON list of system table values |

System tables include `FileMaker_Tables`, `FileMaker_Fields`, `FileMaker_Scripts`, etc. See the FileMaker SQL Reference for the full list.

### Get metadata

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/<database>/$metadata` |
| Auth | Required |
| Response | CSDL/EDMX XML with FileMaker annotations |

Returns the complete metadata listing for the database, including entity types, entity sets, actions (scripts), and FileMaker-specific annotations. See [docs/05-metadata.md](05-metadata.md) for annotation details.

## Request data

### Request records from a table

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/<database>/<table>` |
| Auth | Required |
| Query options | `$filter`, `$select`, `$orderby`, `$top`, `$skip`, `$expand`, `$count`, `$apply` |
| Response | JSON collection of records |

The `<table>` segment can be the table name or the FileMaker Table ID (FMTID).

### Request number of records

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/<database>/<table>?$count=true` |
| Auth | Required |
| Response | JSON collection with `@odata.count` property |

Note: the `/$count` suffix form (e.g. `/<table>/$count`) is **not supported**. Use the inline `?$count=true` form. To get only the count without records, combine with `$top=0`.

### Request an individual record

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/<database>/<table>(<primary-key-value>)` |
| Auth | Required |
| Query options | `$select` |
| Response | JSON entity |

### Request an individual field value

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/<database>/<table>(<primary-key-value>)/<field>` |
| Auth | Required |
| Response | JSON with the field value |

### Request the binary value for an individual field

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/<database>/<table>(<primary-key-value>)/<field>/$value` |
| Auth | Required |
| Response | Binary stream |

Used for container fields. See [docs/07-containers.md](07-containers.md).

### Navigate related tables

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/<database>/<table>(<primary-key-value>)/<related-table>` |
| Auth | Required |
| Query options | `$expand`, `$select` |
| Response | JSON entity or collection |

### Request a cross join of unrelated tables

| Property | Value |
|----------|-------|
| Method | `GET` |
| URL | `/<database>/<table>?$expand=<related-table>` |
| Auth | Required |
| Response | JSON with expanded related records |

## Modify data

### Create a record

| Property | Value |
|----------|-------|
| Method | `POST` (or `PUT`) |
| URL | `/<database>/<table>` |
| Auth | Required |
| Content-Type | `application/json` (or `application/atom+xml`) |
| Body | JSON object with field values |
| Response | Created record entity |

Notes:
- Repeating field values: specify repetition in brackets, e.g. `"Name[4]": "value"`.
- Empty JSON objects require at least one nullable field.
- FileMaker global fields are read-only and cannot be set via OData.

### Update a record

| Property | Value |
|----------|-------|
| Method | `PATCH` (or `PUT`) |
| URL | `/<database>/<table>(<primary-key-value>)` |
| Auth | Required |
| Content-Type | `application/json` |
| Body | JSON object with fields to update |
| Response | Updated record entity (if `Prefer: return=representation`) |

### Delete a record

| Property | Value |
|----------|-------|
| Method | `DELETE` |
| URL | `/<database>/<table>(<primary-key-value>)` |
| Auth | Required |
| Response | Empty (HTTP 204) |

### Update record references

| Property | Value |
|----------|-------|
| Method | `POST`, `PATCH`, `PUT` (add/replace), `DELETE` (detach) |
| URL | `/<database>/<table>(<primary-key-value>)/<related-table>/$ref` |
| Auth | Required |
| Content-Type | `application/json` |
| Body (add/replace) | `{"@odata.id": "/fmi/odata/v4/<database>/<related-table>(<key>)"} ` |
| Response | Empty (HTTP 204) |

## Batch requests

### Perform batch operations

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/<database>/$batch` |
| Auth | Required |
| Content-Type | `multipart/mixed; boundary=<batch-boundary>` |
| Body | Multipart MIME with embedded HTTP requests |
| Response | Multipart MIME with responses |

See [docs/08-batch.md](08-batch.md) for format details and FileMaker-specific quirks.

## Scripts

### Run a script

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/<database>/Script.<script-name>` or `/<database>/Script.FMSID:<id>` |
| Auth | Required |
| Content-Type | `application/json` |
| Body | Empty (no parameter) or `{"scriptParameterValue": "<value>"}` |
| Response | `{"scriptResult": {"code": 0, "resultParameter": "..."}}` |

Script scopes:
- Database scope: `/<database>/Script.<name>`
- Entity-set scope: `/<database>/<table>/Script.<name>`
- Record scope: `/<database>/<table>(<key>)/Script.<name>`

See [docs/06-scripts.md](06-scripts.md) for full details.

## Container data

### Create a record with a container field

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/<database>/<table>` |
| Content-Type | `application/json` |
| Body | JSON with base64-encoded container data using `@com.filemaker.odata.Filename` and `@com.filemaker.odata.ContentType` annotations |

### Update a container field with binary data

| Property | Value |
|----------|-------|
| Method | `PATCH` |
| URL | `/<database>/<table>(<primary-key-value>)/<container-field>` |
| Content-Type | `image/png`, `image/jpeg`, `image/gif`, `image/tiff`, or `application/pdf` |
| Headers | `Content-Disposition: inline; filename=<name>` |
| Body | Raw binary data |

Only PNG, JPEG, GIF, TIFF, and PDF binary types are supported for direct binary upload.

### Update container fields with base64-encoded data

| Property | Value |
|----------|-------|
| Method | `PATCH` (or `PUT`) |
| URL | `/<database>/<table>(<primary-key-value>)` |
| Content-Type | `application/json` |
| Body | JSON with base64-encoded data using FileMaker annotations |

Supports updating multiple container fields and regular fields in a single request.

See [docs/07-containers.md](07-containers.md) for full details.

## Schema modification

### Create a table

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/<database>/FileMaker_Tables` |
| Content-Type | `application/json` |
| Body | `{"tableName": "<name>", "fields": [...]}` |

### Add fields to a table

| Property | Value |
|----------|-------|
| Method | `PATCH` (or `PUT`) |
| URL | `/<database>/FileMaker_Tables('<table-name>')` |
| Body | `{"fields": [...]}` |

### Delete a table

| Property | Value |
|----------|-------|
| Method | `DELETE` |
| URL | `/<database>/FileMaker_Tables('<table-name>')` |

### Delete a field

| Property | Value |
|----------|-------|
| Method | `DELETE` |
| URL | `/<database>/FileMaker_Tables('<table-name>')/<field-name>` |

### Create a field index

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/<database>/FileMaker_Indexes` |

### Delete an index

| Property | Value |
|----------|-------|
| Method | `DELETE` |
| URL | `/<database>/FileMaker_Indexes('<index-name>')` |

See [docs/10-schema-modification.md](10-schema-modification.md) for field types and properties.

## Webhooks

### Create a webhook

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/<database>/Webhook.Add` |
| Content-Type | `application/json` |
| Body | `{"webhook": "<url>", "tableName": "<table>", ...}` |

### Delete a webhook

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/<database>/Webhook.Remove` |

### Get specified webhook data

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/<database>/Webhook.Get` |

### Get all webhooks

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/<database>/Webhook.GetAll` |

### Invoke a webhook

| Property | Value |
|----------|-------|
| Method | `POST` |
| URL | `/<database>/Webhook.Invoke` |

See [docs/09-webhooks.md](09-webhooks.md) for full details.
