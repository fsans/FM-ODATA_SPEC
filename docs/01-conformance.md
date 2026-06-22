# 01 — OData Standard Conformance

## Conformance level

FileMaker Server and FileMaker Cloud support OData at the **intermediate conformance level**, with some exceptions.

The OData 4.01 specification defines three conformance levels: minimal, intermediate, and advanced. FileMaker targets intermediate but does not implement every feature required at that level.

## Supported OData features

These standard OData features are supported by the FileMaker OData API:

| Feature | Status | Notes |
|---------|--------|-------|
| Service document | Supported | GET on the database root returns the service document |
| Metadata (`$metadata`) | Supported | CSDL/EDMX XML format with FileMaker annotations |
| Request records from a table | Supported | GET on `/<database>/<table>` |
| Request individual record | Supported | GET on `/<database>/<table>(<key>)` |
| Request individual field value | Supported | GET on `/<database>/<table>(<key>)/<field>` |
| Request binary field value | Supported | GET on `/<database>/<table>(<key>)/<field>/$value` |
| Navigate related tables | Supported | Via navigation properties and `$expand` |
| Cross join of unrelated tables | Supported | Via `$expand` with cross-join syntax |
| Create a record | Supported | POST on `/<database>/<table>` |
| Update a record | Supported | PATCH or PUT on `/<database>/<table>(<key>)` |
| Delete a record | Supported | DELETE on `/<database>/<table>(<key>)` |
| Update record references (`$ref`) | Supported | POST/PATCH/PUT/DELETE on `.../<related>/$ref` |
| Batch requests (`$batch`) | Supported | POST on `/<database>/$batch` with `multipart/mixed` |
| Query option `$filter` | Supported | With operator/function subset (see below) |
| Query option `$select` | Supported | |
| Query option `$orderby` | Supported | No built-in functions allowed |
| Query option `$top` | Supported | |
| Query option `$skip` | Supported | |
| Query option `$expand` | Supported | |
| Query option `$count` | Supported | Inline form `?$count=true` only (not `/$count` suffix) |
| Query option `$apply` | Supported | aggregate, groupby (Claris 2024+ / FMS 22.0.1+) |
| JSON format | Supported | `application/json` (default) |
| Atom/XML format | Supported | `application/atom+xml` or `application/xml` |
| `IEEE754Compatible=true` | Supported | Edm.Int64 and Edm.Decimal returned as strings |
| `Prefer: odata.continue-on-error` | Supported | |
| `Prefer: odata.maxpagesize` | Supported | |
| `Prefer: return=representation` | Supported | |
| `Prefer: return=minimal` | Supported | |
| Modify schema (create/delete tables, fields, indexes) | Supported | Via system tables (see [docs/10-schema-modification.md](10-schema-modification.md)) |
| Run scripts | Supported (non-standard) | FileMaker-specific action (see [docs/06-scripts.md](06-scripts.md)) |
| Container data upload/download | Supported (non-standard) | FileMaker-specific (see [docs/07-containers.md](07-containers.md)) |
| Webhooks | Supported (non-standard) | FileMaker-specific (see [docs/09-webhooks.md](09-webhooks.md)) |

## Unsupported OData features

These OData features from the intermediate conformance level are **not supported**:

| Feature | Status | Notes |
|---------|--------|-------|
| `$search` query option | Not supported | |
| Lambda operators `any` and `all` | Not supported | |
| `fractionalseconds()` function | Not supported | |
| `isof()` function | Not supported | |
| `geo.distance()` function | Not supported | |
| `geo.length()` function | Not supported | |
| `geo.intersects()` function | Not supported | |
| `$orderby` with built-in functions | Not supported | Only field names, not functions |
| `/$count` suffix form | Not supported | Use inline `?$count=true` instead |
| `$compute` query option | Not supported | |
| Delta query (`$delta`) | Not supported | |
| Asynchronous requests | Not supported | |
| `$format` query option | Limited | Overridden by `Accept` header; not fully documented |

## `$filter` operator and function support

### Supported operators

| Operator | Description |
|----------|-------------|
| `eq` | Equal |
| `ne` | Not equal |
| `gt` | Greater than |
| `ge` | Greater than or equal |
| `lt` | Less than |
| `le` | Less than or equal |
| `and` | Logical AND |
| `or` | Logical OR |
| `not` | Logical NOT |
| `()` | Grouping |

### Supported built-in functions

| Function | Notes |
|----------|-------|
| `startswith()` | |
| `endswith()` | |
| `contains()` | |
| `length()` | |
| `tolower()` | |
| `toupper()` | |
| `trim()` | |
| `substring()` | |
| `indexof()` | |
| `concat()` | |
| `year()` | Date/time |
| `month()` | Date/time |
| `day()` | Date/time |
| `hour()` | Date/time |
| `minute()` | Date/time |
| `second()` | Date/time |
| `date()` | Date/time |
| `time()` | Date/time |
| `round()` | Numeric |
| `floor()` | Numeric |
| `ceiling()` | Numeric |

### Unsupported built-in functions

| Function | Notes |
|----------|-------|
| `fractionalseconds()` | Explicitly unsupported |
| `isof()` | Explicitly unsupported |
| `geo.distance()` | Explicitly unsupported |
| `geo.length()` | Explicitly unsupported |
| `geo.intersects()` | Explicitly unsupported |
| `any` / `all` (lambda) | Explicitly unsupported |

## FileMaker features not accessible via standard OData calls

These FileMaker features are **not directly accessible** through standard OData API calls, but may be available indirectly via scripts:

| Feature | Workaround |
|---------|------------|
| Access to data in external ODBC data sources | Use scripts |
| Calculation fields depending on FileMaker plug-ins | Use scripts |
| Calculation fields depending on host file system info (e.g. `Get(TemporaryPath)`) | Use scripts |
| Calculation fields depending on plug-in info or script triggers | Use scripts |
| Script trigger activation | Not supported (scripts run server-side, triggers do not fire) |

Scripts run by OData API calls are **server-side scripts** — they behave the same as those run by the Perform Script on Server script step, running in separate processes from standard OData API calls.

## Data format support

| Format | Request | Response | Notes |
|--------|---------|----------|-------|
| JSON | `application/json` | `application/json` (default) | Default format |
| Atom/XML | `application/atom+xml` or `application/xml` | `application/atom+xml` or `application/xml` | For XML-structured data |
| HTML | — | `text/html` | Response only |
| Multipart | `multipart/mixed` | `multipart/mixed` | For `$batch` operations |
| Binary | (container-specific Content-Type) | (container-specific) | For container field binary updates |

## HTTP method support

| Method | Used for |
|--------|----------|
| `GET` | Metadata, query, request data |
| `POST` | Create record, create table, create field index, run script, update record references, create webhook |
| `PATCH` | Update record, update record references, update container (binary), add fields to table |
| `PUT` | Create record (alternative), update record, update record references, update container, add fields to table |
| `DELETE` | Delete record, delete table, delete field, delete index, update record references (detach) |
