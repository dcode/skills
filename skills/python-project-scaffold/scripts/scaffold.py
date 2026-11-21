#!/usr/bin/env python3
"""Render the project templates into a target directory.

Stdlib only, so it runs before the new project has an environment. It writes files and
nothing else: no installs, no network, no git.
"""

import argparse
import datetime
import keyword
import re
import sys
from dataclasses import dataclass
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "assets" / "templates"
DIST_NAME = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
PY_VERSION = re.compile(r"3\.(\d+)")
KINDS = ("lib", "cli", "mcp")

# Template layers per kind; a later layer's file replaces an earlier one at the same path.
LAYERS: dict[str, tuple[str, ...]] = {
    "lib": ("common",),
    "cli": ("common", "cli"),
    "mcp": ("common", "mcp"),
}

# Runtime dependencies per kind. `uv lock --upgrade` picks the newest compatible versions.
DEPENDENCIES: dict[str, tuple[str, ...]] = {
    "lib": (),
    "cli": ("cyclopts>=5.4",),
    "mcp": (
        "cyclopts>=5.4",
        "httpx>=0.28",
        "mcp>=2.3,<3",
        "pydantic>=2.14",
        "structlog>=26.1",
    ),
}

# Where CI installs the built wheel to check it runs. A path in the CI runner's shell,
# not a temporary file this script creates.
WHEEL_CHECK = "/tmp/wheel-check"  # noqa: S108

MCP_USAGE = """\
Run the server over stdio; agent hosts start it this way:

```bash
{env_prefix}_BASE_URL=https://service.example/api uv run {name} serve
```

Register it with an agent host that reads the common `mcpServers` JSON shape:

```json
{{
  "mcpServers": {{
    "{name}": {{
      "command": "uv",
      "args": ["run", "--directory", "/path/to/{name}", "{name}", "serve"],
      "env": {{ "{env_prefix}_BASE_URL": "https://service.example/api" }}
    }}
  }}
}}
```"""

MIT_LICENSE = """\
MIT License

Copyright (c) {year} {holder}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


@dataclass(frozen=True, slots=True)
class Options:
    """Validated command-line options.

    Attributes:
        target: Directory to write into.
        dist_name: Distribution name, kebab-case.
        description: One-line description, ending in a period.
        kind: ``lib``, ``cli`` or ``mcp``.
        license: SPDX license expression.
        holder: Copyright holder for the MIT license text.
        repo: GitHub ``owner/repo``.
        python: Minimum Python version, ``3.N``.
        force: Overwrite existing files.
    """

    target: Path
    dist_name: str
    description: str
    kind: str
    license: str
    holder: str
    repo: str
    python: str
    force: bool

    @property
    def package(self) -> str:
        """Import name derived from the distribution name."""
        return self.dist_name.replace("-", "_")


def error_base_name(package: str) -> str:
    """Name the package's base exception, e.g. ``log_shipper`` -> ``LogShipperError``.

    Args:
        package: Import name of the package.

    Returns:
        A CamelCase class name ending in ``Error``.
    """
    return "".join(part.capitalize() for part in package.split("_")) + "Error"


def parse_args(argv: list[str]) -> Options:
    """Parse and validate the command line.

    Args:
        argv: Arguments without the program name.

    Returns:
        The validated options.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="directory to create or fill")
    parser.add_argument("--name", required=True, help="distribution name, kebab-case")
    parser.add_argument("--description", required=True, help="one-line description")
    parser.add_argument("--kind", choices=KINDS, default="lib")
    parser.add_argument("--license", default="MIT", help="SPDX expression (default MIT)")
    parser.add_argument("--holder", default="", help="copyright holder for an MIT LICENSE")
    parser.add_argument("--repo", default="", help="GitHub owner/repo")
    parser.add_argument("--python", default="3.14", help="minimum Python, 3.N (default 3.14)")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args(argv)

    if not DIST_NAME.fullmatch(args.name):
        parser.error(f"--name {args.name!r} must be lower-case kebab-case, e.g. log-shipper")
    if keyword.iskeyword(args.name.replace("-", "_")):
        parser.error(f"--name {args.name!r} is a Python keyword")
    if not PY_VERSION.fullmatch(args.python):
        parser.error(f"--python {args.python!r} must look like 3.14")
    description = args.description.strip()
    if not description or any(c in description for c in '"\\\n'):
        parser.error("--description must be one non-empty line without quotes or backslashes")
    if description[-1] not in ".!?":
        description += "."
    if args.repo and not re.fullmatch(r"[\w.-]+/[\w.-]+", args.repo):
        parser.error(f"--repo {args.repo!r} must be owner/repo")

    return Options(
        target=args.target,
        dist_name=args.name,
        description=description,
        kind=args.kind,
        license=args.license,
        holder=args.holder or "the " + args.name + " authors",
        repo=args.repo or f"OWNER/{args.name}",
        python=args.python,
        force=args.force,
    )


