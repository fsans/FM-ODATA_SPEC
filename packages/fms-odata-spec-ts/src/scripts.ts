/**
 * Script execution types for the FileMaker OData API.
 *
 * @see docs/06-scripts.md
 */

/** Script invocation scope. */
export type ScriptScope = 'database' | 'entitySet' | 'record';

/** Options for running a script. */
export interface ScriptOptions {
  /** Script parameter value (string, number, or JSON object). */
  parameter?: string | number | object;
  /** AbortSignal for cancellation. */
  signal?: AbortSignal;
}

/** Script identifier: either name or FMSID. */
export type ScriptIdentifier =
  | { type: 'name'; name: string }
  | { type: 'fmsid'; id: number };

/** Script result from the OData API. */
export interface ScriptResultEnvelope {
  scriptResult: {
    code: number;
    resultParameter?: string;
  };
}

/** Parsed script result. */
export interface ScriptResult {
  /** Exit Script code (0 = success). */
  code: number;
  /** Text result from Exit Script step. */
  resultParameter?: string;
  /** Raw response data. */
  raw: unknown;
}

/** Script descriptor from metadata. */
export interface ScriptDescriptor {
  name: string;
  fmsid?: string;
  isBound: boolean;
  parameterType?: string;
  returnType?: string;
}

/** Common FileMaker script error codes. */
export const SCRIPT_ERROR_CODES = {
  SUCCESS: 0,
  RECORD_MISSING: 101,
  NO_RECORDS_FOUND: 401,
  USER_CANCELED: 1,
  FILE_MISSING: 3,
  FILE_INACCESSIBLE: 4,
  PASSWORD_REQUIRED: 212,
} as const;

/** Build the URL path segment for a script invocation. */
export function scriptPathSegment(id: ScriptIdentifier): string {
  if (id.type === 'name') {
    return `Script.${id.name}`;
  }
  return `Script.FMSID:${id.id}`;
}

/** Build the request body for a script invocation. */
export function scriptRequestBody(options?: ScriptOptions): string | undefined {
  if (options?.parameter === undefined) {
    return undefined; // Empty body for no-parameter scripts
  }
  const param = options.parameter;
  return JSON.stringify({ scriptParameterValue: param });
}

/**
 * Parse the raw JSON response from a script invocation into a ScriptResult.
 *
 * FMS returns a nested envelope:
 * ```json
 * {"scriptResult": {"code": 0, "resultParameter": "Hello World"}}
 * ```
 *
 * This helper extracts `code` and `resultParameter` from the nested object.
 * A non-zero code indicates a script error.
 */
export function parseScriptResponse(raw: unknown): ScriptResult {
  if (raw === null || typeof raw !== 'object') {
    return { code: 0, raw };
  }

  const obj = raw as Record<string, unknown>;
  const scriptResult = obj.scriptResult;

  if (scriptResult !== null && typeof scriptResult === 'object') {
    const nested = scriptResult as { code?: unknown; resultParameter?: unknown };
    return {
      code: nested.code !== undefined ? Number(nested.code) : 0,
      resultParameter: nested.resultParameter !== undefined ? String(nested.resultParameter) : undefined,
      raw,
    };
  }

  // Fallback for older FMS versions that may use flat shape
  return {
    code: 0,
    raw,
  };
}
