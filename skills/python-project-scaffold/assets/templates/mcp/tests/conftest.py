"""Shared fixtures: a fake service served through httpx.MockTransport."""

from collections.abc import AsyncIterator

import httpx
import pytest

from __PKG__.api import HttpApiClient

BASE_URL = "https://service.example/api"


class FakeService:
    """In-process stand-in for the real service. Extend ``routes`` per test."""

    def __init__(self) -> None:
        self.routes: dict[tuple[str, str], httpx.Response] = {
            ("GET", "/api/status"): httpx.Response(200, json={"version": "1.2.3"}),
        }
        self.requests: list[httpx.Request] = []

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return self.routes.get(
            (request.method, request.url.path), httpx.Response(404, json={"error": "not found"})
        )

    @property
    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handle)


@pytest.fixture
def fake() -> FakeService:
    return FakeService()


@pytest.fixture
async def api(fake: FakeService) -> AsyncIterator[HttpApiClient]:
    async with HttpApiClient(BASE_URL, transport=fake.transport) as client:
        yield client
