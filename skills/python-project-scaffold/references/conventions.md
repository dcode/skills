# Code conventions

Rules for writing code in a project made with this skill. The tool configuration enforces
most of them; the rest are judgment calls that review should catch.

## Language level

- Target the newest stable Python the project allows (3.14 by default) and use its features:
  `X | None` (never `Optional`), built-in generics (`list[str]`, `dict[str, Any]`), `type`
  aliases (`type Headers = dict[str, str]`), PEP 695 generics (`def first[T](xs: list[T]) ->
  T`), `match` where it reads better than an `if` chain, `@override` on overriding methods,
  and `Self` for fluent returns.
- Annotate every function, method, and module-level constant, including `-> None`. Test
  functions are exempt from ruff's `ANN` rules but are annotated anyway, fixtures included
  (`capsys: pytest.CaptureFixture[str]`).
- Use `Annotated[...]` to attach metadata (pydantic constraints, cyclopts parameters) rather
  than defaults with side effects.
- Abstract types in signatures, concrete types in returns: accept `Sequence`/`Mapping`/
  `Iterable` from `collections.abc`, return `list`/`dict`.
- Prefer `Protocol` for seams between layers (for example an `ApiClient` protocol with one
  adapter per kind of service), so tests can substitute fakes without inheritance.
- Immutable data by default: `@dataclass(frozen=True, slots=True)` or a frozen pydantic
  model for anything parsed from outside.

## Async and I/O

- Anything that waits on the network, a subprocess or a slow disk is `async`. Use `httpx`'s
  `AsyncClient`, `asyncio.TaskGroup` for concurrency, and `asyncio.timeout()` for deadlines.
- Never block the event loop: ruff's `ASYNC` rules are on. A justified exception is
  suppressed on the line with its reason, for example
  `path.expanduser()  # noqa: ASYNC240 - reads $HOME only, no file I/O`.
- Close what you open: async context managers, or an explicit `aclose()` on the owning
  object.

## Errors

- One base exception per package (`<Project>Error` in `errors.py`), with a subclass per
  failure the caller can act on (configuration, authentication, not found, connectivity).
- Messages are plain language, safe to show a user, and never contain secrets.
- Catch the narrowest exception that you can handle; let the rest propagate. No bare
  `except`, no `except Exception: pass`.

## Docstrings and comments

- Google style, enforced by ruff's `D` rules: a module docstring on every module, a
  docstring on every public function, class and method, with `Args:`, `Returns:`, `Raises:`
  and `Attributes:` sections where they apply.
- Comments say why, not what. A non-obvious constant or workaround gets a comment with the
  reason and, when there is one, the evidence (a server version, an issue link).
- American English throughout, code and docs.

## Suppressions

- Never a blanket ignore. Each `# noqa: CODE`, `# type: ignore[code]` or
  `# ty: ignore[rule]` names the rule and, if not obvious, gives the reason after ` - `.
- A rule disabled for the whole project goes in `pyproject.toml` with a comment saying why.
- The security rules (`S`) are on. Fix the finding rather than suppress it: no
  `subprocess` with `shell=True`, no `pickle`/`eval` of outside data, `secrets` not
  `random` for anything security-related, explicit `timeout=` on network calls. When a
  finding is a false positive (a fixed command list to `subprocess.run`, a path that is
  not a temp file), suppress that line with the reason. Tests may `assert` (S101 is off
  there).
- The pytest rules (`PT`) are on: `pytest.raises` gets a `match=` for broad exceptions,
  one statement per `raises` block, fixtures without needless parentheses.

## Logging and output

- Library code logs; it does not print. Use `structlog` (or `logging`) to stderr, rendered
  for people on a terminal and as JSON lines otherwise. Never log secrets: redact tokens,
  cookies and authorization headers before they reach a logger.
- Anything that speaks a protocol on stdout (an MCP server, a pipe-friendly CLI) must never
  write logs there.

## MCP servers

- Tools never make HTTP calls themselves. They call an `ApiClient` protocol; each kind of
  service gets one adapter implementing it, so a second backend or a test fake needs no
  change to the tools.
- Every tool declares `ToolAnnotations` (`read_only_hint`, and for writes
  `destructive_hint` and `idempotent_hint`) so agent hosts can ask before a change.
- Errors raised on purpose are passed to the model with their message (the `anticipated`
  wrapper re-raises them as `ToolError`); the SDK hides the text of anything else.
- Tools return pydantic models, so the agent gets structured output with a schema.
- Write tools default to a dry run that reports the request it would send, until the user
  turns writes on in the config.
- The docstring of a tool is the model's only manual: say when to call it, what it returns,
  and what to do when it fails.
- Test every tool through `build_server(...).call_tool(...)` against the in-process fake,
  including its failure path.

## Default libraries

Reach for these when the need arises; do not add them speculatively.

| Need | Library |
|---|---|
| CLI | `cyclopts` (with `rich` for output) |
| HTTP | `httpx` (async), `truststore` for the system trust store |
| Data validation and settings | `pydantic` v2 |
| Logging | `structlog` |
| Secrets at rest | `keyring` |
| TOML read | `tomllib` (stdlib) |

Add runtime dependencies with `uv add <pkg>` and dev ones with `uv add --dev <pkg>`; never
edit `uv.lock` by hand.

## Configuration and secrets

- User configuration lives outside the repository (`~/.config/<project>/config.toml`); the
  repo ships a `config.example.toml` with placeholder values only.
- Secrets come from the OS keychain (`keyring`), an environment variable, or an untracked
  env file, never from a tracked file. `.gitignore` already excludes `.env`, `*.env`,
  `.secrets/`, `*.pem` and `config.toml`. Commit a `.env.example` with `<placeholder>`
  values when scripts need local values.
- No real hostnames, account names or ticket keys in tracked files, tests included; use
  `example.com`-style placeholders.

## Tests

- Mirror the source: `src/<pkg>/foo.py` is tested by `tests/test_foo.py`.
- Plain functions, not classes. `async def test_...` works without a decorator
  (`asyncio_mode = "auto"`).
- Parametrize instead of copying, with the argument names as a tuple:
  `@pytest.mark.parametrize(("a", "b"), [...])`.
- No test reaches a real server. Fake external services in-process, for example an
  `httpx.MockTransport` handler that routes on method and path, shared through fixtures in
  `tests/conftest.py`. Things that can only be checked against the real service go in
  ROADMAP.md under "Confirm against the real thing", with the exact command to run.
- Assert on behavior the caller sees (return values, raised error type and message, log
  events), not on private state.
- Branch coverage is held at 100% (`fail_under = 100`). `if TYPE_CHECKING:` is excluded
  already; a line that truly cannot be tested gets `# pragma: no cover - <reason>`, and
  review questions every one.

## Git

- Conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`, `build:`,
  `ci:`, `style:`, `perf:`, with an optional scope (`feat(config): ...`). Subject in the
  imperative, lower case after the colon, no trailing period.
- One logical change per commit, and the ROADMAP.md update travels with it.
- Experimental probes that are not product code live in `scripts/` with a `spike:` commit
  prefix, and their findings are recorded in ROADMAP.md or DESIGN.md.
- Release tags (`vX.Y.Z`) go on the commit that changes `__version__`.
