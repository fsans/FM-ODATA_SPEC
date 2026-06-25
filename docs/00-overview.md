# 00 — Overview

## What this spec is

This is the **canonical base reference** for the Claris FileMaker Server OData API. It documents what the API supports, what it explicitly does not support, and the FileMaker-specific extensions that go beyond the OData standard.

It is not a tutorial, not a wrapper library, and not a runnable application. It is a contract that downstream libraries (MCP servers, JavaScript wrappers, Python clients, etc.) conform to and evolve against.

## Why it exists

Two existing wrapper projects had drifted apart in how they implement the same API:

- **fms-odata-mcp** — a TypeScript MCP server exposing FileMaker OData as tools for AI agents.
- **fms-odata-js** — a lightweight TypeScript client library for browsers, Node, and the FileMaker Web Viewer.

Both target the same FileMaker OData API, but they diverged in naming conventions, feature coverage, parameter handling, error models, and URL encoding. This spec provides a single source of truth so that:

1. Both libraries can realign on a shared contract.
2. Future FileMaker Server OData releases can be reflected in one place, then propagated to every derived library.
3. New wrappers can be built against a documented spec instead of reverse-engineering the API.

## Scope

### In scope

- The OData API exposed by FileMaker Server and FileMaker Cloud (URL prefix: `/fmi/odata/v4/`).
- Standard OData 4.0 features that FileMaker implements.
- Standard OData 4.0 features that FileMaker explicitly does *not* implement.
- FileMaker-specific extensions to OData (scripts, containers, webhooks, custom headers, metadata annotations, system tables, schema modification).
- Authentication mechanisms (HTTP Basic, Claris ID / FMID, OAuth identity providers).
- Version-specific differences across FileMaker 19.x, 2023, 2024, and 2026.
- Real-world quirks and undocumented behaviors observed in production.

### Out of scope

- The FileMaker Data API (a separate REST API at `/fmi/data/v1/`).
- The FileMaker Admin API (a separate REST API for server administration).
- ODBC/JDBC access to FileMaker data.
- The FileMaker WebDirect API.
- FileMaker Pro plug-in development.
- General OData protocol theory (see the [OData 4.01 specification](http://docs.oasis-open.org/odata/odata/v4.01/os/part1-protocol/odata-v4.01-os-part1-protocol.html) for that).

## OData protocol version

FileMaker Server and FileMaker Cloud implement **OData 4.0**. This is advertised via the `OData-Version: 4.0` and `OData-MaxVersion: 4.0` headers.

The official Claris documentation references the OData 4.01 specification for protocol conventions, but the implemented protocol version is 4.0. This spec uses "OData 4.0" when referring to the implemented version and "OData 4.01" when referring to the specification document that defines the conventions.

## URL structure

All OData API calls follow this pattern:

```
https://<host>/fmi/odata/v4/<database-name>/<resource>
```

| Component | Description |
|-----------|-------------|
| `host` | FileMaker Server or FileMaker Cloud host name |
| `fmi` | Fixed path segment |
| `odata` | Fixed path segment |
| `v4` | OData version segment (always `v4`) |
| `database-name` | Name of the hosted FileMaker database (omitted for the database-listing endpoint) |
| `resource` | Table name, system table, `$metadata`, `$batch`, `Script.<name>`, `Webhook.Add`, etc. |

### URL length limit

The maximum URL length is influenced by OS, web server, and browser differences. For cross-platform safety, limit URLs to **2,000 characters**.

### Encoding

- URL paths must use percent-encoding for special characters.
- Request body strings must use UTF-8 encoding.
- See [docs/13-quirks.md](13-quirks.md) for FileMaker-specific encoding quirks (commas, dollar signs, single quotes).

## Version targeting

This spec covers the following FileMaker Server versions:

| Version | Codename | OData introduced? | Status in this spec |
|---------|----------|-------------------|---------------------|
| FileMaker 19.x | — | Yes (introduced) | Baseline |
| Claris FileMaker 2023 | — | Yes | Deltas documented |
| Claris FileMaker 2024 | — | Yes | Deltas documented |
| Claris FileMaker 2026 | Current | Yes | Primary reference |
| Future / next | — | — | Reserved section |

Version-specific differences are documented in [docs/12-version-deltas.md](12-version-deltas.md).

## How to read this spec

The docs are numbered for reading order:

1. **01-conformance.md** — What OData standard features FileMaker does and does not support.
2. **02-endpoints.md** — Full endpoint reference (URL patterns, HTTP methods).
3. **03-query-options.md** — Query options ($filter, $select, $orderby, etc.).
4. **04-authentication.md** — Authentication mechanisms.
5. **05-metadata.md** — Metadata, annotations, system tables, IDs.
6. **06-scripts.md** — FileMaker script execution via OData.
7. **07-containers.md** — Container field binary/base64 upload and download.
8. **08-batch.md** — Batch requests and changesets.
9. **09-webhooks.md** — Webhook management.
10. **10-schema-modification.md** — DDL operations (create/delete tables, fields, indexes).
11. **11-non-odata-additions.md** — Summary of all FileMaker-specific extensions.
12. **12-version-deltas.md** — Version-by-version differences.
13. **13-quirks.md** — Real-world quirks and workarounds.
14. **14-reconciliation.md** — How the two existing wrapper repos diverge and how to reconcile them.

## Sources

- **Primary**: [Claris FileMaker OData API Guide](https://help.claris.com/en/odata-guide/content/index.html)
- **OData reference**: [OData 4.01 Protocol](http://docs.oasis-open.org/odata/odata/v4.01/os/part1-protocol/odata-v4.01-os-part1-protocol.html), [URL Conventions](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html), [CSDL](https://docs.oasis-open.org/odata/odata/v4.01/csprd01/part3-csdl/odata-v4.01-csprd01-part3-csdl.html), [JSON Format](https://docs.oasis-open.org/odata/odata-json-format/v4.01/odata-json-format-v4.01.html)
- **Observed behavior**: fms-odata-mcp and fms-odata-js repositories (see docs/14-reconciliation.md).
