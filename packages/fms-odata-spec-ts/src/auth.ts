/**
 * Authentication types for the FileMaker OData API.
 *
 * @see docs/04-authentication.md
 */

/** Authentication scheme supported by FileMaker OData. */
export type FMAuthScheme = 'Basic' | 'FMID';

/** Static auth token string (e.g., "Basic dXNlcjpwYXNz" or "FMID <token>"). */
export type FMAuthToken = string;

/**
 * Token provider function. Returns the auth header value.
 * Can be async to support token refresh (e.g., Claris ID token expiry).
 */
export type FMAuthTokenProvider = () => string | Promise<string>;

/** Configuration for Basic auth (FileMaker Server on-premise). */
export interface FMBasicAuthConfig {
  scheme: 'Basic';
  account: string;
  password: string;
}

/** Configuration for FMID auth (FileMaker Cloud). */
export interface FMIDAuthConfig {
  scheme: 'FMID';
  token: string;
  /** Optional refresh callback invoked on 401 responses. */
  onUnauthorized?: () => Promise<string>;
}

/** Union of auth configurations. */
export type FMAuthConfig = FMBasicAuthConfig | FMIDAuthConfig;

/** Standard auth-related headers. */
export interface FMAuthHeaders {
  Authorization: string;
  'OData-Version'?: '4.0';
  'OData-MaxVersion'?: '4.0';
}

/** Build a Basic auth header value from account and password. */
export function basicAuth(account: string, password: string): string {
  const raw = `${account}:${password}`;
  // Works in both Node (Buffer) and browsers (btoa)
  if (typeof Buffer !== 'undefined') {
    return `Basic ${Buffer.from(raw).toString('base64')}`;
  }
  return `Basic ${btoa(raw)}`;
}

/** Build an FMID auth header value from a Claris ID token. */
export function fmidAuth(token: string): string {
  return `FMID ${token}`;
}

/** Normalize a token string: if it already has a scheme prefix, use as-is. */
export function normalizeAuthToken(token: string): string {
  if (token.startsWith('Basic ') || token.startsWith('FMID ') || token.startsWith('Bearer ')) {
    return token;
  }
  // Default to Bearer for bare tokens (callers should use basicAuth() or fmidAuth() helpers)
  return `Bearer ${token}`;
}
