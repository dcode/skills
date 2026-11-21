"""MCP tool definitions."""

import functools
from collections.abc import Awaitable, Callable

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict

from __PKG__.api import ApiClient
from __PKG__.errors import __ERROR_BASE__

# Every tool declares whether it changes anything, so agent hosts can ask before writes.
READ = ToolAnnotations(read_only_hint=True, open_world_hint=True)
WRITE = ToolAnnotations(
    read_only_hint=False, destructive_hint=False, idempotent_hint=False, open_world_hint=True
)


def anticipated[**P, R](tool: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    """Pass this package's own errors to the model with their message intact.

    The MCP SDK hides the text of unexpected exceptions from the model. Errors
    raised on purpose carry plain-language guidance, so they are re-raised as
    the SDK's ``ToolError``, whose message is passed through.

    Args:
        tool: The async tool function to wrap.

    Returns:
        The wrapped tool, with the same signature.
    """

    @functools.wraps(tool)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await tool(*args, **kwargs)
        except __ERROR_BASE__ as exc:
            raise ToolError(str(exc)) from exc

    return wrapper


class ServiceStatus(BaseModel):
    """Result of the status tool.

    Attributes:
        base_url: Where the service is.
        version: Version the service reports, if any.
    """

    model_config = ConfigDict(frozen=True)

    base_url: str
    version: str | None = None


def register_tools(server: MCPServer, api: ApiClient) -> None:
    """Register every tool on an MCP server.

    Args:
        server: The MCP server to add tools to.
        api: The service the tools call.
    """

    @server.tool(annotations=READ)
    @anticipated
    async def service_status() -> ServiceStatus:
        """Check the connection to the service and report its version.

        Call this first if another tool fails, to see what is wrong.
        """
        body = await api.get("status")
        version = body.get("version")
        return ServiceStatus(
            base_url=api.base_url, version=version if isinstance(version, str) else None
        )
