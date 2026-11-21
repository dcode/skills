"""Command-line entry point: run the MCP server over stdio."""

import asyncio
import sys
from collections.abc import Sequence
from typing import Annotated

import httpx
from cyclopts import App, Parameter

from __PKG__ import __version__
from __PKG__.api import HttpApiClient
from __PKG__.logs import LogLevel, configure_logging
from __PKG__.server import build_server

app = App(name="__DIST_NAME__", help="__DESCRIPTION__", version=__version__)


async def serve_stdio(base_url: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
    """Run the MCP server over stdio until the client disconnects.

    Args:
        base_url: Root URL of the service's API.
        transport: Replacement HTTP transport, used by tests.
    """
    async with HttpApiClient(base_url, transport=transport) as api:
        await build_server(api).run_stdio_async()


@app.command
def serve(
    *,
    base_url: Annotated[str, Parameter(env_var="__ENV_PREFIX___BASE_URL")],
    log_level: LogLevel = "info",
) -> None:
    """Run the MCP server over stdio. Agent hosts start this command.

    Args:
        base_url: Root URL of the service's API.
        log_level: Lowest log level written to stderr.
    """
    configure_logging(log_level)
    asyncio.run(serve_stdio(base_url))


def main(argv: Sequence[str] | None = None) -> None:
    """Run the command line and exit with its status.

    Args:
        argv: Arguments without the program name; defaults to ``sys.argv[1:]``.
    """
    app(sys.argv[1:] if argv is None else argv)
