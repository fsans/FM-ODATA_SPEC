/**
 * Endpoint definitions for the FileMaker OData API.
 *
 * @see docs/02-endpoints.md
 */

import type { FMVersionMajor } from './versions.js';

/** HTTP methods used by the OData API. */
export type HttpMethod = 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE';

/** Endpoint category. */
export type EndpointCategory =
  | 'discovery'
  | 'metadata'
  | 'query'
  | 'crud'
  | 'batch'
  | 'scripts'
  | 'containers'
  | 'schema'
  | 'webhooks';

/** Endpoint descriptor. */
export interface FMEndpoint {
  /** Endpoint identifier (e.g., "getRecords", "runScript"). */
  id: string;
  /** HTTP method. */
  method: HttpMethod;
  /** URL path template relative to /fmi/odata/v4. Use {param} for path params. */
  path: string;
  /** Human-readable description. */
  description: string;
  /** Minimum FileMaker Server version that supports this endpoint. */
  minVersion: FMVersionMajor;
  /** Additional HTTP methods that also work for this endpoint. */
  alsoMethods?: HttpMethod[];
  /** Content-Type required for the request body. */
  contentType?: string;
  /** Query options supported by this endpoint. */
  queryOptions?: string[];
  /** Endpoint category. */
  category: EndpointCategory;
}

