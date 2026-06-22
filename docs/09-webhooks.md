# 09 — Webhooks

FileMaker OData supports webhooks that activate when records or table schema change. Webhooks are a FileMaker-specific extension — they are not part of the OData standard.

## Overview

- Webhooks are activated when records or table schema change.
- Only record changes matching webhook filters activate the webhooks.
- Only fields set by webhook selects are returned in the payload.
- Webhook payloads are sent as HTTP POST requests to the configured endpoint URL.

## Endpoints

All webhook operations use POST with JSON bodies.

### Create a webhook

```
POST /fmi/odata/v4/<database>/Webhook.Add
```

#### Body

```json
{
  "webhook": "https://my.example.com:8080/webhook",
  "endpointHeaders": {
    "Content-Type": "application/json"
  },
  "queryHeaders": {
    "Prefer": "fmodata.entity-ids",
    "Accept": "application/json;IEEE754Compatible=true"
  },
  "tableName": "myTable",
  "notifySchemaChanges": true,
  "select": "PrimaryKey,CreatedBy",
  "filter": "CreatedBy eq 'Admin'",
  "maxFailedAttempts": 10
}
```

#### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `webhook` | Yes | — | URL to receive webhook POST payloads |
| `tableName` | Yes | — | Table to monitor for changes |
| `endpointHeaders` | No | `{}` | Headers sent to the endpoint URL (does not affect processing) |
| `queryHeaders` | No | `{}` | Headers controlling how the webhook payload is generated |
| `headers` | No | `{}` | Legacy alias for `endpointHeaders` |
| `notifySchemaChanges` | No | `false` | Whether to notify on schema changes |
| `select` | No | `""` | Comma-separated field list to include in payload |
| `filter` | No | `""` | OData filter expression; only matching records trigger webhook |
| `maxFailedAttempts` | No | `0` | Max retry attempts (0 = infinite) |

#### `queryHeaders` behavior

`queryHeaders` control how the webhook payload is generated:

| Query header | Effect on payload |
|--------------|-------------------|
| `Prefer: fmodata.entity-ids` | Payload uses entity IDs instead of table/field names |
| `Accept: application/json;IEEE754Compatible=true` | Decimal values enclosed in quotes |

#### `endpointHeaders` vs `queryHeaders`

- `endpointHeaders` (or legacy `headers`): Always sent to the endpoint URL without affecting processing.
- `queryHeaders`: Control how the webhook payload is generated (affect the query that produces the payload).

#### `maxFailedAttempts`

- `0` = no maximum; retry indefinitely until success or webhook deletion.
- Any positive integer = max retry attempts before giving up.
- Retry attempts are logged in the `fmodata.log` file.

### Delete a webhook

```
POST /fmi/odata/v4/<database>/Webhook.Remove
```

### Get specified webhook data

```
POST /fmi/odata/v4/<database>/Webhook.Get
```

### Get all webhooks

```
POST /fmi/odata/v4/<database>/Webhook.GetAll
```

### Invoke a webhook

```
POST /fmi/odata/v4/<database>/Webhook.Invoke
```

Manually triggers a webhook (useful for testing).

## Webhook payload

When a record or schema change matches a webhook's filter, FileMaker sends an HTTP POST to the configured `webhook` URL. The payload:
- Contains the fields specified in `select`.
- Is formatted according to `queryHeaders`.
- Includes `endpointHeaders` in the request.

## Wrapper library guidance

Downstream libraries should:

1. Provide typed interfaces for webhook creation parameters.
2. Distinguish between `endpointHeaders` and `queryHeaders` clearly.
3. Support the legacy `headers` alias for backward compatibility.
4. Handle `maxFailedAttempts` semantics (0 = infinite).
5. Provide methods for all five webhook operations (Add, Remove, Get, GetAll, Invoke).
6. For MCP servers, expose webhook management as tools with clear parameter documentation.
