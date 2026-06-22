# 06 — Scripts

FileMaker scripts are exposed as OData **actions** on a system table named `Script`. Running a script via OData executes it as a **server-side script** (equivalent to Perform Script on Server).

## Endpoint

### By name

```
POST /fmi/odata/v4/<database>/Script.<script-name>
```

### By script ID (Claris 2026+)

```
POST /fmi/odata/v4/<database>/Script.FMSID:<script-id>
```

Using the FMSID is recommended for production integrations because it survives script renames.

## Script scopes

Scripts can be invoked at three scopes:

| Scope | URL pattern | Description |
|-------|-------------|-------------|
| Database | `/<database>/Script.<name>` | Script runs with database context |
| Entity-set | `/<database>/<table>/Script.<name>` | Script runs with table context |
| Record | `/<database>/<table>(<key>)/Script.<name>` | Script runs with record context |

## Request

### Headers

```
Authorization: <auth>
Content-Type: application/json
OData-Version: 4.0
OData-MaxVersion: 4.0
```

### Body

- **No parameter**: POST body must be completely empty.
- **With parameter**: POST body must contain a single field `scriptParameterValue`:

```json
{
  "scriptParameterValue": "World"
}
```

The `scriptParameterValue` accepts:
- String values
- Number values
- JSON object values

### Example (cURL)

```bash
curl --request POST \
  "https://myhost.example.com/fmi/odata/v4/ContactMgmt/Script.HelloScript" \
  --header 'Authorization: Basic YWRtaW46YWRtaW4=' \
  --header 'Content-Type: application/json' \
  --header 'OData-Version: 4.0' \
  --header 'OData-MaxVersion: 4.0' \
  --data '{"scriptParameterValue": "World"}'
```

## Response

If the script includes the Exit Script script step, the text result is returned in `resultParameter`:

```json
{
  "scriptResult": {
    "code": 0,
    "resultParameter": "Hello World"
  }
}
```

| Field | Description |
|-------|-------------|
| `scriptResult.code` | Exit Script code (0 = success) |
| `scriptResult.resultParameter` | Text result from Exit Script step |

## Script name restrictions

OData does **not** support script names with:
- Special characters: `@`, `&`, `/`, etc.
- Names beginning with a number

If a script name contains unsupported characters, use the FMSID form (`Script.FMSID:<id>`) instead (Claris 2026+).

## Server-side script behavior

Scripts run by OData API calls are **server-side scripts**:

- They run in separate processes from standard OData API calls.
- They behave the same as scripts run by the Perform Script on Server script step.
- They run without user interaction — OData only supports scripts that run without UI.
- Script triggers do **not** fire when scripts are run via OData.

## What scripts can do

Scripts can access FileMaker features that are not directly available via standard OData calls:

| Feature | Available via script? |
|---------|----------------------|
| External ODBC data source access | Yes |
| Calculation fields depending on plug-ins | Yes |
| Calculation fields depending on host file system info | Yes |
| Calculation fields depending on script triggers | Yes (but triggers don't fire) |
| Commit records | Yes (recommended) |

## Best practices for OData-callable scripts

1. **Include Commit Records/Requests**: Data changes are not accessible until saved to the server. Add the Commit Records/Requests script step at the end of any script that modifies data.
2. **Use only web-compatible script steps**: Verify scripts use only steps supported by OData.
3. **Restrict with privileges**: Use accounts and privileges to restrict which scripts a web service can run.
4. **Consider privilege interactions**: If a script includes a step to delete records but the web service account doesn't allow deletion, the step is skipped but the script may continue — leading to unexpected results.
5. **Use Full Access privilege for elevated scripts**: In FileMaker Pro, grant Full Access privilege to a script to allow it to perform tasks the calling account cannot.
6. **Test on hosted databases**: Open each script that web users might run and verify it works when the database is hosted for OData access.

## Discovering available scripts

Scripts are listed in the `$metadata` response as OData actions. Each script has:
- Name (action name)
- FMSID (FileMaker Script ID, in metadata annotation)
- Parameter type (if any)
- Return type (if any)

To list scripts:
1. Fetch `$metadata`.
2. Parse actions bound to the `Script` entity set.
3. Extract `ScriptID` annotations for FMSID values.

## Error handling

If a script fails (non-zero exit code), the response includes the error code:

```json
{
  "scriptResult": {
    "code": 101,
    "resultParameter": "Record is missing"
  }
}
```

Common script error codes follow FileMaker's standard error code list (e.g., `0` = success, `101` = record missing, `401` = no records found).

## Wrapper library guidance

Downstream libraries should:

1. Support all three scopes (database, entity-set, record).
2. Support both name-based and FMSID-based invocation (Claris 2026+).
3. Accept string, number, and JSON object parameters.
4. Parse the `scriptResult.code` and `scriptResult.resultParameter` from the response.
5. Expose script error codes as typed errors (e.g., `FMScriptError` with `code` and `resultParameter`).
6. Provide a method to list available scripts from `$metadata`.
7. Handle empty POST body correctly when no parameter is provided (some HTTP clients add a default `Content-Type` that breaks empty bodies).
