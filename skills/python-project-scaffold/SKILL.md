---
name: python-project-scaffold
description: >-
  Create a new Python project (library, CLI, or MCP server) already set up with the user's
  standard tooling and quality gates: uv, hatchling/hatch, ruff (including security and
  pytest rules), ty in strict mode, pytest with 100% branch coverage and pytest-asyncio,
  pre-commit (ruff, rumdl, taplo, ty), GitHub Actions CI and GitHub tag releases,
  Dependabot, and the working docs (ROADMAP.md, DESIGN.md, AGENTS.md) that keep context
  between sessions. Use when the user asks to start, scaffold, bootstrap or "set up" a Python
  project, package or MCP server, or to bring an existing Python repo up to these
  conventions. Not for one-off scripts that will never be a package.
compatibility: Requires python3, uv, and git; network access to resolve dependencies and hook revisions.
---

# Python project scaffold

This skill produces a repository that passes every check on its first commit and carries the
working documentation needed to pick it back up after days away. The conventions come from a
mature project of the user's; [references/conventions.md](references/conventions.md) holds the
code-level rules to follow while writing code in the new project, and reading it is part of
step 4.

## What the user expects (non-negotiable defaults)

- **Python 3.14+** (`requires-python = ">=3.14"`), `src/` layout, strict type annotations
  everywhere, `async` for anything I/O-bound.
- **uv** manages environments and the lockfile; **hatchling** builds, with the version read
  from `__version__` in the package's `__init__.py`; **hatch** scripts wrap the common tasks.
- **ruff** for lint and format, with the security (`S`) and pytest-style (`PT`) rules on;
  **ty** for type checking with warnings as errors.
- **pytest** with **100% branch coverage enforced** (`fail_under = 100`), `pytest-asyncio`
  in auto mode, and no test that touches a real network service.
- **pre-commit** runs ruff, rumdl (Markdown), taplo (TOML) and ty; CI runs the same hooks.
- **GitHub only:** CI on GitHub Actions, releases as GitHub releases from a `v*` tag. No
  PyPI publishing; the user adds a trusted-publishing job themselves if a package needs it.
- **docs/ROADMAP.md is mandatory** and is updated in the same commit as the work it
  describes. It is the first thing read when coming back to the project.
- **AGENTS.md** (not CLAUDE.md) carries the instructions for coding agents.

Do not swap any of these for an alternative (mypy, black, poetry, setuptools, tox, nox,
unittest) unless the user asks.

## Workflow

### 1. Gather the inputs

Ask only for what cannot be inferred, and ask all the unknowns in a single round:

| Input | Default | Notes |
|---|---|---|
| Distribution name | from the directory or request | kebab-case, e.g. `log-shipper` |
| One-line description | none, ask | becomes `description` and the README tagline |
| Kind | see below | `lib`, `cli` or `mcp` |
| License (SPDX) | `MIT` | see step 3 for anything other than MIT |
| GitHub `owner/repo` | from `git remote` if one exists | used for links in the README |
| Python version | `3.14` | only lower it if the user says so |

Pick the kind from the request: `mcp` when it mentions MCP, an agent's tools, or a server an
agent host starts; `cli` when it mentions a command; otherwise `lib`.

Also ask what problem the project solves, in a sentence or two, because that seeds
DESIGN.md's Problem Statement. If the user has already described it, use that.

### 2. Generate the files

Run the bundled generator, [scripts/scaffold.py](scripts/scaffold.py); `<skill-dir>` below is this skill's directory. It
is stdlib-only and only writes files: it never installs, fetches or commits.

```bash
python3 <skill-dir>/scripts/scaffold.py <target-dir> \
  --name <dist-name> --description "<one line>" --kind lib|cli|mcp \
  --license MIT --repo <owner/repo>
```

It refuses to overwrite existing files unless `--force` is given, and prints every file it
wrote. Run `python3 <skill-dir>/scripts/scaffold.py --help` for all options.

Every kind gets:

```text
.github/dependabot.yml        weekly, grouped; commit prefixes ci: and build:
.github/workflows/ci.yml      pre-commit job, test on Linux + macOS, build + wheel smoke test
.github/workflows/release.yml v* tag -> check tag == __version__ -> CI -> GitHub release
.gitignore  .pre-commit-config.yaml  .taplo.toml  pyproject.toml  LICENSE (MIT only)
AGENTS.md                     agent instructions: read the roadmap first, gates, style
README.md                     quickstart, development, CI, releasing, hatch commands
docs/DESIGN.md                PRD-shaped design record
docs/ROADMAP.md               status, done, verify, next, later, open questions
src/<pkg>/__init__.py  src/<pkg>/py.typed  src/<pkg>/errors.py
tests/__init__.py  tests/test_package.py
```

Kind-specific additions:

| Kind | Adds | Runtime dependencies |
|---|---|---|
| `lib` | nothing | none |
| `cli` | `cli.py` (cyclopts app, `--version`), `__main__.py`, `tests/test_cli.py` | cyclopts |
| `mcp` | see below | cyclopts, httpx, mcp, pydantic, structlog |

