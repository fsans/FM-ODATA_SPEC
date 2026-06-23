/**
 * @fms-odata/spec-ts — Shared TypeScript types for the FileMaker OData API specification.
 *
 * These types describe the FileMaker Server OData API surface as documented in
 * the fms-odata-spec repository (https://github.com/fsans/fms-odata-spec).
 * Downstream libraries (MCP servers, JS wrappers, etc.) should depend on this
 * package for shared type definitions.
 */

// Versions and feature flags
export * from './versions.js';

// Authentication
export * from './auth.js';

// Endpoints
export * from './endpoints.js';

// Query options
export * from './query-options.js';

// Metadata
export * from './metadata.js';

// Scripts
export * from './scripts.js';

// Containers
export * from './containers.js';

// Batch
export * from './batch.js';

// Webhooks
export * from './webhooks.js';

// Schema modification (DDL)
export * from './schema.js';

// Errors
export * from './errors.js';
