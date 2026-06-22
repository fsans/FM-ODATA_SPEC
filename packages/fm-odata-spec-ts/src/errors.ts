/**
 * Error types for the FileMaker OData API.
 *
 * @see docs/13-quirks.md (for real-world error behaviors)
 */

/** Base error class for all FileMaker OData errors. */
export class FMODataError extends Error {
  /** HTTP status code. */
  readonly status: number;
  /** OData error code (if available). */
  readonly code?: string;
  /** OData error object (if available in response body). */
  readonly odataError?: ODataErrorBody;
  /** The request that caused the error. */
  readonly request?: { method: string; url: string };

  constructor(
    message: string,
    options: {
      status: number;
      code?: string;
      odataError?: ODataErrorBody;
      request?: { method: string; url: string };
    },
  ) {
    super(message);
    this.name = 'FMODataError';
    this.status = options.status;
    this.code = options.code;
    this.odataError = options.odataError;
    this.request = options.request;
  }
}

/** Error thrown when a FileMaker script returns a non-zero exit code. */
export class FMScriptError extends FMODataError {
  /** Script error code (from scriptResult.code). */
  readonly scriptError: number;
  /** Script result parameter (from scriptResult.resultParameter). */
  readonly scriptResult?: string;

  constructor(
    message: string,
    options: {
      scriptError: number;
      scriptResult?: string;
      request?: { method: string; url: string };
    },
  ) {
    super(message, {
      status: 200, // Script errors return HTTP 200 with error in body
      code: String(options.scriptError),
      request: options.request,
    });
    this.name = 'FMScriptError';
    this.scriptError = options.scriptError;
    this.scriptResult = options.scriptResult;
  }
}

/** OData standard error response body. */
export interface ODataErrorBody {
  error: {
    code: string;
    message: string;
    target?: string;
    details?: Array<{
      code: string;
      message: string;
      target?: string;
    }>;
    innererror?: {
      type: string;
      message: string;
    };
  };
}

/** Authentication error (HTTP 401). */
export class FMAuthError extends FMODataError {
  constructor(message: string, request?: { method: string; url: string }) {
    super(message, { status: 401, request });
    this.name = 'FMAuthError';
  }
}

/** Not found error (HTTP 404). */
export class FMNotFoundError extends FMODataError {
  constructor(message: string, request?: { method: string; url: string }) {
    super(message, { status: 404, request });
    this.name = 'FMNotFoundError';
  }
}

/** Validation error (HTTP 400). */
export class FMValidationError extends FMODataError {
  constructor(message: string, odataError?: ODataErrorBody, request?: { method: string; url: string }) {
    super(message, { status: 400, odataError, request });
    this.name = 'FMValidationError';
  }
}

/** Check if an error is a FileMaker OData error. */
export function isFMODataError(err: unknown): err is FMODataError {
  return err instanceof FMODataError;
}

/** Check if an error is a FileMaker script error. */
export function isFMScriptError(err: unknown): err is FMScriptError {
  return err instanceof FMScriptError;
}
