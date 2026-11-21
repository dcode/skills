import httpx
import pytest

from __PKG__.api import HttpApiClient
from __PKG__.errors import ApiError, ConnectivityError

from .conftest import BASE_URL, FakeService


async def test_get_returns_the_json_object(api: HttpApiClient, fake: FakeService) -> None:
    assert await api.get("/status", params={"verbose": 1}) == {"version": "1.2.3"}
    assert str(fake.requests[0].url) == f"{BASE_URL}/status?verbose=1"


async def test_error_status_becomes_api_error(api: HttpApiClient) -> None:
    with pytest.raises(ApiError, match="HTTP 404 for missing") as info:
        await api.get("missing")
    assert info.value.status == 404


async def test_non_object_body_is_rejected(api: HttpApiClient, fake: FakeService) -> None:
    fake.routes["GET", "/api/list"] = httpx.Response(200, json=[1, 2])
    with pytest.raises(ApiError, match="Expected a JSON object"):
        await api.get("list")


async def test_network_failure_becomes_connectivity_error() -> None:
    def refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    async with HttpApiClient(BASE_URL, transport=httpx.MockTransport(refuse)) as api:
        with pytest.raises(ConnectivityError, match=r"Could not reach .* ConnectError"):
            await api.get("status")
