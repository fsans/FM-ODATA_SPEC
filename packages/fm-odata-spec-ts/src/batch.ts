/**
 * Batch request types for the FileMaker OData API.
 *
 * @see docs/08-batch.md
 */

/** Batch operation type. */
export type BatchOpType = 'list' | 'get' | 'create' | 'patch' | 'put' | 'delete';

/** A single operation in a batch request. */
export interface BatchOperation {
  /** Operation type. */
  op: BatchOpType;
  /** Entity set (table) name. */
  entitySet: string;
  /** Record key (for get, patch, put, delete). */
  key?: string | number;
  /** Request body (for create, patch, put). */
  body?: object;
  /** Query parameters (for list, get). */
  query?: Record<string, unknown>;
  /** Content-ID for referencing within changeset. */
  contentId?: number;
}

/** A changeset is a group of atomic write operations. */
export interface Changeset {
  operations: BatchOperation[];
}

/** A batch request consists of retrieve operations and changesets. */
export interface BatchRequest {
  /** Retrieve operations (GET) — executed outside changesets. */
  retrieveOps: BatchOperation[];
  /** Changesets (atomic write groups). */
  changesets: Changeset[];
}

/** Result of a single batch operation. */
export interface BatchOpResult<T = unknown> {
  status: number;
  body?: T;
  headers: Record<string, string>;
  ok: boolean;
  /** Content-ID if specified in the request. */
  contentId?: number;
}

/** Overall batch result. */
export interface BatchResult {
  responses: BatchOpResult[];
  ok: boolean;
}

/** Handle for tracking a queued operation's result. */
export interface BatchHandle<T = unknown> {
  /** Resolves when the batch is sent and this operation's result is available. */
  promise: Promise<BatchOpResult<T>>;
}

/**
 * Generate a unique boundary string for multipart MIME.
 * Uses crypto.randomUUID if available, otherwise a random string.
 */
export function generateBoundary(prefix: string = 'batch'): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return `${prefix}_${crypto.randomUUID()}`;
  }
  return `${prefix}_${Date.now()}-${Math.random().toString(36).slice(2)}`;
}