/** All OData API endpoints. */
export const FM_ENDPOINTS: FMEndpoint[] = [
  // Discovery & metadata
  { id: 'getDatabases', method: 'GET', path: '/', description: 'List all hosted databases', minVersion: '19', category: 'discovery' },
  { id: 'getTables', method: 'GET', path: '/{database}', description: 'List tables in a database', minVersion: '19', category: 'discovery' },
  { id: 'getSystemTable', method: 'GET', path: '/{database}/{systemTable}', description: 'Get system table values', minVersion: '19', category: 'discovery' },
  { id: 'getMetadata', method: 'GET', path: '/{database}/$metadata', description: 'Get CSDL/EDMX metadata', minVersion: '19', category: 'metadata' },

  // Query
  { id: 'getRecords', method: 'GET', path: '/{database}/{table}', description: 'Query records from a table', minVersion: '19', category: 'query', queryOptions: ['$filter', '$select', '$orderby', '$top', '$skip', '$expand', '$count', '$apply'] },
  { id: 'getRecord', method: 'GET', path: '/{database}/{table}({key})', description: 'Get a single record', minVersion: '19', category: 'query', queryOptions: ['$select'] },
  { id: 'getFieldValue', method: 'GET', path: '/{database}/{table}({key})/{field}', description: 'Get a single field value', minVersion: '19', category: 'query' },
  { id: 'getBinaryFieldValue', method: 'GET', path: '/{database}/{table}({key})/{field}/$value', description: 'Get binary value of a container field', minVersion: '19', category: 'query' },
  { id: 'navigateRelated', method: 'GET', path: '/{database}/{table}({key})/{relatedTable}', description: 'Navigate to related table records', minVersion: '19', category: 'query', queryOptions: ['$expand', '$select'] },

  // CRUD
  { id: 'createRecord', method: 'POST', path: '/{database}/{table}', description: 'Create a new record', minVersion: '19', category: 'crud', contentType: 'application/json', alsoMethods: ['PUT'] },
  { id: 'updateRecord', method: 'PATCH', path: '/{database}/{table}({key})', description: 'Update a record', minVersion: '19', category: 'crud', contentType: 'application/json', alsoMethods: ['PUT'] },
  { id: 'deleteRecord', method: 'DELETE', path: '/{database}/{table}({key})', description: 'Delete a record', minVersion: '19', category: 'crud' },
  { id: 'updateRecordRef', method: 'POST', path: '/{database}/{table}({key})/{relatedTable}/$ref', description: 'Add/replace a record reference', minVersion: '19', category: 'crud', contentType: 'application/json', alsoMethods: ['PATCH', 'PUT', 'DELETE'] },

  // Batch
  { id: 'batch', method: 'POST', path: '/{database}/$batch', description: 'Perform batch operations', minVersion: '19', category: 'batch', contentType: 'multipart/mixed' },

  // Scripts
  { id: 'runScript', method: 'POST', path: '/{database}/Script.{scriptName}', description: 'Run a FileMaker script by name', minVersion: '19', category: 'scripts', contentType: 'application/json' },
  { id: 'runScriptById', method: 'POST', path: '/{database}/Script.FMSID:{scriptId}', description: 'Run a FileMaker script by FMSID', minVersion: '26', category: 'scripts', contentType: 'application/json' },

  // Containers
  { id: 'updateContainerBinary', method: 'PATCH', path: '/{database}/{table}({key})/{containerField}', description: 'Update a container field with binary data', minVersion: '19', category: 'containers' },
  { id: 'updateContainerBase64', method: 'PATCH', path: '/{database}/{table}({key})', description: 'Update container fields with base64-encoded data', minVersion: '19', category: 'containers', contentType: 'application/json', alsoMethods: ['PUT'] },

  // Schema
  { id: 'createTable', method: 'POST', path: '/{database}/FileMaker_Tables', description: 'Create a new table', minVersion: '19', category: 'schema', contentType: 'application/json' },
  { id: 'addFields', method: 'PATCH', path: "/{database}/FileMaker_Tables('{tableName}')", description: 'Add fields to a table', minVersion: '19', category: 'schema', contentType: 'application/json', alsoMethods: ['PUT'] },
  { id: 'deleteTable', method: 'DELETE', path: "/{database}/FileMaker_Tables('{tableName}')", description: 'Delete a table', minVersion: '19', category: 'schema' },
  { id: 'deleteField', method: 'DELETE', path: "/{database}/FileMaker_Tables('{tableName}')/{fieldName}", description: 'Delete a field from a table', minVersion: '19', category: 'schema' },
  { id: 'createIndex', method: 'POST', path: '/{database}/FileMaker_Indexes', description: 'Create a field index', minVersion: '19', category: 'schema', contentType: 'application/json' },
  { id: 'deleteIndex', method: 'DELETE', path: "/{database}/FileMaker_Indexes('{indexName}')", description: 'Delete an index', minVersion: '19', category: 'schema' },

  // Webhooks
  { id: 'createWebhook', method: 'POST', path: '/{database}/Webhook.Add', description: 'Create a webhook', minVersion: '21', category: 'webhooks', contentType: 'application/json' },
  { id: 'deleteWebhook', method: 'POST', path: '/{database}/Webhook.Remove', description: 'Delete a webhook', minVersion: '21', category: 'webhooks', contentType: 'application/json' },
  { id: 'getWebhook', method: 'POST', path: '/{database}/Webhook.Get', description: 'Get specified webhook data', minVersion: '21', category: 'webhooks', contentType: 'application/json' },
  { id: 'getAllWebhooks', method: 'POST', path: '/{database}/Webhook.GetAll', description: 'Get all webhooks', minVersion: '21', category: 'webhooks', contentType: 'application/json' },
  { id: 'invokeWebhook', method: 'POST', path: '/{database}/Webhook.Invoke', description: 'Manually invoke a webhook', minVersion: '21', category: 'webhooks', contentType: 'application/json' },
];

/** Find an endpoint by ID. */
export function getEndpoint(id: string): FMEndpoint | undefined {
  return FM_ENDPOINTS.find((e) => e.id === id);
}

/** Get all endpoints available in a given version. */
export function getEndpointsForVersion(version: FMVersionMajor): FMEndpoint[] {
  const order: FMVersionMajor[] = ['19', '21', '22', '26'];
  const idx = order.indexOf(version);
  if (idx === -1) return FM_ENDPOINTS; // future = all
  return FM_ENDPOINTS.filter((e) => order.indexOf(e.minVersion) <= idx);
}
