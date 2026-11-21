import runpy
import sys

import pytest

from __PKG__ import __version__
from __PKG__.cli import main


def run(*args: str) -> int | str | None:
    with pytest.raises(SystemExit) as exit_:
        main(args)
    return exit_.value.code


def test_greets_the_world_by_default(capsys: pytest.CaptureFixture[str]) -> None:
    assert run() == 0
    assert capsys.readouterr().out == "Hello, world!\n"


def test_greets_by_name(capsys: pytest.CaptureFixture[str]) -> None:
    assert run("--name", "Ada") == 0
    assert capsys.readouterr().out == "Hello, Ada!\n"


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    assert run("--version") == 0
    assert capsys.readouterr().out.strip() == __version__


def test_unknown_option_is_a_usage_error() -> None:
    assert run("--bogus") == 2


def test_runs_as_a_module(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["__PKG__", "--name", "module"])
    with pytest.raises(SystemExit) as exit_:
        runpy.run_module("__PKG__", run_name="__main__")
    assert exit_.value.code == 0
    assert capsys.readouterr().out == "Hello, module!\n"
