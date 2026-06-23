# 03 — Query Options

FileMaker OData supports a subset of OData 4.0 system query options. This document details each supported option, its syntax, and FileMaker-specific notes.

## Supported query options

| Option | Supported | Notes |
|--------|-----------|-------|
| `$filter` | Yes | Operator/function subset (see [docs/01-conformance.md](01-conformance.md)) |
| `$select` | Yes | |
| `$orderby` | Yes | Field names only; no built-in functions |
| `$top` | Yes | |
| `$skip` | Yes | |
| `$expand` | Yes | Navigation properties |
| `$count` | Yes | Inline `?$count=true` only; `/$count` suffix not supported |
| `$apply` | Yes | Claris 2024+ (FMS 22.0.1+) |
| `$search` | No | Explicitly unsupported |
| `$compute` | No | Not supported |
| `$format` | Limited | Overridden by `Accept` header |

## `$filter`

Filters records by evaluating an expression for each record.

### Syntax

```
GET /<database>/<table>?$filter=<expression>
```

### Example

```
/fmi/odata/v4/ContactMgmt/Contacts?$filter=Title eq 'Manager' or startswith(Title,'Admin')
```

### FileMaker-specific notes

- Date, time, and timestamp formats conform to ISO 8601. Time zone offsets are relative to the server's time zone.
- Field names with special characters (spaces, underscores) must be enclosed in double-quotation marks: `"First Name" eq 'John'`.
- Field names can be replaced with FileMaker Field IDs (FMFID) for stability across renames (Claris 2026+).
- See [docs/01-conformance.md](01-conformance.md) for the full list of supported operators and functions.

## `$select`

Limits the fields returned for each record.

### Syntax

```
GET /<database>/<table>?$select=<field1>,<field2>,...
```

### Example

```
/fmi/odata/v4/ContactMgmt/Contacts?$select=Company,Website
```

### Default behavior

By default, all fields are returned **except** container and summary fields.

### FileMaker-specific notes

- The `ROWID` and `ROWMODID` system fields are included by specifying them in `$select`: `$select=ROWID, ROWMODID`.
  - `ROWID` = `Get(RecordID)` for the record.
  - `ROWMODID` = `Get(RecordModificationCount)` for the record.
- `$select` queries can be nested within other `$select` queries and within other query options:
  ```
  GET /Categories?$expand=Products&$select=Name,Products/Name
  ```

## `$orderby`

Sorts records in ascending (default) or descending order.

### Syntax

```
GET /<database>/<table>?$orderby=<field> {asc|desc}
```

### Example

```
/fmi/odata/v4/ContactMgmt/Contacts?$orderby=Company desc
```

### FileMaker-specific notes

- Field names with special characters must be enclosed in double-quotation marks.
- The `$orderby` option does **not** support OData built-in functions — only field names.
- The `<field>` segment can be the field name or the FileMaker Field ID (FMFID).

## `$top` and `$skip`

Paginates through a result set.

### Syntax

```
GET /<database>/<table>?$top=<number>
GET /<database>/<table>?$skip=<number>
GET /<database>/<table>?$top=<number>&$skip=<number>
```

### Examples

```
/fmi/odata/v4/ContactMgmt/Contacts?$top=2        # First 2 records
/fmi/odata/v4/ContactMgmt/Contacts?$skip=19       # Records starting from 20th
/fmi/odata/v4/ContactMgmt/Contacts?$top=10&$skip=20  # Records 21-30
```

## `$expand`

Includes related records along with the primary records in the response.

### Syntax

```
GET /<database>/<table>?$expand=<related-table>
```

### Example

```
/fmi/odata/v4/ContactMgmt/Contacts?$expand=Orders
```

### Nested expansion

`$expand` can be combined with `$select` for nested field selection:

```
GET /Categories?$expand=Products&$select=Name,Products/Name
```

## `$count`

Requests a count of matching records alongside the records.

### Syntax

```
GET /<database>/<table>?$count=true
```

### Example

```
/fmi/odata/v4/ContactMgmt/Contacts?$count=true
```

### FileMaker-specific notes

- `$count` ignores `$top` and `$skip` — it returns the total count across all matching records, including those matching `$filter` if specified.
- The `/$count` suffix form (e.g. `/<table>/$count`) is **not supported**. Always use the inline `?$count=true` form.
- To get only the count without records, combine with `$top=0`: `?$count=true&$top=0`.

## `$apply`

Transforms returned records using aggregation and grouping.

### Syntax

```
GET /<database>/<table>?$apply=<transformation>
```

### Supported transformations

| Transformation | Description |
|----------------|-------------|
| `aggregate(<field> with <function> as <alias>)` | Aggregate a field |
| `aggregate(<field> add <value> with <function> as <alias>)` | Aggregate with offset |
| `groupby(("<field1>", "<field2>"))` | Group by fields |
| `groupby(("<field>"), aggregate(...))` | Group by with aggregation |

### Aggregate functions

| Function | Description |
|----------|-------------|
| `sum` | Sum of values |
| `min` | Minimum value |
| `max` | Maximum value |
| `average` | Average of values |
| `countdistinct` | Count of distinct values |

### Examples

```
# Aggregate with sum and average
/fmi/odata/v4/Inventory/Purchase?$apply=aggregate(Total add 1 with sum as t, Total with average as a)

# Group by only
/fmi/odata/v4/Inventory/Purchase?$apply=groupby(("Product ID", "Customer ID"))

# Group by with aggregation
/fmi/odata/v4/Inventory/Purchase?$apply=groupby(("Product ID", "Customer ID"), aggregate(Total add 1 with sum as t, Total with average as a))
```

### Version requirement

`$apply` is supported in **Claris 2024+ (FileMaker Server 22.0.1+)**. Earlier versions return an error.

## Combining query options

Multiple query options can be combined in a single request using `&`:

```
GET /<database>/<table>?$filter=<expr>&$select=<fields>&$orderby=<field> desc&$top=10&$skip=20&$count=true
```

## URL encoding notes

- Commas in `$select`, `$orderby`, and `$expand` must **not** be percent-encoded (FileMaker rejects `%2C`).
- Dollar signs in system query options must **not** be percent-encoded (FileMaker rejects `%24`).
- Parentheses in `$apply` expressions must **not** be percent-encoded (FileMaker rejects `%28`/`%29`). The `aggregate(...)` and `groupby((...))` syntax requires literal parentheses.
- Single quotes in string literals must be doubled: `'O''Brien'`.
- Spaces should be encoded as `%20`, not `+`.
- See [docs/13-quirks.md](13-quirks.md) for full encoding details.
