# 07 — Container Fields

Container fields store binary data (images, PDFs, files) in FileMaker. The OData API provides two mechanisms for uploading container data: **binary** (raw bytes) and **base64-encoded** (JSON body). Downloading container data is done via the `/$value` path segment.

## Container storage types

FileMaker container data can be stored in three ways:
- **Embedded**: Data is stored directly in the field.
- **File reference**: Field stores a reference to a file path.
- **External storage**: Data is stored externally (secure storage or open storage).

The OData API handles all three storage types transparently.

## Uploading container data

### Method 1: Binary data (single field)

Updates a single container field with raw binary data.

#### Request

```
PATCH /fmi/odata/v4/<database>/<table>(<primary-key-value>)/<container-field>
```

#### Headers

| Header | Value |
|--------|-------|
| `Authorization` | `<auth>` |
| `Content-Type` | `image/png`, `image/jpeg`, `image/gif`, `image/tiff`, or `application/pdf` |
| `Content-Disposition` | `inline; filename=<filename>` |
| `OData-Version` | `4.0` |
| `OData-MaxVersion` | `4.0` |

#### Body

Raw binary data.

#### Supported binary types

Only these MIME types are supported for binary upload:

| MIME type | Extension |
|-----------|-----------|
| `image/png` | .png |
| `image/jpeg` | .jpg, .jpeg |
| `image/gif` | .gif |
| `image/tiff` | .tif, .tiff |
| `application/pdf` | .pdf |

#### Example (cURL)

```bash
curl --request PATCH \
  "https://myhost.example.com/fmi/odata/v4/ContactMgmt/Contacts('ALFKI')/Photo" \
  --header 'Content-Type: image/png' \
  --header 'Authorization: Basic YWRtaW46YWRtaW4=' \
  --header 'OData-Version: 4.0' \
  --header 'OData-MaxVersion: 4.0' \
  --header 'Content-Disposition: inline; filename=ALFKI.png' \
  --data-binary '@photo.png'
```

#### Content-Disposition format

- ASCII filenames: `Content-Disposition: inline; filename=name.png`
- Non-ASCII filenames: `Content-Disposition: inline; filename*=UTF-8''<percent-encoded-name>` (RFC 5987)

Some clients send both forms; FileMaker accepts either.

### Method 2: Base64-encoded data (JSON body)

Updates one or more container fields (and optionally regular fields) in a single request using base64-encoded data in a JSON body.

#### Request

```
PATCH /fmi/odata/v4/<database>/<table>(<primary-key-value>)
```

#### Headers

| Header | Value |
|--------|-------|
| `Authorization` | `<auth>` |
| `Content-Type` | `application/json` |
| `OData-Version` | `4.0` |
| `OData-MaxVersion` | `4.0` |

#### Body

```json
{
  "Photo": {
    "@com.filemaker.odata.Filename": "profile.png",
    "@com.filemaker.odata.ContentType": "image/png",
    "data": "<base64-encoded-data>"
  },
  "RegularField": "updated value"
}
```

#### FileMaker-specific annotations

| Annotation | Description |
|------------|-------------|
| `@com.filemaker.odata.Filename` | Filename to store in the container |
| `@com.filemaker.odata.ContentType` | MIME type of the data |
| `data` | Base64-encoded binary data |

#### Advantages over binary method

- Can update multiple container fields in one request.
- Can update container fields and regular fields simultaneously.
- Not limited to the 5 binary MIME types — any content type can be specified.

### Method 3: Create a record with a container field

Creates a new record with container data in a single POST request.

#### Request

```
POST /fmi/odata/v4/<database>/<table>
```

#### Body

Same JSON format as Method 2 (base64 with annotations).

## Downloading container data

### Request

```
GET /fmi/odata/v4/<database>/<table>(<primary-key-value>)/<container-field>/$value
```

### Response

Binary stream of the container data.

### Accept header quirk

| Accept header | Response |
|---------------|----------|
| `application/octet-stream` | Returns the stored filename as `text/plain` (NOT the binary data) |
| `*/*` or any other value | Returns the actual binary data |

**Always use `Accept: */*` (or omit the Accept header) for container downloads.** Do not use `application/octet-stream`.

## Auto-generated filenames

When uploading binary data without specifying a filename in `Content-Disposition`, FileMaker generates a default filename of `Untitled.png` (regardless of actual content type). The binary data is correct; only the filename is cosmetic. Always pass an explicit filename to avoid this.

## Deleting container data

To clear a container field, update it with an empty value:

```
PATCH /fmi/odata/v4/<database>/<table>(<primary-key-value>)
Content-Type: application/json

{
  "ContainerField": null
}
```

Or use the binary method with an empty body (not recommended — behavior varies by version).

## Wrapper library guidance

Downstream libraries should:

1. Support both binary and base64 upload methods.
2. Auto-detect MIME type from file magic bytes when not explicitly provided.
3. Always send `Content-Disposition` with an explicit filename for binary uploads.
4. Use `Accept: */*` for container downloads (never `application/octet-stream`).
5. Support both ASCII and RFC 5987 non-ASCII filename formats in `Content-Disposition`.
6. Provide a streaming download method for large containers.
7. Handle the `Untitled.png` auto-generated filename case by always passing an explicit name.
8. For MCP/JSON-based transports that cannot handle raw binary, use the base64 method exclusively.
