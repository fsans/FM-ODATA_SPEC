/**
 * Webhook types for the FileMaker OData API.
 *
 * @see docs/09-webhooks.md
 */

/** Parameters for creating a webhook. */
export interface WebhookCreateParams {
  /** URL to receive webhook POST payloads. Required. */
  webhook: string;
  /** Table to monitor for changes. Required. */
  tableName: string;
  /** Headers sent to the endpoint URL (does not affect processing). */
  endpointHeaders?: Record<string, string>;
  /** Legacy alias for endpointHeaders. */
  headers?: Record<string, string>;
  /** Headers controlling how the webhook payload is generated. */
  queryHeaders?: Record<string, string>;
  /** Whether to notify on schema changes. Default: false. */
  notifySchemaChanges?: boolean;
  /** Comma-separated field list to include in payload. Default: "". */
  select?: string;
  /** OData filter expression; only matching records trigger webhook. Default: "". */
  filter?: string;
  /** Max retry attempts (0 = infinite). Default: 0. */
  maxFailedAttempts?: number;
}

/** Webhook data returned by Webhook.Get / Webhook.GetAll. */
export interface WebhookData {
  id?: string;
  webhook: string;
  tableName: string;
  endpointHeaders?: Record<string, string>;
  queryHeaders?: Record<string, string>;
  notifySchemaChanges?: boolean;
  select?: string;
  filter?: string;
  maxFailedAttempts?: number;
}

/** Webhook operation types. */
export type WebhookOperation = 'Add' | 'Remove' | 'Get' | 'GetAll' | 'Invoke';

/** Build the URL path for a webhook operation. */
export function webhookPath(database: string, operation: WebhookOperation): string {
  return `/${database}/Webhook.${operation}`;
}
