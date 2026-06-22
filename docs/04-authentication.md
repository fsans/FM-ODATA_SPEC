# 04 — Authentication

The FileMaker OData API requires authentication on every request via the `Authorization` header. The mechanism differs between FileMaker Server (on-premise) and FileMaker Cloud.

## FileMaker Server (on-premise)

### Mechanism: HTTP Basic Auth

FileMaker Server uses standard HTTP Basic authentication with a FileMaker file account (account name + password defined in the hosted database).

### Header format

```
Authorization: Basic <base64(account:password)>
```

For example, with account `admin` and password `admin`:
- Raw: `admin:admin`
- Base64: `YWRtaW46YWRtaW4=`
- Header: `Authorization: Basic YWRtaW46YWRtaW4=`

### Notes

- The account must have the `fmproExtended` (or equivalent OData) extended privilege enabled in the FileMaker file.
- Credentials are sent on every request — there is no session token or login/logout flow.
- HTTPS is required (OData does not accept plain HTTP connections).
- Self-signed certificates are common in LAN deployments; clients must handle TLS verification accordingly.

## FileMaker Cloud

### Mechanism: Claris ID (FMID) token

FileMaker Cloud uses Claris ID for external authentication. You must first generate a Claris ID token, then include it in the `Authorization` header.

### Header format

```
Authorization: FMID <Claris_ID_Token>
```

### Token lifecycle

1. Authenticate with Claris ID account (via Claris Customer Console or API).
2. Retrieve the session token.
3. Include the token in the `Authorization: FMID <token>` header for all OData calls.
4. Tokens are valid for **1 hour**.
5. After expiry, API calls fail with HTTP 401. Re-authenticate to get a new token.

### Notes

- The `FMID` scheme is FileMaker-specific (not a standard HTTP auth scheme).
- Token refresh is the client's responsibility — the OData API does not auto-refresh.
- HTTPS is required.

## OAuth identity provider (FileMaker Cloud)

FileMaker Cloud supports logging in to a database session using an OAuth identity provider (e.g., Google, Microsoft, Amazon).

### Flow

1. Obtain an OAuth token from the identity provider.
2. Use the OAuth token to authenticate to the FileMaker database session.
3. Include the resulting session token in OData calls.

See the official Claris documentation for the current list of supported OAuth providers and the exact flow.

## Authentication comparison

| Property | FileMaker Server | FileMaker Cloud |
|----------|-----------------|-----------------|
| Auth scheme | HTTP Basic | FMID (Claris ID) |
| Credentials | FileMaker file account | Claris ID account |
| Token expiry | No (stateless) | 1 hour |
| Refresh needed | No | Yes (client responsibility) |
| HTTPS required | Yes | Yes |
| Header format | `Authorization: Basic <base64>` | `Authorization: FMID <token>` |

## Required headers for all requests

Regardless of auth mechanism, these headers should be included:

| Header | Value | Required? |
|--------|-------|-----------|
| `Authorization` | `Basic <base64>` or `FMID <token>` | Yes |
| `OData-Version` | `4.0` | Recommended |
| `OData-MaxVersion` | `4.0` | Recommended |
| `Accept` | `application/json` (default), `application/atom+xml`, or `text/html` | Optional |
| `Content-Type` | `application/json` (for POST/PATCH/PUT) | Required for write operations |

### Note on OData-Version headers

The OData specification mandates `OData-Version` and `OData-MaxVersion` headers. In practice, FileMaker Server 2026 accepts requests without them, but they should be sent per spec for correctness and forward compatibility.

## What does NOT work

- **FileMaker Data API bearer tokens**: The Data API (`/fmi/data/v1/`) uses a different auth flow (POST to `/auth` to get a bearer token). That token does **not** work with the OData API. OData requires Basic auth (Server) or FMID (Cloud).
- **Session cookies**: OData is stateless — there are no session cookies to maintain.
- **API keys**: There is no API key mechanism in the OData API.

## Wrapper library guidance

Downstream libraries should:

1. Support both Basic auth (Server) and FMID token (Cloud) auth schemes.
2. Allow the auth token to be provided as either a static string or a function (for token refresh).
3. Auto-detect the auth scheme from the token format (if it starts with `Basic ` or `FMID `, use as-is; otherwise prepend the appropriate scheme).
4. Handle 401 responses with a retry/refresh callback for FileMaker Cloud token expiry.
5. Never log or expose credentials in error messages.
6. Support configurable TLS verification (for self-signed certificates in development).
