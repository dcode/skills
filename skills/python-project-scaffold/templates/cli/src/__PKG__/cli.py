"""Command-line entry point."""

import sys
from collections.abc import Sequence
from typing import Annotated

from cyclopts import App, Parameter

from __PKG__ import __version__

app = App(name="__DIST_NAME__", help="__DESCRIPTION__", version=__version__)


@app.default
def greet(name: Annotated[str, Parameter(help="Who to greet.")] = "world") -> None:
    """Print a greeting. Replace with the first real command.

    Args:
        name: Who to greet.
    """
    print(f"Hello, {name}!")


def main(argv: Sequence[str] | None = None) -> None:
    """Run the command line and exit with its status.

    Args:
        argv: Arguments without the program name; defaults to ``sys.argv[1:]``.
    """
    app(sys.argv[1:] if argv is None else argv)
