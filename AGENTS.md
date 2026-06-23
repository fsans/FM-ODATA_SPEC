# AGENTS.md

Guidance for AI agents (Devin, Claude, Cursor, etc.) working on this repository.

## Project type

This is a **specification repository**, not a runnable application. It contains:

1. Markdown documentation (`docs/`) — the human-readable spec.
2. A JSON capability manifest (`schema/fm-odata-capabilities.json`) — machine-readable.
3. A TypeScript types package (`packages/fm-odata-spec-ts/`) — shared types for downstream libraries.

## Key conventions

- **No emojis** in any generated markdown or code.
- **No runtime code** — the TS package is types-only (no implementation logic).
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
- If `@fm-odata/spec-ts` package version changes, the tag must match it.

## When updating the spec for a new FileMaker Server release

1. Read the official Claris OData docs for the new version.
2. Update `docs/12-version-deltas.md` with a new section for the release.
3. Update `docs/01-conformance.md` if conformance level or supported/unsupported features changed.
4. Update `docs/13-quirks.md` if new quirks or bug fixes were observed.
5. Update `schema/fm-odata-capabilities.json` with new version entry and feature flags.
6. Update `packages/fm-odata-spec-ts/src/versions.ts` with the new version constant and feature matrix.
7. Update `README.md` version table if a new version was added.

## File structure rules

- `_research/` is gitignored — never commit cloned repos.
- `docs/` files are numbered (`00-`, `01-`, ...) for reading order.
- `packages/fm-odata-spec-ts/` is a publishable npm package (`@fm-odata/spec-ts`).
- `schema/` contains only the single capabilities JSON manifest.

## Verification

There is no build step for the docs. For the TS package:

```bash
cd packages/fm-odata-spec-ts
npm install
npm run build      # tsc --emitDeclarationOnly
npm run typecheck  # tsc --noEmit
```

The JSON manifest can be validated with any JSON schema validator. No formal JSON Schema is provided yet — the manifest is self-describing.