def substitutions(opts: Options) -> dict[str, str]:
    """Build the token table for the templates.

    Args:
        opts: The validated options.

    Returns:
        A mapping from ``__TOKEN__`` to its replacement.
    """
    minor = PY_VERSION.fullmatch(opts.python)
    if minor is None:  # pragma: no cover - parse_args already validated it
        raise ValueError(f"bad Python version {opts.python!r}")
    has_command = opts.kind in {"cli", "mcp"}
    scripts_block = (
        f'\n[project.scripts]\n{opts.dist_name} = "{opts.package}.cli:main"\n'
        if has_command
        else ""
    )
    if has_command:
        smoke = f"{WHEEL_CHECK}/bin/{opts.dist_name} --version"
    else:
        smoke = (
            f"{WHEEL_CHECK}/bin/python -c "
            f'"import {opts.package}; print({opts.package}.__version__)"'
        )
    env_prefix = opts.package.upper()
    match opts.kind:
        case "mcp":
            usage = MCP_USAGE.format(name=opts.dist_name, env_prefix=env_prefix)
        case "cli":
            usage = f"```bash\nuv run {opts.dist_name} --help\n```"
        case _:
            usage = f"```python\nimport {opts.package}\n```"
    dependencies = "".join(f'\n    "{dep}",' for dep in DEPENDENCIES[opts.kind])
    return {
        "__DIST_NAME__": opts.dist_name,
        "__PKG__": opts.package,
        "__DESCRIPTION__": opts.description,
        "__TITLE__": opts.description.rstrip(".!?"),
        "__LICENSE__": opts.license,
        "__PY_VERSION__": opts.python,
        "__PY_TAG__": f"py3{minor.group(1)}",
        "__REPO__": opts.repo,
        "__DATE__": datetime.date.today().isoformat(),
        "__ERROR_BASE__": error_base_name(opts.package),
        "__DEPENDENCIES__": dependencies + ("\n" if dependencies else ""),
        "__ENV_PREFIX__": env_prefix,
        "__SCRIPTS_BLOCK__": scripts_block,
        "__WHEEL_SMOKE__": smoke,
        "__USAGE__": usage,
    }


def render(text: str, table: dict[str, str]) -> str:
    """Replace every token in a template.

    Args:
        text: Template text.
        table: Tokens and their replacements.

    Returns:
        The rendered text.

    Raises:
        ValueError: A ``__TOKEN__`` was left unreplaced.
    """
    for token, value in table.items():
        text = text.replace(token, value)
    leftover = re.findall(r"__[A-Z][A-Z_]*[A-Z]__", text)
    if leftover:
        raise ValueError(f"unreplaced template tokens: {sorted(set(leftover))}")
    return text


def plan(opts: Options) -> dict[Path, str]:
    """Work out every file to write and its content.

    Args:
        opts: The validated options.

    Returns:
        Target path to rendered content, in a stable order.
    """
    table = substitutions(opts)
    files: dict[Path, str] = {}
    for layer in LAYERS[opts.kind]:
        root = TEMPLATES / layer
        for source in sorted(p for p in root.rglob("*") if p.is_file()):
            relative = Path(render(str(source.relative_to(root)), table))
            files[opts.target / relative] = render(source.read_text(), table)
    if opts.license == "MIT":
        year = datetime.date.today().year
        files[opts.target / "LICENSE"] = MIT_LICENSE.format(year=year, holder=opts.holder)
    return files


def main(argv: list[str] | None = None) -> int:
    """Generate the project.

    Args:
        argv: Arguments without the program name; defaults to ``sys.argv[1:]``.

    Returns:
        The process exit status.
    """
    opts = parse_args(sys.argv[1:] if argv is None else argv)
    files = plan(opts)
    clashes = [path for path in files if path.exists()]
    if clashes and not opts.force:
        print("Refusing to overwrite (pass --force to allow):", file=sys.stderr)
        for path in clashes:
            print(f"  {path}", file=sys.stderr)
        return 1
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(path)
    if opts.license != "MIT":
        print(
            f"No LICENSE written: add the {opts.license} text before building.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
