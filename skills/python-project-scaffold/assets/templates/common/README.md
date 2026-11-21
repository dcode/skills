# __DIST_NAME__

__DESCRIPTION__

## Quickstart

```bash
git clone https://github.com/__REPO__.git
```

```bash
cd __DIST_NAME__ && uv sync
```

__USAGE__

## Design and roadmap

[docs/DESIGN.md](docs/DESIGN.md) records the design: the problem, the decisions made and the
reasons for them. [docs/ROADMAP.md](docs/ROADMAP.md) tracks what is done, what still needs
checking, and what comes next.

## Development

Install the git hooks once after cloning:

```bash
uv run pre-commit install
```

The hooks lint and format Python (ruff), Markdown (rumdl) and TOML (taplo), and type-check
with ty. To run everything by hand:

```bash
uv run pre-commit run --all-files
```

```bash
uv run pytest
```

### Continuous integration

GitHub Actions runs on every pull request and on every push to `main`:

| Job | What it does |
|---|---|
| Lint, format and type-check | All pre-commit hooks: ruff, rumdl, taplo and ty |
| Test | The test suite with the coverage threshold, on Linux and macOS |
| Build | Builds the sdist and wheel, installs the wheel into a clean environment, and uploads both as an artifact |

Dependabot opens weekly pull requests for GitHub Actions and Python dependency updates.

### Releasing

1. Bump the version: `hatch version minor` (or `patch`, `major`), then commit.
2. Tag that commit with the same version, prefixed with `v`, and push the tag:

   ```bash
   git tag v0.2.0 && git push origin v0.2.0
   ```

The release workflow checks that the tag matches `__version__`, runs the full CI suite, and
publishes a GitHub release with the sdist and wheel attached and generated release notes. It
does not publish to PyPI.

### With hatch

The same checks are available as [hatch](https://hatch.pypa.io/) commands, which manage their
own environments:

| Command | What it runs |
|---|---|
| `hatch test` | The test suite with branch coverage and the 100% threshold |
| `hatch test -k name --no-cov` | A subset of tests, without the coverage threshold |
| `hatch fmt` | ruff lint (with fixes) and format, using this project's settings |
| `hatch fmt --check` | The same, reporting only |
| `hatch run types` | ty type check |
| `hatch run hooks` | Every pre-commit hook on all files |
| `hatch run check` | Hooks, then tests |
| `hatch build` | Build the sdist and wheel into `dist/` |

Tool settings live in `pyproject.toml`, except taplo's, which it only reads from
`.taplo.toml`.
