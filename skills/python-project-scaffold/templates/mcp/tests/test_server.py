from typing import Any

import httpx
import pytest
from mcp.server.mcpserver.exceptions import ToolError

from __PKG__.api import HttpApiClient
from __PKG__.server import build_server

from .conftest import BASE_URL, FakeService


def structured(result: Any) -> dict[str, Any]:
    """Pull the structured payload out of a tool call result."""
    assert not result.is_error, result.content
    return dict(result.structured_content)


async def test_every_tool_declares_whether_it_writes(api: HttpApiClient) -> None:
    tools = await build_server(api).list_tools()
    assert tools, "the server offers no tools"
    for tool in tools:
        assert tool.annotations is not None, tool.name
        assert tool.annotations.read_only_hint is not None, tool.name


async def test_status_through_mcp(api: HttpApiClient) -> None:
    status = structured(await build_server(api).call_tool("service_status", {}))
    assert status == {"base_url": BASE_URL, "version": "1.2.3"}


async def test_status_without_a_version(api: HttpApiClient, fake: FakeService) -> None:
    fake.routes["GET", "/api/status"] = httpx.Response(200, json={})
    status = structured(await build_server(api).call_tool("service_status", {}))
    assert status["version"] is None


async def test_errors_reach_the_model_with_their_message(
    api: HttpApiClient, fake: FakeService
) -> None:
    fake.routes["GET", "/api/status"] = httpx.Response(503)
    with pytest.raises(ToolError, match="answered HTTP 503"):
        await build_server(api).call_tool("service_status", {})
