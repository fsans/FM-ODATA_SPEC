# AGENTS.md

Guidance for AI agents (Devin, Claude, Cursor, etc.) working on this repository.

## Project type

This is a **specification repository**, not a runnable application. It contains:

1. Markdown documentation (`docs/`) — the human-readable spec.
2. A JSON capability manifest (`schema/fms-odata-capabilities.json`) — machine-readable.
3. A TypeScript types package (`packages/fms-odata-spec-ts/`) — shared types for downstream libraries (npm: `@fms-odata/spec-ts`).
4. A Python types package (`packages/fms-odata-spec-py/`) — the same surface as the TS package, as stdlib dataclasses (PyPI: `fms-odata-spec`).

## Key conventions

- **No emojis** in any generated markdown or code.
- **No runtime code** — the TS package is types-only (no implementation logic). The Python package is types + pure helpers only (no HTTP client, no validation framework).
- **Source of truth**: official Claris OData docs (https://help.claris.com/en/odata-guide/) + observed behavior from the two reference repos in `_research/` (gitignored).
- **Version naming**: use "FileMaker 19.x", "Claris 2023", "Claris 2024", "Claris 2026" (current). Never guess future version numbers.
- **OData protocol version**: FileMaker implements OData 4.0, not 4.01. The 4.01 spec is referenced for conventions only.
- **URL pattern**: `https://host/fmi/odata/v4/<database>/<resource>` — version segment is always `v4`.

## Branching model (Git Flow)

- **`main`**: Stable releases only. Every commit is a merge from `develop` and is tagged with an annotated version tag.
- **`develop`**: Active development branch. All work lands here first.
- Feature branches (optional): branch off `develop`, merge back into `develop`.

**When making changes:**

1. Commit work to `develop`.
2. When ready for release, merge `develop` into `main` (fast-forward or merge commit).
3. Tag the release on `main` with an annotated tag: `git tag -a vMAJOR.MINOR.PATCH -m "..."`.
4. Push everything: `git push origin develop main --tags`.

**Tag rules:**
- Semantic versioning: `vMAJOR.MINOR.PATCH`.
- Annotated tags only (`git tag -a`), never lightweight tags.
- Tags only on `main`, never on `develop`.
- If `@fms-odata/spec-ts` package version changes, the tag must match it.

## When updating the spec for a new FileMaker Server release

1. Read the official Claris OData docs for the new version.
2. Update `docs/12-version-deltas.md` with a new section for the release.
3. Update `docs/01-conformance.md` if conformance level or supported/unsupported features changed.
4. Update `docs/13-quirks.md` if new quirks or bug fixes were observed.
5. Update `schema/fms-odata-capabilities.json` with new version entry and feature flags.
6. Update `packages/fms-odata-spec-ts/src/versions.ts` with the new version constant and feature matrix.
7. Update `packages/fms-odata-spec-py/src/fms_odata_spec/versions.py` with the same version constant and feature matrix (mirror the TS package).
8. Update `README.md` version table if a new version was added.

## File structure rules

- `_research/` is gitignored — never commit cloned repos.
- `docs/` files are numbered (`00-`, `01-`, ...) for reading order.
- `packages/fms-odata-spec-ts/` is a publishable npm package (`@fms-odata/spec-ts`).
- `packages/fms-odata-spec-py/` is a publishable Python package (`fms-odata-spec` on PyPI), versioned independently of the TS package. It is NOT part of any npm workspace glob.
- `schema/` contains only the single capabilities JSON manifest.

## Verification

There is no build step for the docs. For the TS package:

```bash
cd packages/fms-odata-spec-ts
npm install
npm run build      # tsc --emitDeclarationOnly
npm run typecheck  # tsc --noEmit
```

The JSON manifest can be validated with any JSON schema validator. No formal JSON Schema is provided yet — the manifest is self-describing.

For the Python package:

```bash
cd packages/fms-odata-spec-py
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest                           # 159 tests
python -m build                  # sdist + wheel into dist/
```

## TODO — fms-odata-spec-py v0.1.0 release blockers

> **IMPORTANT — read this before cutting the Python v0.1.0 release.**
> These items were intentionally deferred during the initial port and MUST be
> addressed before publishing `fms-odata-spec` 0.1.0 to PyPI. Do NOT silently
> drop them; either complete them or explicitly move them to a later milestone.

1. **PyPI publishing workflow** — `.github/workflows/py-ci.yml` runs tests and
   `python -m build` but does NOT publish. Add a publish job (or separate
   workflow) using `twine upload`, gated on a `PYPI_API_TOKEN` repository
   secret, triggered on tag pushes matching the Python package version. The
   Python package is versioned independently of the TS package and of git tags
   on `main`; decide on a tag scheme (e.g. `py-v0.1.0`) to avoid collision with
   the existing `vMAJOR.MINOR.PATCH` TS tags.

2. **LICENSE bundling** — `pyproject.toml` declares `license = "MIT"` and the
   Python README links to the root `LICENSE`, but hatchling does NOT bundle the
   root `LICENSE` into the sdist/wheel automatically. Either copy `LICENSE`
   into `packages/fms-odata-spec-py/` or add a `[tool.hatch.build]` include for
   `../../LICENSE`. PyPI will warn about a missing license file otherwise.

3. **CHANGELOG** — no `CHANGELOG.md` exists for the Python package (the TS
   package has none either, so this is consistent). For semver discipline on
   PyPI, add at least a `packages/fms-odata-spec-py/CHANGELOG.md` with the
   0.1.0 entry before publishing.

4. **`ODataEntity[T]` ergonomics review** — the wrapping-dataclass approach
   means callers access `envelope.entity.field` rather than `envelope.field`.
   This is the one place the Python API is noticeably less ergonomic than the
   TS intersection type. Before 0.1.0, decide whether to keep it as-is (and
   document it loudly) or add a `from_dict` constructor / `Mapping`-backed
   variant. Changing it after 0.1.0 is a breaking change.

5. **CI matrix Python 3.14** — `py-ci.yml` matrix tops out at 3.13. Python 3.14
   is released; add `"3.14"` to the matrix once
   `actions/setup-python` ships a stable 3.14 on the runners.

6. **Async token-refresh helper** — `FMIDAuthConfig.on_unauthorized` is typed
   but nothing invokes it (this package is types + pure helpers only). This
   matches the TS package, but document it explicitly in the Python README so
   downstream consumers know they must wire it up themselves.

7. **Shared schema source** — if a genuinely shared schema/spec source (JSON
   Schema, OpenAPI, or OData CSDL) is introduced later, both language packages
   should be generated from or validated against it. This was deferred per the
   original task instructions ("ask before moving anything"). Revisit before
   the two packages drift apart in content.

## Branch state of the Python package

- Initial port landed on branch `feature/py-spec` (branched from `develop`).
- Merge `feature/py-spec` into `develop` via a PR once reviewed.
- The Python package version (`0.1.0`) is independent of the TS package
  version (`1.1.0`) and of any git tag on `main`. Do not lockstep them unless
  explicitly asked.
