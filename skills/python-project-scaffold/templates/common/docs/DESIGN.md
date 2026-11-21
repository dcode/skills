# __DIST_NAME__ — __TITLE__

The design record: the problem, the decisions made and the reasons for them. What is done and
what comes next is tracked in [ROADMAP.md](ROADMAP.md).

## Problem Statement

TODO: who has the problem, what they cannot do today, and what constrains the solution.

## Solution

TODO: what this project does about it, in a paragraph or two.

## User Stories

Numbered, grouped by area: "As a <role>, I want <capability>, so that <outcome>."

## Implementation Decisions

### Overall shape

How the code is organized and why: the main modules, the seams between them, and what a new
feature has to touch.

### Tooling and code style

- Python __PY_VERSION__+, uv for environments, hatchling build with the version read from
  `__version__`.
- Async for all I/O, Google-style docstrings, strict annotations throughout (`X | None`, never
  `Optional`; built-in generics such as `list[]`).
- ruff (lint and format, line length 100, including the `S` security and `PT` pytest
  rules), ty (type check, warnings are errors), rumdl
  (Markdown), taplo (TOML), all through pre-commit. Settings live in `pyproject.toml`, except
  taplo's, which live in `.taplo.toml`.
- pytest with branch coverage held at 100%. hatch scripts: `hatch test`,
  `hatch fmt`, `hatch run types`, `hatch run hooks`, `hatch run check`, `hatch build`.
- American English everywhere. Conventional-commit messages.
- GitHub Actions: pre-commit job, test job on Linux and macOS, build job that installs the
  wheel into a clean environment. A `v*` tag publishes a GitHub release (not to PyPI) after
  checking that the tag matches `__version__`. Dependabot runs weekly for Actions and Python.

## Testing Decisions

- Automated tests run against in-process fakes. Nothing in the suite contacts a real
  service.
- Branch coverage is held at 100%; a line that cannot be tested is excluded with
  `# pragma: no cover` and a reason.
- What can only be verified by hand is listed in ROADMAP.md under "Confirm against the real
  thing", with the command to run.

## Out of Scope

What this project deliberately does not do, each with the reason.

- **Publishing to PyPI.** Releases are GitHub releases only. If the package is ever
  published, add a trusted-publishing job to the release workflow.

## Further Notes

Findings, probe results and context that explain the decisions above.
