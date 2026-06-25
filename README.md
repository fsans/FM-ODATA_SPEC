# fms-odata-spec

A canonical base reference for the **Claris FileMaker Server OData API**, intended as the single source of truth that downstream libraries (MCP servers, JavaScript wrappers, and any future wrappers) conform to and evolve against.

## Purpose

This project provides a **unified source of conventions and a version-aware capability list** for the Claris FileMaker Server OData API. It serves as a common platform to unify FileMaker OData implementations across different languages, runtimes, and tool ecosystems.

The Claris OData API has evolved across server versions (19.x, 2023, 2024, 2026) with subtle behavioral differences, undocumented quirks, and version-gated features. Without a shared reference, each wrapper library independently discovers and works around the same issues, leading to divergent implementations and duplicated effort.

This repository solves that by providing:

1. **A single, documented contract** for what the FileMaker OData API does and does not support — so every wrapper implements the same behavior instead of guessing.
2. **A version-aware capability matrix** that maps FileMaker Server versions to supported features, query options, and endpoint availability — so wrappers can detect the server version and gate functionality accordingly.
3. **A propagation point for API changes** — when Claris releases a new FileMaker Server version, the update happens here first, then flows to every derived library.
4. **Three explicit categories of coverage**:
   - **Standard OData features** that FileMaker covers.
   - **Standard OData features** that FileMaker explicitly does *not* cover (so wrappers don't try to implement them).
   - **Non-OData additions** specific to FileMaker (containers, scripts, webhooks, custom `Prefer` headers, metadata annotations, system tables, etc.).

### Current downstream implementations

Three projects already consume this spec:

| Project | Type | Repository |
| ------- | ------ | ---------- |
| **fms-odata-mcp** | MCP server for AI agents (TypeScript) | <https://github.com/fsans/fms-odata-mcp> |
| **fms-odata-js** | JavaScript/TypeScript client library | <https://github.com/fsans/fms-odata-js> |
| **fms-odata-webhooks** | Webhook handler for FileMaker OData events | <https://github.com/fsans/fms-odata-webhooks> |

## What's in this repo

### Specification documents (`docs/`)

The primary deliverable. Read in order — each document builds on the previous:

| # | Document | Description |
| --- | ---------- | ------------- |
| 00 | [Overview](docs/00-overview.md) | Scope, purpose, version targeting |
| 01 | [Conformance](docs/01-conformance.md) | OData standard coverage matrix — what FMS supports and what it doesn't |
| 02 | [Endpoints](docs/02-endpoints.md) | Full endpoint reference (URL patterns, methods, status codes) |
| 03 | [Query Options](docs/03-query-options.md) | `$filter`, `$select`, `$orderby`, `$top`, `$skip`, `$expand`, `$count`, `$apply` |
| 04 | [Authentication](docs/04-authentication.md) | Basic auth, Claris ID (FMID), OAuth |
| 05 | [Metadata](docs/05-metadata.md) | `$metadata` document, annotations, system tables, version detection |
| 06 | [Scripts](docs/06-scripts.md) | Script execution, scopes, parameters, results |
| 07 | [Containers](docs/07-containers.md) | Container field binary/base64 upload and download |
| 08 | [Batch](docs/08-batch.md) | `$batch` requests, changesets, FMS quirks |
| 09 | [Webhooks](docs/09-webhooks.md) | Webhook creation and management |
| 10 | [Schema Modification](docs/10-schema-modification.md) | DDL: create/delete tables, fields, indexes |
| 11 | [Non-OData Additions](docs/11-non-odata-additions.md) | FileMaker-specific extensions beyond the OData standard |
| 12 | [Version Deltas](docs/12-version-deltas.md) | 19.x → 2023 → 2024 → 2026 → future, feature comparison matrix |
| 13 | [Quirks](docs/13-quirks.md) | Real-world quirks, bugs, and workarounds |
| 14 | [Reconciliation](docs/14-reconciliation.md) | Divergence matrix between the two downstream repos |

### Other contents

```text
schema/
  fms-odata-capabilities.json    # Machine-readable capability manifest (version feature matrix)
packages/
  fms-odata-spec-ts/             # Shared TypeScript types package (@fms-odata/spec-ts on npm)
    src/                        # Endpoint, query, auth, metadata, script, container, batch,
                               # webhook, schema, error, version type definitions
_research/                      # Gitignored: cloned source repos used as input
```

## Version targeting

The spec covers these FileMaker Server versions, with deltas documented in [docs/12-version-deltas.md](docs/12-version-deltas.md):

| Version | Codename | Status |
| --------- | ---------- | -------- |
| FileMaker 19.x | — | Baseline (OData API introduced) |
| Claris FileMaker 2023 | — | Documented deltas |
| Claris FileMaker 2024 | — | Documented deltas |
| Claris FileMaker 2026 | Current | Primary reference |
| Future / next | — | Reserved section for announced changes |

## Source of truth

The spec is built from:

1. **Official Claris OData API documentation** (<https://help.claris.com/en/odata-guide/>) — primary source.
2. **Observed behavior** from the two existing wrapper repositories (`fms-odata-mcp` and `fms-odata-js`) — real-world quirks, workarounds, and undocumented behaviors.

Where official docs and observed behavior diverge, both are documented and the discrepancy is noted.

## How downstream libraries use this

- **Read the docs** to understand what the API supports and what it doesn't.
- **Import the TypeScript types** from `packages/fms-odata-spec-ts` for shared type definitions (endpoint names, query option types, error codes, version feature flags).
- **Consume the JSON manifest** (`schema/fms-odata-capabilities.json`) to programmatically check feature availability per FileMaker Server version.
- **Follow the reconciliation matrix** (docs/14-reconciliation.md) when aligning divergent implementations.

## OData protocol version

FileMaker Server and FileMaker Cloud implement **OData 4.0** (advertised via `OData-Version: 4.0` and `OData-MaxVersion: 4.0` headers). The official docs reference the OData 4.01 specification for protocol conventions, but the implemented protocol version is 4.0. See [docs/01-conformance.md](docs/01-conformance.md) for the full conformance level and feature support matrix.

## Branching model

This repository uses a Git Flow-style workflow:

| Branch | Purpose |
|--------|---------|
| `main` | Stable releases only. Every commit on `main` is a merge from `develop` and is tagged with a version tag (`v1.0.0`, `v1.1.0`, etc.). |
| `develop` | Active development. All work lands here first via direct commits or feature branches merged back. |

**Workflow:**

1. Work on `develop` (or a feature branch off `develop`).
2. When a set of changes is ready for release, merge `develop` into `main`.
3. Tag the merge commit on `main` with an annotated version tag (`vMAJOR.MINOR.PATCH`).
4. Push both branches and the tag to `origin`.

**Tagging convention:**

- Tags follow semantic versioning: `vMAJOR.MINOR.PATCH`.
- Tags are annotated (`git tag -a`) with a summary of what changed.
- Tags are only created on `main`, never on `develop`.
- If the `@fms-odata/spec-ts` npm package version changes, the tag version should match the package version.

**Current tags:**

| Tag | Commit | Description |
|-----|--------|-------------|
| `v1.0.0` | `a8c7d9a` | Initial spec: 15 docs, JSON manifest, spec-ts types package |
| `v1.1.0` | `307389f` | Multi-strategy version detection aligned with fms-odata-mcp |
| `v1.1.1` | `b3b23ba` | Script result envelope fix + FMS v26 quirks |
| `v1.2.0` | `b72ab04` | Complete fm-odata -> fms-odata rename (package, directory, schema, all references) |

## License

MIT — see [LICENSE](LICENSE).
