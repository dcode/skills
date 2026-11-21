"""The seam between the MCP tools and the service they call.

Tools depend only on the ``ApiClient`` protocol. ``HttpApiClient`` is the real
adapter; tests substitute an in-process fake through ``httpx.MockTransport``
or a plain class with the same methods.
"""

from typing import Any, Protocol, Self

import httpx
import structlog

from __PKG__.errors import ApiError, ConnectivityError

type JsonObject = dict[str, Any]

log = structlog.get_logger(__name__)


class ApiClient(Protocol):
    """What a tool may ask of the service."""

    base_url: str

    async def get(self, path: str, params: dict[str, str | int] | None = None) -> JsonObject:
        """Read one JSON object.

        Args:
            path: Path relative to ``base_url``.
            params: Query parameters.

        Returns:
            The decoded JSON object.
        """
        ...

    async def aclose(self) -> None:
        """Release the connection."""
        ...


class HttpApiClient:
    """``ApiClient`` over HTTP with httpx."""

    def __init__(
        self,
        base_url: str,
        *,
        timeout: float = 30.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        """Create the adapter.

        Args:
            base_url: Root URL of the service's API.
            timeout: Seconds to wait for each request.
            transport: Replacement transport, used by tests.
        """
        self.base_url = base_url.rstrip("/")
        self._http = httpx.AsyncClient(
            base_url=self.base_url + "/", timeout=timeout, transport=transport
        )

    async def __aenter__(self) -> Self:
        """Enter the context; the client is already open."""
        return self

    async def __aexit__(self, *_: object) -> None:
        """Close the client on leaving the context."""
        await self.aclose()

    async def get(self, path: str, params: dict[str, str | int] | None = None) -> JsonObject:
        """Read one JSON object.

        Args:
            path: Path relative to ``base_url``.
            params: Query parameters.

        Returns:
            The decoded JSON object.

        Raises:
            ConnectivityError: The service could not be reached.
            ApiError: The service answered with an error or something other than an object.
        """
        try:
            response = await self._http.get(path.lstrip("/"), params=params)
        except httpx.HTTPError as exc:
            raise ConnectivityError(
                f"Could not reach {self.base_url}: {exc.__class__.__name__}. "
                "Check the address and your network connection."
            ) from exc
        log.debug("http_response", method="GET", path=path, status=response.status_code)
        if response.is_error:
            raise ApiError(
                response.status_code,
                f"{self.base_url} answered HTTP {response.status_code} for {path}.",
            )
        body = response.json()
        if not isinstance(body, dict):
            raise ApiError(response.status_code, f"Expected a JSON object from {path}.")
        return body

    async def aclose(self) -> None:
        """Release the connection."""
        await self._http.aclose()
