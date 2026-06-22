# 10 — Schema Modification (DDL)

FileMaker OData supports creating and deleting tables, fields, and indexes via the system tables `FileMaker_Tables` and `FileMaker_Indexes`. These are DDL operations that modify the database schema.

## Create a table

### Request

```
POST /fmi/odata/v4/<database>/FileMaker_Tables
Content-Type: application/json
```

### Body

```json
{
  "tableName": "Company",
  "fields": [
    {
      "name": "Company ID",
      "type": "int",
      "primary": true
    },
    {
      "name": "User ID",
      "type": "varchar(20)",
      "unique": true,
      "default": "CURRENT_USER"
    },
    {
      "name": "Company Name",
      "type": "varchar(100)",
      "nullable": false
    },
    {
      "name": "Notes",
      "type": "varchar(2000)",
      "global": true
    },
    {
      "name": "Signed Contract",
      "type": "blob",
      "externalSecurePath": "ContactMgmt/"
    }
  ]
}
```

### Atom/XML alternative

```xml
<TableDefinition tableName="Company">
  <FieldDefinition name="Company ID" type="int" primary="true"/>
  <FieldDefinition name="User ID" type="varchar(20)" unique="true" default="CURRENT_USER"/>
  <FieldDefinition name="Company Name" type="varchar(100)" nullable="false"/>
  <FieldDefinition name="Notes" type="varchar(2000)" global="true"/>
</TableDefinition>
```

## Field types

| Type | Description |
|------|-------------|
| `NUMERIC` | Numeric |
| `DECIMAL` | Decimal number |
| `INT` | Integer |
| `DATE` | Date |
| `TIME` | Time |
| `TIMESTAMP` | Timestamp |
| `VARCHAR(n)` | Variable-length text (max length n) |
| `CHARACTER VARYING` | Variable-length text (alias) |
| `BLOB` | Binary large object (container) |
| `VARBINARY` | Variable-length binary |
| `LONGVARBINARY` | Long variable-length binary |
| `BINARY VARYING` | Variable-length binary (alias) |

When creating a new table and specifying `NULL` as the default type, the keyword value defaults to `TIMESTAMP`.

### Repetitions

Repetitions are specified in brackets after the type:

```json
{
  "name": "QuarterlyTotals",
  "type": "INT[4]"
}
```

### Text field length

Maximum length of a text field is specified in parentheses:

```json
{
  "name": "CompanyName",
  "type": "VARCHAR(200)"
}
```

## Field properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `name` | string | (required) | Field name |
| `type` | string | (required) | Field type (see above) |
| `primary` | boolean | `false` | Whether the field is a primary key |
| `unique` | boolean | `false` | Whether the field requires unique values |
| `nullable` | boolean | `true` | Whether the field allows null values |
| `global` | boolean | `false` | Whether the field is a global field |
| `default` | string | — | Default value expression |
| `externalSecurePath` | string | — | Relative path for secure external storage (BLOB fields only) |

### Default value expressions

| Expression | Description |
|------------|-------------|
| `USER` | Current user name |
| `USERNAME` | Current user name (alias) |
| `CURRENT_USER` | Current user name (alias) |
| `CURRENT_DATE` | Current date |
| `CURDATE` | Current date (alias) |
| `CURRENT_TIME` | Current time |
| `CURTIME` | Current time (alias) |
| `CURRENT_TIMESTAMP` | Current timestamp |
| `CURTIMESTAMP` | Current timestamp (alias) |

## Add fields to a table

### Request

```
PATCH /fmi/odata/v4/<database>/FileMaker_Tables('<table-name>')
Content-Type: application/json
```

### Body

```json
{
  "fields": [
    {
      "name": "NewField",
      "type": "varchar(50)"
    }
  ]
}
```

`PUT` can also be used for this operation.

## Delete a table

### Request

```
DELETE /fmi/odata/v4/<database>/FileMaker_Tables('<table-name>')
```

## Delete a field

### Request

```
DELETE /fmi/odata/v4/<database>/FileMaker_Tables('<table-name>')/<field-name>
```

## Create a field index

### Request

```
POST /fmi/odata/v4/<database>/FileMaker_Indexes
Content-Type: application/json
```

## Delete an index

### Request

```
DELETE /fmi/odata/v4/<database>/FileMaker_Indexes('<index-name>')
```

## Security considerations

Schema modification operations are powerful and potentially destructive. Downstream libraries should:

1. **Gate DDL behind explicit opt-in**: Require a configuration flag (e.g., `FM_ALLOW_SCHEMA_EDITS=true`) before exposing DDL operations.
2. **Require confirmation for destructive operations**: Delete table and delete field operations should require an explicit confirmation parameter.
3. **Validate field types**: Ensure field types are from the supported set before sending.
4. **Handle repetitions and length**: Parse `type` strings with bracket and parenthesis suffixes correctly.
5. **Document privilege requirements**: DDL operations require appropriate FileMaker account privileges.
