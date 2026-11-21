"""Assembles the MCP server."""

from mcp.server.mcpserver import MCPServer

from __PKG__ import __version__
from __PKG__.api import ApiClient
from __PKG__.tools import register_tools

INSTRUCTIONS = "Tools for __TITLE__. Call service_status first if a tool fails."


def build_server(api: ApiClient) -> MCPServer:
    """Create the MCP server with every tool registered.

    Args:
        api: The service the tools call.

    Returns:
        The server, ready to run.
    """
    server = MCPServer("__DIST_NAME__", instructions=INSTRUCTIONS, version=__version__)
    register_tools(server, api)
    return server
