# fms-odata-spec (Python)

Python types and spec definitions for the **Claris FileMaker Server OData API**.

This is the Python companion to [`@fms-odata/spec-ts`](https://www.npmjs.com/package/@fms-odata/spec-ts).
Both packages mirror the same specification (defined in the
[fms-odata-spec](https://github.com/fsans/fms-odata-spec) repository) and are
published independently — pick the one matching your runtime. The Python
package has **no runtime dependency** on the TypeScript package (or vice versa).

## What's in the box

- Version identifiers and a feature-flag matrix for FileMaker Server 19.x,
  2023, 2024, and 2026 (`versions`).
- Authentication helpers and config types for Basic and Claris ID (FMID) auth
  (`auth`).
- Endpoint descriptors and version-scoped lookup helpers (`endpoints`).
- OData query-option types and literal-formatting helpers (`query_options`).
- `$metadata` parsing helpers and EDM model types (`metadata`).
- Script execution types and response parsing (`scripts`).
- Container field upload/download helpers and MIME sniffing (`containers`).
- `$batch` request and result types (`batch`).
- Webhook management types (`webhooks`).
- Schema modification (DDL) types and field-type parsing (`schema`).
- Error class hierarchy for OData responses (`errors`).

All models are stdlib `dataclasses` (no pydantic / no validation framework).
Discriminated unions from the TS spec are modeled with `typing.Literal`
discriminator fields. The package ships a `py.typed` marker (PEP 561) so
static type checkers pick up the annotations.

## Install

```bash
pip install fms-odata-spec
```

For local development from this repository:

```bash
cd packages/fms-odata-spec-py
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## Usage

```python
from fms_odata_spec import (
    FM_VERSION_MATRIX,
    has_feature,
    basic_auth,
    parse_server_version,
    format_literal,
    FMODataError,
)

# Check feature availability per FileMaker Server version.
# Feature names are snake_case (matching the FMFeatureFlags dataclass fields).
assert has_feature("26", "scripts_by_fmsid") is True
assert has_feature("19", "webhooks") is False

# Build a Basic auth header value.
hdr = basic_auth("admin", "secret")  # -> "Basic YWRtaW46c2VjcmV0"

# Detect the server version from a $metadata XML payload.
ver = parse_server_version(
    '<Annotation Term="Org.OData.Core.V1.ProductVersion" String="26.0.1.500"/>'
)
assert ver.major == 26

# Format an OData $filter literal.
assert format_literal("O'Brien") == "'O''Brien'"
assert format_literal(42) == "42"
```

## Versioning

This package is versioned independently of `@fms-odata/spec-ts` and starts at
`0.1.0`. It is published to [PyPI](https://pypi.org/project/fms-odata-spec/) as
`fms-odata-spec`.

## Roadmap to a real v0.1.0 release

> **IMPORTANT — these items must be addressed before publishing 0.1.0 to PyPI.**
> See `AGENTS.md` at the repository root for the same list with more detail.

- [ ] **PyPI publishing workflow** — `.github/workflows/py-publish.yml` exists
      and triggers on `py-v*` tag pushes. Remaining: create a PyPI API token,
      add it as the `PYPI_API_TOKEN` repo secret, optionally create a `pypi`
      environment for protection rules, then re-push the tag to trigger. See
      `AGENTS.md` for full steps.
- [x] **LICENSE bundling** — DONE. `LICENSE` is copied into this directory
      and declared as a wheel artifact + sdist include in `pyproject.toml`;
      verified it ships in both the wheel and sdist.
- [ ] **CHANGELOG** — add `CHANGELOG.md` with the 0.1.0 entry.
- [ ] **`ODataEntity[T]` ergonomics** — confirm the wrapping-dataclass shape
      (`envelope.entity.field`) is acceptable before the first release; it is a
      breaking change to alter afterwards.
- [ ] **CI matrix** — add Python 3.14 to `py-ci.yml` once
      `actions/setup-python` supports it.
- [ ] **Async token-refresh** — document that `FMIDAuthConfig.on_unauthorized`
      is typed but not invoked by this package (downstream must wire it).
- [ ] **Shared schema source** — revisit whether both language packages should
      be generated from a single JSON Schema / CSDL source before they drift.

## License

MIT — see the repository [LICENSE](../../LICENSE).
