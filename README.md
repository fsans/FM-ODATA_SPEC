# FM-ODATA_SPEC

A canonical base reference for the **Claris FileMaker Server OData API**, intended as the single source of truth that downstream libraries (MCP servers, JavaScript wrappers, and any future wrappers) conform to and evolve against.

## Purpose

Two existing projects had drifted apart in how they implement the FileMaker OData API:

| Project | Type | Repo |
|---------|------|------|
| **FMS-ODATA-MCP** | MCP server (TypeScript) | https://github.com/fsans/FMS-ODATA-MCP |
| **fm-odata-js** | JavaScript wrapper (TypeScript) | https://github.com/fsans/fm-odata-js |

This repository exists so that:

1. Both libraries (and any future ones) share a single, documented contract for what the FileMaker OData API does and does not support.
2. When Claris releases a new FileMaker Server version with OData changes, the update happens **here first**, then propagates to every derived library.
3. The spec explicitly captures three categories:
   - **Standard OData features** that FileMaker covers.
   - **Standard OData features** that FileMaker explicitly does *not* cover (so wrappers don't try to implement them).
   - **Non-OData additions** specific to FileMaker (containers, scripts, webhooks, custom `Prefer` headers, metadata annotations, system tables, etc.).

## What's in this repo

```
FM-ODATA_SPEC/
├── docs/                          # Human-readable spec (the primary deliverable)
│   ├── 00-overview.md             # Scope, purpose, version targeting
│   ├── 01-conformance.md          # OData standard coverage matrix
│   ├── 02-endpoints.md            # Full endpoint reference
│   ├── 03-query-options.md        # $filter, $select, $orderby, $top, $skip, $expand, $count, $apply
│   ├── 04-authentication.md       # Basic auth, Claris ID (FMID), OAuth
│   ├── 05-metadata.md             # $metadata, annotations, system tables, IDs
│   ├── 06-scripts.md              # Script execution, scopes, parameters, results
│   ├── 07-containers.md           # Container field binary/base64 upload/download
│   ├── 08-batch.md                # $batch requests, changesets, FMS quirks
│   ├── 09-webhooks.md             # Webhook creation/management
│   ├── 10-schema-modification.md  # DDL: create/delete tables, fields, indexes
│   ├── 11-non-odata-additions.md  # FileMaker-specific extensions
│   ├── 12-version-deltas.md       # 19.x -> 2023 -> 2024 -> 2026 -> future
│   ├── 13-quirks.md               # Real-world quirks & workarounds
│   └── 14-reconciliation.md       # Divergence matrix between the two existing repos
├── schema/
│   └── fm-odata-capabilities.json # Machine-readable capability manifest
├── packages/
│   └── fm-odata-spec-ts/          # Shared TypeScript types package
│       └── src/                   # Endpoint, query, auth, metadata, script, container, batch, webhook, schema, error, version types
└── _research/                     # Gitignored: cloned source repos used as input
```

## Version targeting

The spec covers these FileMaker Server versions, with deltas documented in [docs/12-version-deltas.md](docs/12-version-deltas.md):

| Version | Codename | Status |
|---------|----------|--------|
| FileMaker 19.x | — | Baseline (OData API introduced) |
| Claris FileMaker 2023 | — | Documented deltas |
| Claris FileMaker 2024 | — | Documented deltas |
| Claris FileMaker 2026 | Current | Primary reference |
| Future / next | — | Reserved section for announced changes |

## Source of truth

The spec is built from:

1. **Official Claris OData API documentation** (https://help.claris.com/en/odata-guide/) — primary source.
2. **Observed behavior** from the two existing wrapper repositories (`FMS-ODATA-MCP` and `fm-odata-js`) — real-world quirks, workarounds, and undocumented behaviors.

Where official docs and observed behavior diverge, both are documented and the discrepancy is noted.

## How downstream libraries use this

- **Read the docs** to understand what the API supports and what it doesn't.
- **Import the TypeScript types** from `packages/fm-odata-spec-ts` for shared type definitions (endpoint names, query option types, error codes, version feature flags).
- **Consume the JSON manifest** (`schema/fm-odata-capabilities.json`) to programmatically check feature availability per FileMaker Server version.
- **Follow the reconciliation matrix** (docs/14-reconciliation.md) when aligning divergent implementations.

## OData protocol version

FileMaker Server and FileMaker Cloud implement **OData 4.0** (advertised via `OData-Version: 4.0` and `OData-MaxVersion: 4.0` headers). The official docs reference the OData 4.01 specification for protocol conventions, but the implemented protocol version is 4.0. See [docs/01-conformance.md](docs/01-conformance.md) for the full conformance level and feature support matrix.

## License

MIT — see [LICENSE](LICENSE).
