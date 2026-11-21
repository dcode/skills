import runpy
import sys
from unittest.mock import AsyncMock

import pytest

from __PKG__ import __version__, cli
from __PKG__.cli import main, serve_stdio

from .conftest import BASE_URL, FakeService


def run(*args: str) -> int | str | None:
    with pytest.raises(SystemExit) as exit_:
        main(args)
    return exit_.value.code


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    assert run("--version") == 0
    assert capsys.readouterr().out.strip() == __version__


def test_serve_needs_a_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("__ENV_PREFIX___BASE_URL", raising=False)
    assert run("serve") != 0


@pytest.mark.parametrize(
    ("args", "env"),
    [(("serve", "--base-url", BASE_URL), None), (("serve",), BASE_URL)],
)
def test_serve_runs_the_server(
    monkeypatch: pytest.MonkeyPatch, args: tuple[str, ...], env: str | None
) -> None:
    if env:
        monkeypatch.setenv("__ENV_PREFIX___BASE_URL", env)
    served = AsyncMock()
    monkeypatch.setattr(cli, "serve_stdio", served)
    assert run(*args, "--log-level", "debug") == 0
    served.assert_awaited_once_with(BASE_URL)


async def test_serve_stdio_closes_the_client(
    monkeypatch: pytest.MonkeyPatch, fake: FakeService
) -> None:
    monkeypatch.setattr("mcp.server.mcpserver.MCPServer.run_stdio_async", AsyncMock())
    await serve_stdio(BASE_URL, transport=fake.transport)


def test_runs_as_a_module(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["__PKG__", "--version"])
    with pytest.raises(SystemExit) as exit_:
        runpy.run_module("__PKG__", run_name="__main__")
    assert exit_.value.code == 0
