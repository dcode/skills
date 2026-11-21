# __DIST_NAME__

__DESCRIPTION__

## Start here

1. Read [docs/ROADMAP.md](docs/ROADMAP.md): where things stand, what is next, and what is
   waiting on a check or a decision.
2. Read the relevant part of [docs/DESIGN.md](docs/DESIGN.md) before changing how something
   works.

## Rules

- Update `docs/ROADMAP.md` (including "Last updated") in the same commit as the work it
  describes. A new decision, and the reason for it, goes in `docs/DESIGN.md`.
- Before every commit both must pass:

  ```bash
  uv run pre-commit run --all-files
  ```

  ```bash
  uv run pytest
  ```

- Every behavior change comes with a test. Branch coverage must stay at 100%; a line that
  truly cannot be tested gets `# pragma: no cover - <why>`. Tests never contact a real
  service.
- Strict typing: annotate everything, `X | None` not `Optional`, built-in generics. ty
  warnings are errors.
- `async` for I/O. Google-style docstrings on every module and public object.
- ruff runs with the security (`S`) and pytest-style (`PT`) rules on. Suppressions name the
  rule and the reason: `# noqa: S603 - <why>`.
- Add dependencies with `uv add` / `uv add --dev`; never edit `uv.lock` by hand.
- Conventional commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`, `build:`,
  `ci:`). American English.
- Never commit secrets, real hostnames or account details; use placeholders and untracked
  `.env` files.

## Commands

| Task | Command |
|---|---|
| Install / sync | `uv sync` |
| All hooks | `uv run pre-commit run --all-files` |
| Tests with coverage | `uv run pytest` |
| One test, no coverage gate | `uv run pytest -k name --no-cov` |
| Type check | `uv run ty check` |
| Hooks then tests | `hatch run check` |
| Build | `uv build` |
| Release | `hatch version minor`, commit, `git tag v<version>`, push the tag |