The `mcp` kind follows the layering of the user's existing MCP server:

```text
src/<pkg>/api.py      ApiClient protocol (the seam) + HttpApiClient, an httpx adapter that
                      turns network and HTTP failures into the package's own errors
src/<pkg>/tools.py    register_tools(): tools with read/write ToolAnnotations, and the
                      @anticipated wrapper that passes the package's errors to the model
src/<pkg>/server.py   build_server(api) -> MCPServer
src/<pkg>/logs.py     structlog to stderr only (stdout carries the MCP protocol)
src/<pkg>/cli.py      `serve` command (stdio), base URL from --base-url or <PKG>_BASE_URL
src/<pkg>/errors.py   adds ConnectivityError and ApiError(status)
tests/conftest.py     FakeService on httpx.MockTransport, and an `api` fixture
tests/test_api.py  tests/test_server.py  tests/test_cli.py  tests/test_logs.py
```

The starter tool is `service_status`, calling `GET status` on the service. Replace it with
the real first tool, keeping the shape: one adapter method per service call, tools that only
call the `ApiClient` protocol, and a test through `server.call_tool` for every tool.

### 3. Fill in what the generator cannot

- **License:** for anything other than MIT, the generator writes no `LICENSE`. Fetch the
  canonical text (for example from `https://spdx.org/licenses/<id>.txt`) into `LICENSE`, or
  ask the user to drop it in. Hatchling fails to build without it.
- **DESIGN.md:** replace the `TODO` placeholders in Problem Statement and Solution with what
  the user told you in step 1. Leave the other sections' prompts for later, but do not leave
  a `TODO` in the two opening sections.
- **ROADMAP.md:** set "Where things stand" and put the user's first real goal under "Next
  up". The generator fills the date.

### 4. Install, lock and verify

Run these from the target directory, in order, and do not stop until all pass:

```bash
git init -b main          # skip if already a repo
uv sync                   # creates .venv and uv.lock
uv lock --upgrade         # newest compatible versions
uv run pre-commit autoupdate   # newest hook revisions
uv run pre-commit install
git add -A                # pre-commit only checks tracked files
uv run pre-commit run --all-files
uv run pytest
uv build
```

Then, if `hatch` is available (`uvx hatch` works when it is not installed):
`uvx hatch run check` and `uvx hatch test`. For a `cli` or `mcp` project also run
`uv run <dist-name> --version`.

If a hook rewrites files on the first run (taplo or rumdl formatting), `git add -A` and run
it again; the second run must be clean. If `autoupdate` moved a hook revision, mention it
in the report so the skill's template can be bumped too. Fix real failures instead of
loosening the config. Before writing any project code, read
[references/conventions.md](references/conventions.md).

### 5. First commit

Commit everything (including `uv.lock`) as a single conventional commit, e.g.
`chore: scaffold project`. Add the "Done" entry for the scaffold to ROADMAP.md in that same
commit (the template already has it). Do not create a GitHub repository, push, or tag unless
the user asks.

### 6. Report

Tell the user what was created, the result of each check, and anything left for them: a
non-MIT license text, the remote to push to, and the first item under "Next up".

## Bringing an existing repository up to these conventions

Run the generator into a scratch directory, then merge file by file instead of overwriting:

1. Diff each generated file against the repo's own. Keep the repo's dependencies, entry
   points and project-specific settings; adopt the tool sections (`[tool.ruff]`,
   `[tool.ty]`, `[tool.pytest]`, `[tool.coverage]`, `[tool.hatch.*]`) and the hook and CI
   files. If the repo has a CLAUDE.md, fold it into AGENTS.md.
2. If the repo has no ROADMAP.md, write one from what the git log and open issues show, and
   ask the user to confirm the "Next up" list.
3. Expect the first `pre-commit run --all-files` to produce many findings, especially from
   the `S` and `PT` rules. Apply the auto-fixes in one commit
   (`style: apply ruff and taplo formatting`), then fix the rest in separate, reviewable
   commits. Do not add blanket ignores to get green.
4. Existing code rarely starts at 100% coverage. Set `fail_under` to the current value
   rounded down, add "Raise coverage to 100%" under "Next up" in ROADMAP.md, and raise the
   floor as tests land. New projects always start at 100%.

## Working in a project made with this skill

These rules apply to every later session in the generated project, and AGENTS.md repeats
them:

- Read `docs/ROADMAP.md` before anything else; update it, including "Last updated", in the
  same commit as the work it describes.
- Record decisions and their reasons in `docs/DESIGN.md`; ROADMAP.md links to it rather than
  repeating it.
- `uv run pre-commit run --all-files` and `uv run pytest` must pass before every commit.
- Every new behavior gets a test, and branch coverage stays at 100%. A line that truly
  cannot be tested gets `# pragma: no cover - <reason>`.
- Releases: `hatch version minor|patch|major`, commit, tag `v<version>` on that commit,
  push the tag. The release workflow refuses a tag that does not match `__version__` and
  publishes a GitHub release only.
