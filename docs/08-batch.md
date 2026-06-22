# 08 — Batch Requests

OData batch requests allow multiple operations to be sent in a single HTTP request. FileMaker supports the standard OData `$batch` mechanism with `multipart/mixed` content type.

## Endpoint

```
POST /fmi/odata/v4/<database>/$batch
```

## Request format

### Headers

| Header | Value |
|--------|-------|
| `Authorization` | `<auth>` |
| `Content-Type` | `multipart/mixed; boundary=<batch-boundary>` |
| `OData-Version` | `4.0` |
| `OData-MaxVersion` | `4.0` |

### Body structure

The body is a multipart MIME document containing:
- **Retrieve operations** (GET requests) — direct children of the batch boundary.
- **Change sets** (atomic write operations) — grouped within a `multipart/mixed` changeset boundary.

### Example

```
POST https://host/fmi/odata/v4/ContactMgmt/$batch
OData-Version: 4.0
Content-Type: multipart/mixed; boundary=batch_36522ad7-fc75-4b56-8c71-56071383e77b
Authorization: Basic YWRtaW46YWRtaW4=

--batch_36522ad7-fc75-4b56-8c71-56071383e77b
Content-Type: application/http

GET https://host/fmi/odata/v4/ContactMgmt/Contacts(1) HTTP/1.1

--batch_36522ad7-fc75-4b56-8c71-56071383e77b
Content-Type: multipart/mixed; boundary=changeset_77162fcd-b8da-41ac-a9f8-9357efbbd

--changeset_77162fcd-b8da-41ac-a9f8-9357efbbd
Content-Type: application/http
Content-ID: 1

POST https://host/fmi/odata/v4/ContactMgmt/Contacts HTTP/1.1
Content-Type: application/json
Content-Length: 162

{
  "PrimaryKey": "BJONES",
  "Name": "Bob Jones",
  "Zone": 1,
  "Title": "SouthWest Sale Manager",
  "Company": "Example, Inc.",
  "Website": "www.example.com"
}

--changeset_77162fcd-b8da-41ac-a9f8-9357efbbd
Content-Type: application/http
Content-ID: 2

PATCH https://host/fmi/odata/v4/ContactMgmt/Contacts(1) HTTP/1.1
Content-Type: application/json
Content-Length: 32

{
  "Title": "Software Engineer"
}

--changeset_77162fcd-b8da-41ac-a9f8-9357efbbd
Content-Type: application/http
Content-ID: 3

DELETE https://host/fmi/odata/v4/ContactMgmt/Contacts(7) HTTP/1.1

--changeset_77162fcd-b8da-41ac-a9f8-9357efbbd--
--batch_36522ad7-fc75-4b56-8c71-56071383e77b
Content-Type: application/http

GET https://host/fmi/odata/v4/ContactMgmt/Contacts(1) HTTP/1.1

--batch_36522ad7-fc75-4b56-8c71-56071383e77b--
```

## Supported operations

| Operation | In changeset? | Notes |
|-----------|---------------|-------|
| GET (retrieve) | No | Direct child of batch boundary |
| POST (create) | Yes | Inside changeset |
| PATCH (update) | Yes | Inside changeset |
| PUT (update/insert) | Yes | Inside changeset |
| DELETE (delete) | Yes | Inside changeset |

## Change sets

Operations within a changeset are **atomic** — either all succeed or all fail. If any operation in a changeset fails, the entire changeset is rolled back.

Retrieve operations (GET) outside changesets are independent and do not roll back.

## Content-ID

Each operation within a changeset can specify a `Content-ID` header. This allows subsequent operations to reference the entity created by a prior operation in the same changeset using `$<Content-ID>` as the entity reference.

## Response format

The response is a multipart MIME document mirroring the request structure, with each part containing the HTTP response for the corresponding request.

## FileMaker-specific quirks

### GET ordering bug (FMS 21.x and some later versions)

**Observed behavior**: On some FileMaker Server versions, GET operations placed before changesets in a batch request cause parsing issues:
- GET operations must **not** appear before changesets.
- Multiple consecutive GETs may result in the last one being silently dropped.

**Workaround**: Place all changesets first, then GET operations at the end. Limit to one GET operation at the end, or accept potential loss of results.

This is a known parser bug and may be fixed in future versions. Test on your target FileMaker Server version before relying on specific batch ordering.

### Boundary format

- Boundary strings should be unique per request (use UUIDs).
- Boundary strings must not appear anywhere in the body content.
- Both batch and changeset boundaries follow the same format rules.

### Content-Length

Each embedded HTTP request should include a `Content-Length` header matching the body size. Some FileMaker versions are strict about this; omitting it may cause parsing errors.

## Wrapper library guidance

Downstream libraries should:

1. Provide a batch builder API that handles multipart MIME construction.
2. Auto-generate unique boundary strings (UUIDs recommended).
3. Group write operations into changesets automatically.
4. Place GET operations after changesets (to work around the ordering bug).
5. Parse the multipart response and map responses to original operations by order/Content-ID.
6. Expose per-operation results (status, body, headers) and an overall success flag.
7. Handle the GET-before-changeset quirk by reordering or warning.
8. For MCP/JSON-based transports, serialize batch operations as a JSON array and reconstruct the multipart MIME internally.
