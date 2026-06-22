# 13 — Quirks and Workarounds

This document captures real-world behaviors of the FileMaker OData API that differ from the official documentation or from standard OData expectations. These quirks were observed in the two reference wrapper repositories (`FMS-ODATA-MCP` and `fm-odata-js`) and in production usage.

## URL encoding quirks

### Commas must not be percent-encoded

**Behavior**: FileMaker rejects `%2C` (percent-encoded comma) in `$select`, `$orderby`, and `$expand` query options.

**Workaround**: After URL-encoding query option values, un-encode commas. Most HTTP client libraries percent-encode commas by default; they must be explicitly preserved.

```javascript
// Wrong: $select=Company%2CWebsite
// Right: $select=Company,Website
```

### Dollar signs must not be percent-encoded

**Behavior**: FileMaker rejects `%24` (percent-encoded dollar sign) in system query option names.

**Workaround**: System query option names (`$filter`, `$select`, etc.) must retain their literal `$` character.

```javascript
// Wrong: %24filter=...
// Right: $filter=...
```

### Single quotes in string keys must be doubled

**Behavior**: OData requires single quotes inside string literals to be doubled.

**Workaround**: Escape single quotes as `''` in string key values.

```
// For the name O'Brien:
GET /Contacts('O''Brien')
```

### Spaces should be `%20`, not `+`

**Behavior**: FileMaker expects standard percent-encoding for spaces (`%20`), not the `+` form used in form-urlencoded encoding.

**Workaround**: Use `%20` for spaces in URLs.

## `/$count` suffix not supported

**Behavior**: The standard OData `/$count` suffix (e.g., `GET /Contacts/$count`) returns HTTP 400 Bad Request.

**Workaround**: Use the inline query option form: `GET /Contacts?$count=true`. To get only the count without records, combine with `$top=0`: `GET /Contacts?$count=true&$top=0`.

## Container download Accept header quirk

**Behavior**: Sending `Accept: application/octet-stream` for a container field download returns the stored filename as `text/plain`, NOT the binary data.

**Workaround**: Use `Accept: */*` (or omit the Accept header) for container downloads. Any value other than `application/octet-stream` returns the actual binary data.

## Auto-generated filename for container uploads

**Behavior**: When uploading binary container data without specifying a filename in `Content-Disposition`, FileMaker generates `Untitled.png` regardless of the actual content type. The binary data is correct; only the filename is wrong.

**Workaround**: Always pass an explicit filename in the `Content-Disposition` header.

```
Content-Disposition: inline; filename=myphoto.jpg
```

## HTTP Basic auth required (not Data API tokens)

**Behavior**: The FileMaker Data API (`/fmi/data/v1/`) uses a bearer token obtained via `POST /auth`. That token does NOT work with the OData API.

**Workaround**: OData requires HTTP Basic auth (FileMaker Server) or FMID token (FileMaker Cloud). Do not attempt to reuse Data API tokens.

## Self-signed TLS certificates

**Behavior**: FileMaker Server deployments on LANs commonly use self-signed SSL certificates. Standard HTTP clients reject these by default.

**Workaround**: In development, configure the HTTP client to skip TLS verification. In Node.js, set `NODE_TLS_REJECT_UNAUTHORIZED=0` (never use in production). In Axios, use a custom `httpsAgent` with `rejectUnauthorized: false`. Always use proper certificates in production.

## Batch request GET ordering bug

**Behavior**: On some FileMaker Server versions (observed in 21.x and some later versions), GET operations placed before changesets in a batch request cause issues:
- GET operations before changesets may not be processed correctly.
- Multiple consecutive GETs may result in the last one being silently dropped.

**Workaround**: Place all changesets first, then GET operations at the end of the batch. Limit to one GET operation at the end, or accept potential loss of results.

## Date/time formatting

**Behavior**: FileMaker returns timestamps in UTC ISO-8601 format, with or without milliseconds depending on the version and field configuration.

**Workaround**: Parse both formats (with and without milliseconds). When sending dates, use ISO-8601 without milliseconds for maximum compatibility.

## OData-Version headers

**Behavior**: The OData spec mandates `OData-Version: 4.0` and `OData-MaxVersion: 4.0` headers. In practice, FileMaker Server 2026 accepts requests without them.

**Workaround**: Always send both headers per spec for correctness and forward compatibility, even though they're currently optional.

## Field name quoting

**Behavior**: Field names with special characters (spaces, underscores) must be enclosed in double-quotation marks in `$filter` and `$orderby`.

**Workaround**: Auto-quote field names containing spaces or special characters. On Claris 2026+, use FMFID instead of field names to avoid quoting issues entirely.

## Non-ASCII field names

**Behavior**: Non-ASCII field names (e.g., accented characters) can cause encoding issues in `$filter` expressions.

**Workaround**: On Claris 2026+, resolve non-ASCII field names to their FMFID (from `$metadata`) and use the ID in queries. On older versions, ensure proper UTF-8 encoding and double-quote the field name.

## Empty POST body for scripts without parameters

**Behavior**: When running a script without a parameter, the POST body must be completely empty. Some HTTP clients add a default `Content-Type: application/json` header even for empty bodies, which can cause issues.

**Workaround**: Explicitly omit the body and set `Content-Type` appropriately. Some clients may need to send `Content-Length: 0`.

## Script names with special characters

**Behavior**: OData does not support script names with special characters (`@`, `&`, `/`) or names beginning with a number.

**Workaround**: On Claris 2026+, use `Script.FMSID:<id>` instead of the script name. On older versions, rename the script to avoid special characters.

## Global fields are read-only

**Behavior**: FileMaker global fields cannot be updated via OData. Attempting to set a global field in a create or update operation is silently ignored or causes an error.

**Workaround**: Do not include global fields in create/update payloads. If global field values need to change, use a script.

## Repeating field syntax

**Behavior**: Repeating field values are accessed by specifying the repetition number in brackets.

**Workaround**: Use `FieldName[repetition]` syntax in both reads and writes:
- Read: `$select=QuarterlyTotals[1],QuarterlyTotals[2]`
- Write: `{"QuarterlyTotals[4]": 100}`

## Edm.Stream vs Edm.Binary for containers

**Behavior**: Different FileMaker Server versions emit different Edm types for container fields in `$metadata`:
- Some versions: `Edm.Stream`
- Some versions: `Edm.Binary`

**Workaround**: Metadata parsers must accept both types as indicating a container field.

## Content-Disposition format for non-ASCII filenames

**Behavior**: FileMaker accepts both unquoted and RFC 5987 formats for `Content-Disposition` filenames.

**Workaround**: For ASCII filenames, use: `Content-Disposition: inline; filename=name.png`. For non-ASCII filenames, use RFC 5987: `Content-Disposition: inline; filename*=UTF-8''<percent-encoded>`. Some clients send both forms; FileMaker accepts either.

## Script result serialization

**Behavior**: The `scriptResult` field in script responses is always a string, even when the script returns a number or boolean. The `scriptError` field is also always a string (e.g., `"0"`, `"101"`).

**Workaround**: Parse `scriptResult` and `scriptError` explicitly (e.g., `Number(scriptResult)`) rather than relying on type coercion.

## URL length limit

**Behavior**: The maximum URL length is influenced by OS, web server, and browser differences. Excessively long URLs (especially with complex `$filter` expressions) may fail.

**Workaround**: Limit URLs to 2,000 characters for cross-platform safety. For very complex filters, consider using batch requests or server-side scripts.
