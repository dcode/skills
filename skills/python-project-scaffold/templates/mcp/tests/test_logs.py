import json
import logging
import sys

import pytest
import structlog

from __PKG__.logs import configure_logging


def test_json_lines_go_to_stderr_only(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("info")
    structlog.get_logger("test").debug("hidden")
    structlog.get_logger("test").info("shown", status=200)
    captured = capsys.readouterr()
    assert captured.out == ""
    event = json.loads(captured.err)
    assert (event["event"], event["level"], event["status"]) == ("shown", "info", 200)


def test_terminal_gets_readable_lines(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys.stderr, "isatty", lambda: True)
    configure_logging("debug")
    structlog.get_logger("test").debug("http_response")
    assert not capsys.readouterr().err.lstrip().startswith("{")


def test_noisy_libraries_stay_at_warning() -> None:
    configure_logging("debug")
    assert logging.getLogger("httpx").level == logging.WARNING
