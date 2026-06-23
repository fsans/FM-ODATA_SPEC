# 14 — Reconciliation Matrix

This document maps the divergence between the two existing wrapper repositories and provides recommendations for aligning them on this shared spec.

## Repositories

| Repository | Type | Language | Package | Version analyzed |
|------------|------|----------|---------|------------------|
| [FMS-ODATA-MCP](https://github.com/fsans/FMS-ODATA-MCP) | MCP server | TypeScript | `filemaker-odata-mcp` | 0.8.2 |
| [fm-odata-js](https://github.com/fsans/fm-odata-js) | JS wrapper | TypeScript | `fm-odata-js` | 0.1.6 |

## Architectural comparison

| Aspect | FMS-ODATA-MCP | fm-odata-js |
|--------|---------------|-------------|
| Purpose | MCP server for AI agents | Direct client library |
| Deployment | Standalone service (stdio/http/https) | Embedded in application |
| API style | Tool-based (RPC) | Fluent/builder pattern |
| Bundle size | ~500 KB (with deps) | ~7.9 KB gzipped (zero deps) |
| Runtime deps | axios, express, commander, dotenv, debug | None |
| Async model | Promise-based | Promise-based |
| Error handling | MCP content array with `isError` | Typed exceptions (`FMODataError`, `FMScriptError`) |
| Session model | Multi-session with aliases | Single client per instance |
| Transport | stdio, HTTP, HTTPS | Direct fetch/HTTP |
| Target environments | Node 18+ | Node 18+, browsers, FileMaker Web Viewer |

## Naming comparison

| Concept | FMS-ODATA-MCP | fm-odata-js | Spec recommendation |
|---------|---------------|-------------|---------------------|
| Main client class | `ODataClient` | `FMOData` | `FMOData` |
| Query builder | Tool parameters (string-based) | `Query<T>` (fluent) | Fluent builder |
| Single record | Tool parameters | `EntityRef<T>` | Entity reference class |
| Script invocation | `fm_odata_run_script` tool | `ScriptInvoker` class | Script runner class |
| Container I/O | Not exposed | `ContainerRef` class | Container reference class |
| Batch operations | Not exposed | `Batch` / `Changeset` classes | Batch builder classes |
| Metadata | `fm_odata_get_metadata` tool | `MetadataFetcher` class | Metadata fetcher class |
| Error type | MCP content + `isError` | `FMODataError` exception | Typed exception |
| Script error | MCP content | `FMScriptError` exception | Typed exception |

## Feature coverage matrix

| Feature | FMS-ODATA-MCP | fm-odata-js | Spec requires |
|---------|---------------|-------------|---------------|
| Query records | Yes | Yes | Yes |
| Get single record | Yes | Yes | Yes |
| Count records | Yes (`?$count=true&$top=0`) | Yes (`?$count=true`) | Yes |
| Create record | Yes | Yes | Yes |
| Update record | Yes (PATCH) | Yes (PATCH) | Yes |
| Delete record | Yes | Yes | Yes |
| `$filter` | Yes (string) | Yes (fluent + string) | Yes |
| `$select` | Yes | Yes | Yes |
| `$orderby` | Yes | Yes | Yes |
| `$top` / `$skip` | Yes | Yes | Yes |
| `$expand` | Yes | Yes | Yes |
| `$count` | Yes (inline only) | Yes (inline only) | Yes (inline only) |
| `$apply` (aggregation) | Yes (v22.0.1+) | No | Yes (version-gated) |
| Type casting | Yes (v21.1+) | No | Optional (version-gated) |
| Parameterized filters | Yes (v21.1+) | No | Optional (version-gated) |
| Scripts (by name) | Yes | Yes | Yes |
| Scripts (by FMSID) | Yes (v26+) | No | Yes (version-gated) |
| List scripts | Yes (v26+) | No (parse metadata) | Yes |
| Container upload (binary) | No | Yes | Yes |
| Container upload (base64) | No | Yes | Yes |
| Container download | No | Yes | Yes |
| Batch (`$batch`) | No | Yes | Yes |
| Metadata fetch | Yes | Yes | Yes |
| Metadata parsing | Yes (XML) | Yes (regex-based) | Yes |
| Metadata annotations | Yes (v26+) | Partial | Yes |
| Schema editing (DDL) | Yes (opt-in) | No | Optional (opt-in) |
| Webhooks | No | No | Optional |
| Record references (`$ref`) | No | No | Yes |
| Cross-join | No | No | Yes |
| Version detection | Yes | No | Yes |
| Multi-session | Yes | No | Optional |
| Connection persistence | Yes (config file) | No | Optional |
| URL encoding quirks | Handled | Handled | Must handle |
| Auth: Basic | Yes | Yes | Yes |
| Auth: FMID | No (Server only) | Yes (via token provider) | Yes |
| Auth: 401 retry | No | Yes (`onUnauthorized`) | Recommended |
| TLS verification toggle | Yes | No (env var) | Yes |

## Gap analysis

### Gaps in FMS-ODATA-MCP (vs spec)

| Missing feature | Priority | Notes |
|-----------------|----------|-------|
| Container upload/download | High | MCP can use base64 method (binary not suitable for JSON-RPC) |
| Batch requests | Medium | Useful for atomic multi-operation; add as MCP tool |
| Record references (`$ref`) | Medium | Standard OData feature |
| Cross-join | Low | Niche feature |
| FMID auth (FileMaker Cloud) | High | Currently Server-only; needed for Cloud support |
| 401 retry / token refresh | Medium | Important for FileMaker Cloud token expiry |
| Webhooks | Low | Niche feature; can add as MCP tools |

### Gaps in fm-odata-js (vs spec)

| Missing feature | Priority | Notes |
|-----------------|----------|-------|
| `$apply` (aggregation) | Medium | Supported in FMS 22.0.1+; add to query builder |
| Version detection | High | Needed for feature gating |
| Feature gating | Medium | Currently all features available regardless of server version |
| Schema editing (DDL) | Low | Optional; can add as separate module |
| Scripts by FMSID | Medium | Supported in FMS 26+; add for stable integrations |
| List scripts from metadata | Low | Can parse from existing metadata fetch |
| Type casting in filters | Low | Niche feature |
| Parameterized filters | Low | Niche feature |
| Record references (`$ref`) | Medium | Standard OData feature |
| Webhooks | Low | Niche feature; can add as separate module |
| Multi-session | Low | Different use case; not critical for embedded library |

## Reconciliation recommendations

### 1. Adopt `FMOData` as canonical client class name

Both repos should use `FMOData` as the primary class name. It's concise, signals FileMaker-specific behavior, and aligns with the npm package naming convention.

### 2. Adopt fluent builder pattern for queries

The fluent builder pattern from `fm-odata-js` (`Query<T>`) is more ergonomic and type-safe than string-based parameters. The MCP server can internally use a fluent builder and serialize to URL strings for transport.

### 3. Adopt typed exceptions for errors

`FMODataError` and `FMScriptError` from `fm-odata-js` should be the canonical error types. The MCP server can catch these and convert to MCP content arrays for transport, while internally using typed exceptions.

### 4. Share URL encoding logic

Both repos implement the same URL encoding quirks (commas, dollar signs, single quotes). This logic should be extracted into a shared module (part of `@fms-odata/spec-ts` or a separate `@fms-odata/shared` package).

### 5. Standardize environment variable names

| Variable | Purpose | Both repos should use |
|----------|---------|----------------------|
| `FM_SERVER` | Server host URL | Yes |
| `FM_DATABASE` | Default database name | Yes |
| `FM_USER` | Account name | Yes |
| `FM_PASSWORD` | Account password | Yes |
| `FM_VERIFY_SSL` | TLS verification | Yes |
| `FM_TIMEOUT` | Request timeout (ms) | Yes |

### 6. Expose container I/O in both repos

- **fm-odata-js**: Already has `ContainerRef` — no change needed.
- **FMS-ODATA-MCP**: Add `fm_odata_container_upload` and `fm_odata_container_download` tools using the base64 method (binary is not suitable for JSON-RPC transport).

### 7. Expose batch operations in both repos

- **fm-odata-js**: Already has `Batch` / `Changeset` — no change needed.
- **FMS-ODATA-MCP**: Add `fm_odata_batch` tool that accepts a JSON array of operations and constructs the multipart MIME internally.

### 8. Standardize version detection

Both repos should:
- Lazily parse `$metadata` on first call.
- Cache the version per session.
- Expose a feature compatibility matrix.
- Gate version-specific features with graceful fallback (warnings, not errors) on older servers.

### 9. Standardize auth handling

Both repos should:
- Support Basic auth (Server) and FMID token (Cloud).
- Accept auth as a static string or async function (for token refresh).
- Auto-detect the auth scheme from the token format.
- Handle 401 responses with a retry/refresh callback.

### 10. Align on spec as source of truth

Both repos should:
- Reference this spec in their README and documentation.
- Import shared types from `@fms-odata/spec-ts`.
- Consume `schema/fms-odata-capabilities.json` for feature availability checks.
- Update their implementations when the spec is updated for new FileMaker Server versions.

## Migration path

### Phase 1: Align on types and encoding (low risk)

1. Both repos import `@fms-odata/spec-ts` for shared type definitions.
2. Both repos use the shared URL encoding module.
3. Both repos standardize environment variable names.

### Phase 2: Align on API surface (medium risk)

1. fm-odata-js adopts `FMOData` class name (if not already).
2. FMS-ODATA-MCP adds container I/O (base64) and batch tools.
3. fm-odata-js adds version detection and feature gating.
4. Both repos adopt typed exceptions internally.

### Phase 3: Align on advanced features (higher risk)

1. fm-odata-js adds `$apply` aggregation support.
2. fm-odata-js adds FMSID-based script invocation.
3. FMS-ODATA-MCP adds FMID auth support.
4. Both repos add record references (`$ref`) and cross-join support.

### Phase 4: Ongoing sync

1. When Claris releases a new FileMaker Server version, update this spec first.
2. Both repos consume the updated spec and types.
3. Both repos implement new features following the spec's guidance.
